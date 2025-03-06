import re
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🚨 Basic regex patterns for common spam
SPAM_PATTERNS = [
    r"(free money|get rich quick|click here|make $[0-9]+ fast)",  # Scam phrases
    r"https?://\S+",  # Links
    r"(buy followers|boost your views|pay for likes)",  # Social media scams
    r"([A-Za-z0-9])\1{5,}",  # Repeated characters (e.g., "heeeelloooooo")
    r"(.)\1{10,}",  # Excessive repetition (e.g., "!!!!!!!!!!!")
]

def is_spam_regex(message):
    """Checks message against predefined regex patterns."""
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in SPAM_PATTERNS)

def ai_spam_detection(message):
    """Uses OpenAI API to determine if a message is spam."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Determine if the following message is spam: " + message}],
            temperature=0
        )
        result = response["choices"][0]["message"]["content"].lower()
        return "spam" in result
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return False  # Fail-safe: assume it's not spam

def detect_spam(message):
    """Main spam detection function."""
    regex_spam = is_spam_regex(message)
    ai_spam = ai_spam_detection(message)

    # Scoring system: Regex spam is strong indicator; AI adds additional validation
    spam_score = 0
    if regex_spam:
        spam_score += 1
    if ai_spam:
        spam_score += 2  # AI detection is weighted higher

    return spam_score > 1  # Returns True if high spam confidence

# 🔥 Test the spam filter
if __name__ == "__main__":
    test_messages = [
        "Make $10,000 in a week! Click here: http://scam.com",
        "Hey, how are you?",
        "Folllllooooow me for more"]
