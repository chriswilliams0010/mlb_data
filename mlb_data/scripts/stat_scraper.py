import sys
import os
import time
import string
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logs.logging_config import setup_logging

setup_logging()

# base url for the statistics website
base_url = "https://www.baseball-reference.com"

def scrape_player_links_by_letter(letter: str) -> list:
    '''
    Scrape player names and URLs from the Baseball Reference players page for a given letter.
    
    Args:
        letter (str): The letter players' last names start with.
    Returns:
        list: A list of dictionaries with the keys "name" and "url" corresponding to each player and their page with career stats.
    '''
    players_url = f"{base_url}/players/{letter}/"
    players_page = requests.get(players_url)
    soup = BeautifulSoup(players_page.content, 'html.parser')
    section_content = soup.find('div', id='div_players_')
    
    player_links = section_content.find_all('a')
    
    players_data = []
    for link in player_links:
        player_name = link.text.strip()
        player_url = base_url + link['href']
        players_data.append({'name': player_name, 'url': player_url})
        
    return players_data


def scrape_all_player_links() -> pd.DataFrame:
    '''
    Loop through all letters to run the scrape_player_links_by_letter() function.

    Returns: pandas.DataFrame: A DataFrame containing player names and URLs for all letters.
    '''
    all_players_data = []
    for letter in string.ascii_lowercase:
        logging.info(f"Scraping players starting with letter: {letter}")
        p_dat = scrape_player_links_by_letter(letter)
        logging.info(f"Letter {letter} has {len(p_dat)} players.")
        n += len(p_dat)
        all_players_data.extend(p_dat)
        logging.info(f"All players from letter {letter} added.")
        time.sleep(5)
    logging.info(f"Total number of players: {len(all_players_data)}")
    return pd.DataFrame(all_players_data)


if __name__ == "__main__":
    df = scrape_all_player_links()
