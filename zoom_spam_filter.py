import os
import json
import time
import requests
from dotenv import load_dotenv
from spam_filter import detect_spam, log_spam, notify_discord

# Load environment variables
load_dotenv()
ZOOM_API_KEY = os.getenv("ZOOM_API_KEY")
ZOOM_API_SECRET = os.getenv("ZOOM_API_SECRET")
ZOOM_MEETING_ID = os.getenv("ZOOM_MEETING_ID")

ZOOM_API_BASE = "https://api.zoom.us/v2"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {ZOOM_API_KEY}",
    "Content-Type": "application/json"
}


def get_chat_messages():
    """Fetch recent chat messages from Zoom API."""
    url = f"{ZOOM_API_BASE}/meetings/{ZOOM_MEETING_ID}/chat/messages"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("messages", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Zoom messages: {e}")
        return []


def kick_user(user_id):
    """Remove a user from the Zoom meeting."""
    url = f"{ZOOM_API_BASE}/meetings/{ZOOM_MEETING_ID}/participants/{user_id}/remove"
    try:
        response = requests.delete(url, headers=HEADERS)
        if response.status_code == 204:
            print(f"✅ User {user_id} removed from Zoom meeting.")
        else:
            print(f"❌ Failed to remove user: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error kicking user: {e}")


def monitor_zoom_chat():
    """Continuously monitor Zoom chat for spam."""
    print("🚀 Monitoring Zoom chat for spam...")
    checked_messages = set()

    while True:
        messages = get_chat_messages()

        for message in messages:
            msg_id = message.get("id")
            user = message.get("sender", "Unknown")
            text = message.get("message", "")

            if msg_id not in checked_messages:
                checked_messages.add(msg_id)

                if detect_spam(user, text):
                    print(f"🚨 Spam detected from {user}: {text}")
                    log_spam(user, text)
                    notify_discord(user, text)

        time.sleep(5)  # Poll every 5 seconds


if __name__ == "__main__":
    monitor_zoom_chat()
