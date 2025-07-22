import requests
import pandas as pd

from bs4 import BeautifulSoup


# Base URL of the site
BASE_URL = "https://www.webnyeremeny.hu/"

def save_raw_html(soup: BeautifulSoup) -> None:
    """
    Save the raw HTML content of the soup object to a file.
    """
    with open("webnyeremeny_html_output.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def save_dataframe_as_csv(df: pd.DataFrame, filename: str, ) -> None:
    df.to_csv(filename, index=False)

def collect_contests(soup: BeautifulSoup) -> pd.DataFrame:
    """ 
    Collect stores from webnyeremeny HTML content and return a DataFrame. 
    """
    contests_list = []
    for card in soup.select(".category-box"):
        title = card.select_one("h1").get_text(strip=True)
        games = card.select_one(".category-list").get_text(strip=True, separator=", ")
        games = games.replace(", (új)", " (új)")
        urls = [a["href"] for a in card.select(".category-list a")]
        contests_list.append({
            "title": title,
            "games": games,
            "urls": urls
        })

    return pd.DataFrame(contests_list)

def get_all_contest_online() -> pd.DataFrame:
    """
    Scrape the homepage for active contests and return a DataFrame of contest data.
    """
    resp = requests.get(BASE_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    #save_raw_html(soup)  # Save the raw HTML for debugging
    contests_df = collect_contests(soup)
    #save_dataframe_as_csv(contests_df, "contests.csv")

    return pd.DataFrame(contests_df)

def get_all_contest_offline() -> pd.DataFrame:
    '''
    This function reads the HTML content from a file instead of making a live request.
    '''
    with open("webnyeremeny_html_output.txt", "r", encoding="utf-8") as infile:
        webnyeremeny_raw_html = infile.read()
    soup = BeautifulSoup(webnyeremeny_raw_html, "html.parser")

    contests_df = collect_contests(soup)
    save_dataframe_as_csv(contests_df, "contests.csv")

    return contests_df