import os
import requests
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=BOT_TOKEN)

# store already sent matches
sent_matches = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Betting bot is running!")


async def scan_matches(context: ContextTypes.DEFAULT_TYPE):
    print("Scanning matches...")

    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("API error:", response.status_code)
            return

        games = response.json()

        for game in games:
            home = game["home_team"]
            away = game["away_team"]

            match_id = f"{home}-{away}"

            # skip if already sent
            if match_id in sent_matches:
                continue

            message = f"⚽ Match Found\n{home} vs {away}"

            await bot.send_message(chat_id=CHAT_ID, text=message)

            # remember this match
            sent_matches.add(match_id)

    except Exception as e:
        print("Scanner error:", e)


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    job_queue = app.job_queue
    job_queue.run_repeating(scan_matches, interval=300, first=10)

    print("Bot started")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
