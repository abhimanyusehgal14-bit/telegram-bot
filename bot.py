import requests
import time

BOT_TOKEN = "8759925431:AAGS8H3pdZ2krw_DyXpPrj1-F4RfCPAZ0x4"
CHAT_ID = "7948437238"

while True:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": "Bot running 🚀"}
    requests.post(url, data=data)
    time.sleep(60)
