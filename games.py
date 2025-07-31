import requests
import pandas as pd
import re

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

    game_desc_list = []
    for card in soup.select(".box.bg-light.main-box"):

        # — TITLE (strip off the "Lidl - " prefix if present)
        full_title = card.select_one("h1").get_text(strip=True)
        if " - " in full_title:
            title = full_title.split(" - ", 1)[1]
        else:
            title = full_title
        

        # — CONDITION (first <p> immediately after the <b>Feltétel:</b>)
        feltetel_b = card.find("b", string=re.compile(r"Feltétel", re.IGNORECASE))
        #condition = feltetel_b.find_next_sibling("p").get_text(strip=True)
        row_div = feltetel_b.parent.parent
        ps = row_div.find_all("p")
        condition = ps[0].get_text(strip=True)

        # — DATES
        dates = {}
        for tr in card.select("table.row tr"):
            label = tr.select_one("b").get_text(strip=True).rstrip(":")
            date_text = tr.select_one("span").get_text(strip=True)
            if label == "Kezdete":
                dates["start"] = date_text
            elif label == "Befejezés":
                dates["end"] = date_text
            elif label == "Sorsolás":
                dates["draw"] = date_text

        # — PRIZE (all <p> siblings after the <b>Nyeremény:</b>)
        prize = []
        prize_b = card.find("b", string=re.compile(r"Nyeremény", re.IGNORECASE))
        container_div = prize_b.parent.parent
        for p in container_div.find_all("p"):
            text = p.get_text(strip=True)
            prize.append(text)

        game_desc_list.append({
            "title": title,
            "condition": condition,
            "dates": dates,
            "prize": prize
        })

    game_desc_df = pd.DataFrame(game_desc_list)

    return game_desc_df