import requests
import pandas as pd

from bs4 import BeautifulSoup

# Base URL of the site
BASE_URL = "https://www.webnyeremeny.hu/"

def get_game_description_online(url):
    """
    Scrape the homepage for active contests and return a DataFrame of contest data.
    """
    resp = requests.get(BASE_URL + url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    """ Save the raw HTML content for debugging purposes.
    with open("game_desc.txt", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    """
    return soup

def get_game_description_offline():
    """
    Read the HTML content from a file instead of making a live request.
    """
    with open("game_desc.txt", "r", encoding="utf-8") as infile:
        game_html = infile.read()
    soup = BeautifulSoup(game_html, "html.parser")

    return soup

def get_game_description(url):
    """
    Get the text from the game URL, either online or offline.
    """

    #soup = get_game_description_online(url)
    soup = get_game_description_offline()

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

    return "asdqwe"