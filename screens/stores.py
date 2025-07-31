from screens.modules import *

class StoresScreen(MDScreen):
    def __init__(self, stores_df, **kwargs):
        super().__init__(**kwargs)
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
        urls_screen = self.manager.get_screen("urls")
        urls_screen.update_urls(store_name, self.stores_df)
        self.manager.current = "urls"

    def get_card_size(self):
        return Window.width * 0.30  # ✅ Responsive card size