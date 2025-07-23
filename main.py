from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDTopAppBarTitle,
    MDActionTopAppBarButton,
)
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout

import webbrowser
import os

import get_contests
import stores

BASE_URL = "https://www.webnyeremeny.hu"


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        # Top App Bar
        appbar = MDTopAppBar(
            MDTopAppBarTitle(text="Webnyeremény"),
            type="small",
        )
        root.add_widget(appbar)

        # Center bubble
        content = FloatLayout()
        bubble = MDCard(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            radius=[dp(60)] * 4,
            ripple_behavior=True,
            elevation=6,
            orientation="vertical",
        )
        bubble.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        bubble.add_widget(
            MDLabel(text="Store Games", halign="center", valign="center")
        )
        bubble.bind(on_release=lambda *_: setattr(self.manager, "current", "stores"))
        content.add_widget(bubble)

        root.add_widget(content)
        self.add_widget(root)


class StoresScreen(MDScreen):
    def __init__(self, stores_df, **kwargs):
        super().__init__(**kwargs)
        self.stores_df = stores_df

        root = BoxLayout(orientation="vertical")

        # Top App Bar with back button
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
        flow = MDStackLayout(
            adaptive_height=True,
            padding=dp(10),
            spacing=dp(10),
        )

        for store in sorted(self.stores_df["stores"]):
            card = MDCard(
                size_hint=(None, None),
                size=(dp(120), dp(120)),
                radius=[dp(60)] * 4,
                ripple_behavior=True,
                elevation=6,
                orientation="vertical",
            )
            logo_path = f"assets/logos/{store.lower()}.png"
            if not os.path.exists(logo_path):
                logo_path = "assets/logos/placeholder.png"
            card.add_widget(FitImage(source=logo_path, size_hint=(1, 0.7)))
            card.add_widget(MDLabel(text=store, halign="center", size_hint=(1, 0.3)))
            card.bind(on_release=lambda _, s=store: self._open_store(s))
            flow.add_widget(card)

        scroll.add_widget(flow)
        root.add_widget(scroll)
        self.add_widget(root)

    def _open_store(self, store_name):
        urls_screen = self.manager.get_screen("urls")
        urls_screen.update_urls(store_name, self.stores_df)
        self.manager.current = "urls"


class URLsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        # Dynamic title for App Bar
        self.title_label = MDTopAppBarTitle(text="")

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
            padding=dp(10),
            spacing=dp(10),
        )
        self.scroll.add_widget(self.flow)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def update_urls(self, store_name, stores_df):
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

        for url in urls_list:
            card = MDCard(
                size_hint=(None, None),
                size=(dp(120), dp(120)),
                radius=[dp(60)] * 4,
                ripple_behavior=True,
                elevation=6,
                orientation="vertical",
            )
            label_text = url.strip("/").replace("-", " ").capitalize()
            card.add_widget(
                MDLabel(text=label_text, halign="center", valign="middle")
            )
            card.bind(on_release=lambda _, u=url: webbrowser.open(BASE_URL + u))
            self.flow.add_widget(card)


class WebnyeremenyApp(MDApp):
    def build(self):
        self.title = "Webnyeremény"
        contests_df = get_contests.get_all_contest_offline()
        stores_df = stores.get_all_store_games(contests_df)

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(StoresScreen(stores_df, name="stores"))
        sm.add_widget(URLsScreen(name="urls"))
        return sm


if __name__ == "__main__":
    WebnyeremenyApp().run()
