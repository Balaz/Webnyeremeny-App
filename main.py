import contests
from screen_modules import *
import screen_stores, screen_store_games

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class ScreenMain(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        appbar = MDTopAppBar(
            MDTopAppBarTitle(text="Webnyeremény"),
            type="small",
        )
        root.add_widget(appbar)

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

class WebnyeremenyApp(MDApp):
    def build(self):
        self.title = "Webnyeremény"
        contests_df = contests.collect_contests()

        sm = ScreenManager()
        sm.add_widget(ScreenMain(name="main"))
        sm.add_widget(screen_stores.ScreenStores(contests_df, name="stores"))
        sm.add_widget(screen_store_games.ScreenGame(name="store_games"))
        return sm

if __name__ == "__main__":
    WebnyeremenyApp().run()
