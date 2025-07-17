import requests
import pandas as pd  # <-- Add this import

from my_logging import logging
from bs4 import BeautifulSoup
from datetime import datetime


# Base URL of the site
BASE_URL = "https://www.webnyeremeny.hu/"

def save_raw_html(soup: BeautifulSoup) -> None:
    """
    Save the raw HTML content of the soup object to a file.
    """
    with open("webnyeremeny_html_output.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def fetch_contests():
    """
    Scrape the homepage for active contests and return a DataFrame of contest data.
    Each row contains: title, games, urls (list), prize, deadline, image_url, rules_url
    """
    resp = requests.get(BASE_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    #save_raw_html(soup)  # Save the raw HTML for debugging

    contests = []
    for card in soup.select(".category-box"):  # adjust this selector
        title = card.select_one("h1").get_text(strip=True)
        games = card.select_one(".category-list").get_text(strip=True, separator=", ")
        urls = [a["href"] for a in card.select(".category-list a")]
        # Uncomment and adjust the following as needed
        # prize = card.select_one(".contest-prize").get_text(strip=True) if card.select_one(".contest-prize") else None
        # img_tag = card.select_one("img")
        # image_url = img_tag["src"] if img_tag else None
        # rules_anchor = card.select_one("a.rules-link")
        # rules_url = rules_anchor["href"] if rules_anchor else None

        contests.append({
            "title": title,
            "games": games,
            "urls": urls,
            # "prize": prize,
            # "deadline": deadline,
            # "image_url": image_url,
            # "rules_url": rules_url,
        })

    stores_df = pd.DataFrame(contests)
    stores_df = stores_df[stores_df["title"] == "Üzletekhez kötődő"]
    stores_df = stores_df["games"].apply(lambda x: x.split(", ")).explode().reset_index(drop=True)
    print(stores_df)
    '''
    for i in stores_df.iterrows():
        if i[1]["title"] == "Üzletekhez kötődő":
            print(i[1]["games"])
    '''

def get_webnyeremeny_html() -> str:
    """ 
    Get the raw HTML content of the webnyeremeny.hu homepage.
    This function reads from a saved HTML file for debugging purposes.
    """
    with open("webnyeremeny_html_output.txt", "r", encoding="utf-8") as infile:
        soup = infile.read()
    return soup

def collect_contests(soup: BeautifulSoup) -> pd.DataFrame:
    """ 
    Collect stores from the raw HTML content and return a DataFrame. 
    """
    contests_list = []
    for card in soup.select(".category-box"):
        title = card.select_one("h1").get_text(strip=True)
        games = card.select_one(".category-list").get_text(strip=True, separator=", ")
        urls = [a["href"] for a in card.select(".category-list a")]
        contests_list.append({
            "title": title,
            "games": games,
            "urls": urls
        })

    return pd.DataFrame(contests_list)

def save_dataframe_as_excel(df: pd.DataFrame, filename: str, ) -> None:
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    logging.info("__App Started__")

    webnyeremeny_raw_html = get_webnyeremeny_html()
    soup = BeautifulSoup(webnyeremeny_raw_html, "html.parser")
    contests_df = collect_contests(soup)
    save_dataframe_as_excel(contests_df, "contests.xlsx")   


    logging.info("__App Finished__")