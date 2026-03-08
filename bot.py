import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

# store previous favorites
previous_odds = {}

# prevent duplicate alerts
sent_alerts = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Favorite Flip Bot Running!")


async def scan_matches(context: ContextTypes.DEFAULT_TYPE):
    print("Scanning matches...")

    sports = [
        "soccer_epl",
        "soccer_spain_la_liga",
        "soccer_germany_bundesliga",
        "soccer_italy_serie_a",
        "soccer_france_ligue_one"
    ]

    for sport in sports:

        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "eu",
            "markets": "h2h"
        }

        try:
            r = requests.get(url, params=params)

            if r.status_code != 200:
                print("API error:", r.status_code)
                continue

            games = r.json()

            print(f"{sport}: {len(games)} matches found")

            for game in games:

                home = game["home_team"]
                away = game["away_team"]

                match_id = f"{sport}-{home}-{away}"

                bookmakers = game.get("bookmakers", [])

                if not bookmakers:
                    continue

                markets = bookmakers[0].get("markets", [])

                if not markets:
                    continue

                outcomes = markets[0].get("outcomes", [])

                odds = {o["name"]: o["price"] for o in outcomes}

                if home not in odds or away not in odds:
                    continue

                home_odds = odds[home]
                away_odds = odds[away]

                current_favorite = home if home_odds < away_odds else away

                if match_id not in previous_odds:
                    previous_odds[match_id] = current_favorite
                    continue

                previous_favorite = previous_odds[match_id]

                # detect favorite flip
                if previous_favorite != current_favorite:

                    alert_id = f"{match_id}-{current_favorite}"

                    if alert_id not in sent_alerts:

                        message = f"""
🔥 FAVORITE FLIP DETECTED

Sport: {sport.upper()}
Match: {home} vs {away}

Old Favorite: {previous_favorite}
New Favorite: {current_favorite}

Odds:
{home}: {home_odds}
{away}: {away_odds}
"""

                        await context.bot.send_message(
                            chat_id=CHAT_ID,
                            text=message
                        )

                        sent_alerts.add(alert_id)

                previous_odds[match_id] = current_favorite

        except Exception as e:
            print("Scanner error:", e)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    job_queue = app.job_queue
    job_queue.run_repeating(scan_matches, interval=60, first=10)

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
