import os
import requests
from telegram import Bot
from telegram.ext import Application
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def scan_matches(context):
    print("Scanning matches...")

    try:
        # example API call placeholder
        url = "https://api.the-odds-api.com/v4/sports/soccer/odds"
        response = requests.get(url)

        if response.status_code == 200:
            print("API working")
        else:
            print("API error")

    except Exception as e:
        print("Scanner error:", e)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

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
