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
    with open("raw_html_output.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def parse_deadline(date_str: str) -> datetime:
    """
    Parse a Hungarian-style deadline string like '2025. 07. 15.' into a datetime object.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        # Fallback: try without trailing dot
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")


def fetch_contests() -> pd.DataFrame:
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
        # deadline_str = card.select_one(".contest-deadline").get_text(strip=True) if card.select_one(".contest-deadline") else None
        # deadline = parse_deadline(deadline_str) if deadline_str else None
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

    df = pd.DataFrame(contests)
    return df

if __name__ == "__main__":
    logging.info("__Starting the App__")
    contests_df = fetch_contests()
    stores_df = contests_df[contests_df["title"] == "Üzletekhez kötődő"]
    stores_df = stores_df["games"].apply(lambda x: x.split(", ")).explode().reset_index(drop=True)
    print(stores_df)
    """
    for i in contests_df.iterrows():
        if i[1]["title"] == "Üzletekhez kötődő":
            print(i[1]["games"])
    """