import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import string
import sqlalchemy
from sqlalchemy import create_engine

# base url for the statistics website
base_url = "https://www.baseball-reference.com"

def scrape_player_links_by_letter(letter: str) -> list:
    '''
    Scrape player names and URLs from the Baseball Reference players page for a given letter.
    
    Args:
        letter (str): The letter players' last names start with.
    Returns:
        list: A list of dcitionaries with the keys "name" and "url" corresponding to each player and their page with career stats.
    '''
    # create full url for player page based on first letter of last name
    players_url = f"{base_url}/players/{letter}/"
    # use requests to retrieve content from url
    players_page = requests.get(players_url)
    # use beautiful soup to parse html
    soup = BeautifulSoup(players_page.content, 'html.parser')
    # find the div with id 'div_players_'
    section_content = soup.find('div', id='div_players_')
    
    # find all player links within this div
    player_links = section_content.find_all('a')
    
    # create empty list to store dictionaries of player name and url
    players_data = []
    # loop through links and pull out data
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
        print(f"Scraping players starting with letter: {letter}")
        p_dat = scrape_player_links_by_letter(letter)
        print(f"Letter {letter} has {len(p_dat)} players.")
        all_players_data.append(p_dat)
        print(f"All players from letter {letter} added.")
        time.sleep(5)  # Be polite and don't overload the server
    print(f"Total number of players: {len(all_players_data)}")
    return pd.DataFrame(all_players_data)


if __name__ == "__main__":
    df = scrape_all_player_links()
