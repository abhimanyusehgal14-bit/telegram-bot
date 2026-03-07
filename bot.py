import os
import requests
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=BOT_TOKEN)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Betting bot is running!")


# match scanner
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

        for game in games[:3]:  # just test with first 3 matches
            home = game["home_team"]
            away = game["away_team"]

            message = f"⚽ Match Found\n{home} vs {away}"

            await bot.send_message(chat_id=CHAT_ID, text=message)

    except Exception as e:
        print("Scanner error:", e)


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # command handler
    app.add_handler(CommandHandler("start", start))

    # job queue scanner
    job_queue = app.job_queue
    job_queue.run_repeating(scan_matches, interval=60, first=10)

    print("Bot started successfully")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
