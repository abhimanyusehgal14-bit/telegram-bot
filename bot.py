import requests
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
ODDS_API_KEY = "YOUR_ODDS_API_KEY"

bot = Bot(token=BOT_TOKEN)


def start(update, context):
    update.message.reply_text("✅ Bot running and monitoring odds")


def check_odds():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        for match in data:
            teams = match["teams"]
            odds = match["bookmakers"][0]["markets"][0]["outcomes"]

            for outcome in odds:
                price = outcome["price"]

                if price < 2:
                    print("Favorite detected:", outcome["name"], price)

    except Exception as e:
        print("Error:", e)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    print("Bot started")

    while True:
        check_odds()
        time.sleep(60)


if __name__ == "__main__":
    main()
