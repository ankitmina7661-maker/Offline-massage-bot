import requesimport requests
import time

BOT_TOKEN = "9227645405:AAE3vtGZZdqlW9f9eJ8Qw-QsZC-gh35Cv-w"

REPLY = """Hey! I am bot powered by Ankit

Ankit is currently offline for an indefinite period of time.
There is a very low chance that he will respond to your message anytime soon.
Please don't expect an immediate reply.
Thank you for your understanding! ❤️"""


API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

offset = 0
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

            if chat.get("type") == "private" and text:
                requests.post(
                    API + "sendMessage",
                    data={
                        "chat_id": chat["id"],
                        "text": REPLY
                    },
                    timeout=15
                )
                print("Reply sent 🥱🥱")

    except Exception as e:
        print("Error:", e)
        time.sleep(3)
