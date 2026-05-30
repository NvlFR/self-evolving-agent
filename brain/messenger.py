import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

class TelegramTool:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, text, parse_mode="Markdown"):
        if not self.token or not self.chat_id:
            return
            
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        try:
            requests.post(self.base_url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram Error: {e}")

    def notify_request(self, type, prompt):
        msg = f"🚀 *PERMINTAAN LLM: {type}*\n\n"
        msg += f"```\n{prompt[:500]}...\n```"
        self.send_message(msg)

    def notify_response(self, type, response):
        msg = f"✅ *RESPON LLM: {type}*\n\n"
        msg += f"```\n{response[:500]}...\n```"
        self.send_message(msg)

messenger = TelegramTool()
