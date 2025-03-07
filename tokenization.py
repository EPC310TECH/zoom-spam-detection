import re

def tokenize_message(message):
    """Split message into individual tokens (words, numbers, links, etc.)."""
    return re.findall(r"\b\w+\b", message)

spam_tokens = set()
for msg in spam_messages:
    spam_tokens.update(tokenize_message(msg))
