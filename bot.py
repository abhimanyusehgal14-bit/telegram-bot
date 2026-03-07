import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")


async def scan_matches(context: ContextTypes.DEFAULT_TYPE):
    print("Scanning matches...")


async def post_init(app):
    app.job_queue.run_repeating(scan_matches, interval=60, first=5)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
