import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

class TelegramTool:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, text, parse_mode=None):
        if not self.token or not self.chat_id:
            return

        # Clean text to avoid common parsing errors if no parse_mode is specified
        # or if we want to be safe. For now, let's just use plain text if HTML fails
        # or use a very basic escaping.

        payload = {
            "chat_id": self.chat_id,
            "text": text,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"Telegram Message Sent: {text[:50].replace('\n', ' ')}...")
            else:
                # If Markdown/HTML fails, try sending as plain text
                if parse_mode:
                    print(f"Telegram {parse_mode} failed, retrying as plain text...")
                    del payload["parse_mode"]
                    response = requests.post(self.base_url, json=payload, timeout=10)
                    if response.status_code == 200:
                        print("Telegram Message Sent (Plain Text).")
                        return
                print(f"Telegram API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Telegram Connection Error: {e}")

    def notify_request(self, type, prompt):
        msg = f"🚀 PERMINTAAN LLM: {type}\n\n"
        msg += f"{prompt[:500]}..."
        self.send_message(msg)

    def notify_response(self, type, response):
        msg = f"✅ RESPON LLM: {type}\n\n"
        msg += f"{response[:500]}..."
        self.send_message(msg)


messenger = TelegramTool()
