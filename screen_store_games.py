from screen_modules import *

BASE_URL = "https://www.webnyeremeny.hu"

class ScreenGame(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        self.title_label = MDTopAppBarTitle(text="")

        # Return button to go back to the stores screen
        appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    on_release=lambda *_: setattr(self.manager, "current", "stores"),
                )
            ),
            self.title_label,
            type="small",
        )
        root.add_widget(appbar)

        self.scroll = ScrollView()
        self.flow = MDStackLayout(
            adaptive_height=True,
            size_hint_y=None,
            padding=dp(30),
            spacing=dp(20),
        )
        self.flow.bind(minimum_height=self.flow.setter("height"))
        self.scroll.add_widget(self.flow)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def update_games(self, store_name, stores_df):
        self.title_label.text = store_name
        self.flow.clear_widgets()

        urls_list = stores_df.loc[stores_df["stores"] == store_name, "urls"].values[0]
        if not urls_list:
            self.flow.add_widget(
                MDLabel(
                    text="No games found",
                    halign="center",
                    size_hint=(1, None),
                    height=dp(40),
                )
            )
            return

        card_size = Window.width * 0.42
        for url in urls_list:
            label_text = "Lorem Ipsum" #games.get_text_from_the_game_URL(url)
            '''
            Nyeremmény
            Feltétel első mondata (vásárolj ezt azt)
            Játék kezdete - Befejezése --> Sorsolás dátuma
            '''
            card = MDCard(
                orientation="horizontal",
                size_hint=(1, None),
                height=card_size * 0.9,
                padding=dp(20),
                radius=[12],
                elevation=4,
            )
            card.add_widget(
                MDLabel(text=label_text, halign="center", valign="middle", font_size=card_size * 0.13)
            )
            card.bind(on_release=lambda _, u=url: webbrowser.open(BASE_URL + u))
            self.flow.add_widget(card)
