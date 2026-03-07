import os
import time
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

previous_favorites = {}

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


# -------------------------
# FLASHScore LIVE MATCHES
# -------------------------

def get_flashscore_matches():

    url = "https://www.flashscore.in/"

    r = requests.get(url)

    soup = BeautifulSoup(r.text,"html.parser")

    matches = []

    games = soup.find_all("div",class_="event__match")

    for g in games:

        try:

            team1 = g.find("div",class_="event__participant--home").text
            team2 = g.find("div",class_="event__participant--away").text

            match = f"{team1} vs {team2}"

            matches.append(match)

        except:
            continue

    return matches


# -------------------------
# REDDYBOOK ODDS
# -------------------------

def get_reddybook_odds():

    url = "https://reddybook.green"

    r = requests.get(url)

    soup = BeautifulSoup(r.text,"html.parser")

    odds_data = {}

    # example structure
    matches = soup.find_all("div",class_="match")

    for m in matches:

        try:

            team1 = m.find("span",class_="team1").text
            team2 = m.find("span",class_="team2").text

            odd1 = float(m.find("span",class_="odd1").text)
            odd2 = float(m.find("span",class_="odd2").text)

            match = f"{team1} vs {team2}"

            odds_data[match] = {
                team1: odd1,
                team2: odd2
            }

        except:
            continue

    return odds_data


# -------------------------
# FIND FAVORITE
# -------------------------

def get_favorite(odds):

    fav = None
    fav_odds = 999

    for team,odd in odds.items():

        if odd < fav_odds:

            fav = team
            fav_odds = odd

    return fav,fav_odds


# -------------------------
# MONITOR
# -------------------------

def monitor():

    flash_matches = get_flashscore_matches()

    reddy_odds = get_reddybook_odds()

    for match in flash_matches:

        if match not in reddy_odds:
            continue

        odds = reddy_odds[match]

        fav,fav_odds = get_favorite(odds)

        if fav_odds >= 2:
            continue

        if match not in previous_favorites:

            previous_favorites[match] = fav
            continue

        if previous_favorites[match] != fav:

            message = f"""
⚠️ FAVORITE LOST

Match:
{match}

Old Favorite:
{previous_favorites[match]}

New Favorite:
{fav}
"""

            send_message(message)

            previous_favorites[match] = fav


# -------------------------
# LOOP
# -------------------------

while True:

    try:

        monitor()

        time.sleep(30)

    except Exception as e:

        print(e)

        time.sleep(60)
