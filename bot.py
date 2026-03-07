import asyncio
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

async def scan_matches():
    while True:
        print("Scanning matches...")
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # start background scanner
    asyncio.create_task(scan_matches())

    print("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
