import contests
import stores
import screens.main, screens.stores, screens.store_games

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

BASE_URL = "https://www.webnyeremeny.hu"

class WebnyeremenyApp(MDApp):
    def build(self):
        self.title = "Webnyeremény"
        contests_df = contests.get_all_contest_offline()
        stores_df = stores.get_all_store_games(contests_df)

        sm = ScreenManager()
        sm.add_widget(screens.main.MainScreen(name="main"))
        sm.add_widget(screens.stores.StoresScreen(stores_df, name="stores"))
        sm.add_widget(screens.store_games.URLsScreen(name="urls"))
        return sm


if __name__ == "__main__":
    WebnyeremenyApp().run()
