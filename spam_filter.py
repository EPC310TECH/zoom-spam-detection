import re
import openai
import os
import json
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load spam patterns from external file
def load_spam_patterns(file_path="spam_patterns.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Warning: Spam patterns file not found! Using default patterns.")
        return []

SPAM_PATTERNS = load_spam_patterns()

# 🔍 User spam tracking
user_spam_count = defaultdict(int)

def is_spam_regex(message):
    """Check message against regex patterns."""
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in SPAM_PATTERNS)

def ai_spam_detection(message):
    """Use OpenAI API to analyze spam content."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Identify if the message is spam and return 'spam' or 'not spam'."},
                {"role": "user", "content": message}
            ],
            temperature=0
        )
        return "spam" in response["choices"][0]["message"]["content"].lower()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return False




# Modify detect_spam() in spam_filter.py
def detect_spam(user, message):
    """Detect spam & enforce penalties."""
    regex_spam = is_spam_regex(message)
    ai_spam = ai_spam_detection(message)

    spam_score = 1 * regex_spam + 2 * ai_spam
    if spam_score > 1:
        user_spam_count[user] += 1
        log_spam(user, message)
        notify_discord(user, message)

        if user_spam_count[user] >= 3:  # 🚨 Kick user after 3 spam messages
            kick_user(user)

    return spam_score > 1


def log_spam(user, message):
    """Log spam messages for review."""
    log_entry = {"timestamp": str(datetime.now()), "user": user, "message": message}
    with open("spam_log.json", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

# 🔥 Test with sample messages
if __name__ == "__main__":
    test_messages = {
        "user1": "Win win win win win! Click here: http://scam.com",
        "user2": "Hello everyone, how’s your day?",
        "user3": "Folllllooooow me for more content!!!",
        "user4": "Join my investment group and double your money!",
        "user5": "This is a normal message with no spam.",
        "user6": "Free money $$$$ just visit this link: http://scam.net"
    }

    for user, msg in test_messages.items():
        print(f"User: {user} | Message: {msg}\nSpam: {detect_spam(user, msg)}\n{'-'*40}")
