import requests
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

async def scan_matches(context: ContextTypes.DEFAULT_TYPE):
    print("Scanning matches...")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    while True:
        await scan_matches(None)
        time.sleep(60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
