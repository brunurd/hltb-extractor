import re
import sys
import json
import csv
import datetime
from time import time
from urllib.parse import quote
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .config import MAX_GET_DATA_ATTEMPTS, WAIT_FOR_SECONDS_IN_SELENIUM_SELECT


def search_in_hltb(term):
    start = time()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://howlongtobeat.com/?q={quote(term)}")
    wait = WebDriverWait(driver, WAIT_FOR_SECONDS_IN_SELENIUM_SELECT)
    first_game_card = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "back_darkish")))
    data = {
        "Title": "",
        "Main Story": "",
        "Main + Extra": "",
        "Completionist": ""
    }
    if match := re.search(
        f"^(.*{term}.*)\\n(.*)",
        first_game_card.text,
        re.IGNORECASE | re.MULTILINE
    ):
        groups = match.groups()
        data["Title"] = groups[0]
        values_regex = r"Main Story(.*) HoursMain \+ " + \
                       r"Extra(.*) HoursCompletionist(.*) Hours"
        values = groups[1]
        if values_match := re.search(
            values_regex,
            values,
            re.IGNORECASE | re.MULTILINE
        ):
            values_groups = values_match.groups()
            data["Main Story"] = values_groups[0]
            data["Main + Extra"] = values_groups[1]
            data["Completionist"] = values_groups[2]
    driver.quit()
    end = time()
    execution_time = end - start
    return (data, execution_time)


def recursive_search(game_title, index=1, tries=MAX_GET_DATA_ATTEMPTS):
    print(f"Attempt {index} to get the \"{game_title}\" game data...")
    game_data, execution_time = search_in_hltb(game_title)
    print(f"Elapsed time: {execution_time}")
    if game_data["Title"] == "" and index < tries:
        return recursive_search(game_title, index+1, tries)
    else:
        return game_data


def get_games_data(game_titles):
    games = []
    for game_title in game_titles:
        print(f"Searching for \"{game_title}\"...")
        game_data = recursive_search(game_title)
        print(json.dumps(game_data, indent=4))
        games.append(game_data)
    table_headers = ["Title", "Main Story", "Main + Extra", "Completionist"]
    table_data = []
    for game in games:
        table_data.append([
            game["Title"],
            game["Main Story"],
            game["Main + Extra"],
            game["Completionist"]
        ])
    print(tabulate(table_data, headers=table_headers))
    now = datetime.datetime.now()
    timestamp = int(now.timestamp())
    with open(f"out/{timestamp}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(table_headers)
        writer.writerows(table_data)


def start():
    get_games_data(game_titles=sys.argv[1:])
