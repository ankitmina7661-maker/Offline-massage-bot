
import requests
import time
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_NEW_BOT_TOKEN")

TARGET_CHAT_ID = 8485299821

API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

REPLY_FILE = "reply.json"
waiting_for_reply = False
offset = 0


def save_reply(message):
    with open(REPLY_FILE, "w", encoding="utf-8") as f:
        json.dump({"reply": message}, f, ensure_ascii=False)


def load_reply():
    try:
        with open(REPLY_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("reply", "🥱🥱")
    except:
        return "🥱🥱"


def send_message(chat_id, message):
    requests.post(
        API + "sendMessage",
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=15
    )


print("Auto Reply Bot Started 🥱🥱")

while True:
    try:
        data = requests.get(
            API + "getUpdates",
            params={"offset": offset, "timeout": 30},
            timeout=35
        ).json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message", {})
            chat = message.get("chat", {})
            text = message.get("text", "")

            if chat.get("type") != "private":
                continue

            if chat.get("id") != TARGET_CHAT_ID or not text:
                continue

            if text == "/setdm":
                waiting_for_reply = True
                send_message(
                    TARGET_CHAT_ID,
                    "✍️ Send your new auto reply message."
                )
                continue

            if waiting_for_reply:
                save_reply(text)
                waiting_for_reply = False

                send_message(
                    TARGET_CHAT_ID,
                    "✅ Your auto reply has been saved!"
                )
                continue

            send_message(TARGET_CHAT_ID, load_reply())

    except Exception as e:
        print("Error:", e)
        time.sleep(3)
