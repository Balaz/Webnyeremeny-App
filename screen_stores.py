import pandas as pd
import unicodedata

from screen_modules import *

def remove_accents(text: str) -> str:
    """
    Remove accents from text while preserving base characters.
    """
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                  if not unicodedata.combining(c))

def get_reference_stores() -> pd.DataFrame:
    """
    Reads the reference stores from a CSV file and returns a DataFrame.
    """
    try:
        stores_reference = pd.read_csv('hungarian_stores.csv')
    except FileNotFoundError:
        raise FileNotFoundError("hungarian_stores.csv file not found!")
    
    return stores_reference

def get_store_names(store_contests_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Collect store names from the contests DataFrame and match them with reference stores.
    Returns a DataFrame with store
    '''
    stores_reference = get_reference_stores()                               
    stores_reference = stores_reference['stores'].str.strip().str.lower()     # Clean and process stores_reference

    # Clean and process the games column
    stores_df = store_contests_df['games'].str.replace("-", ",").str.split(',').to_frame(name='games')
    stores_df = stores_df['games'].explode()        # Remove the list parameter
    stores_df = stores_df.str.strip().str.lower()   # Clean whitespace and normalize case
    stores_df = stores_df.to_frame(name='games')

    # Keep only the relevant stores from the reference
    filtered_df = pd.merge(stores_df, stores_reference, left_on='games', right_on='stores', how='inner').drop('games', axis=1)
    
    # Remove duplicates and reset index
    filtered_df = filtered_df.drop_duplicates(subset=['stores']).reset_index(drop=True)

    return filtered_df

def get_all_store_games(contests_df: pd.DataFrame ) -> pd.DataFrame:
    """    
    Collect stores from the contests DataFrame and match them with store URLs.
    Returns a DataFrame with store names and their corresponding URLs.
    """
    store_contests_df = contests_df[contests_df['title'] == 'Üzletekhez kötődő']
    
    store_names_df = get_store_names(store_contests_df)
    store_games_url_series = store_contests_df['urls'].explode()

    store_games_df = pd.DataFrame({
        "stores": store_names_df["stores"],
        "urls": [[]] * len(store_names_df["stores"])  # Initialize with empty lists
    })

    for index, row in store_games_df.iterrows():
        # Remove accents from store name for URL matching
        store_name_no_accents = remove_accents(row['stores'])
        # Match URLs using the accent-free version of the store name
        urls = store_games_url_series[
            store_games_url_series.str.contains(
                store_name_no_accents, 
                case=False, 
                na=False
            )
        ].tolist()
        store_games_df.at[index, 'urls'] = urls

    return store_games_df

class ScreenStores(MDScreen):
    def __init__(self, contests_df, **kwargs):
        super().__init__(**kwargs)
        stores_df = get_all_store_games(contests_df)
        self.stores_df = stores_df

        root = BoxLayout(orientation="vertical")

        appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    on_release=lambda *_: setattr(self.manager, "current", "main"),
                )
            ),
            MDTopAppBarTitle(text="Stores"),
            type="small",
        )
        root.add_widget(appbar)

        scroll = ScrollView()

        card_size = self.get_card_size()
        num_columns = max(1, int(Window.width // card_size))
        total_cards = num_columns * card_size
        spacing_x = (Window.width - total_cards) / (num_columns + 1)
        spacing_y = dp(20)


        flow = MDStackLayout(
            adaptive_height=True,
            size_hint_y=None,  # ✅ Enable vertical layout growth
            padding=[spacing_x, spacing_y, spacing_x, spacing_y],
            spacing=[spacing_x, spacing_y],
        )
        flow.bind(minimum_height=flow.setter("height"))  # ✅ Make layout expand with content

        for store in sorted(self.stores_df["stores"]):
            card_size = self.get_card_size()
            card = MDCard(
                size_hint=(None, None),
                size=(card_size, card_size),
                ripple_behavior=True,
                elevation=6,
                orientation="vertical",
            )
            logo_path = f"assets/logos/{store.lower()}.png"
            if not os.path.exists(logo_path):
                logo_path = "assets/logos/placeholder.png"
            card.add_widget(FitImage(source=logo_path, size_hint=(1, 0.7), allow_stretch=True,))

            card.bind(on_release=lambda _, s=store: self._open_store(s))
            flow.add_widget(card)

        scroll.add_widget(flow)
        root.add_widget(scroll)
        self.add_widget(root)

    def _open_store(self, store_name):
        games_screen = self.manager.get_screen("store_games")
        games_screen.update_games(store_name, self.stores_df)
        self.manager.current = "store_games"

    def get_card_size(self):
        return Window.width * 0.30  # ✅ Responsive card size