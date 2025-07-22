from my_logging import logging
import get_contests
import stores

if __name__ == "__main__":
    logging.info("__App Started__")

    contests_df = get_contests.get_all_contest_offline()
    stores_df = stores.get_all_store_games(contests_df)

    print(stores_df)

    logging.info("__App Finished__")