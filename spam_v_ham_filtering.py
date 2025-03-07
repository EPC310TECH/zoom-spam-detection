import re
import tldextract
from collections import defaultdict
import json

def tokenize_message(message):
    """Split message into individual tokens (words, numbers, links, etc.)."""
    return re.findall(r"\b\w+\b", message)

spam_tokens = set()
for msg in spam_messages:
    spam_tokens.update(tokenize_message(msg))



def generate_regex(token):
    """Convert tokens into regex patterns based on predefined transformation rules."""
    if token.isdigit():  
        return r"\d+"  # Numbers → \d+
    if re.fullmatch(r"[A-F0-9]+", token):  
        return r"[A-F0-9]+"  # Capital Hex → [A-F0-9]+
    if re.fullmatch(r"[a-f0-9]+", token):  
        return r"[a-f0-9]+"  # Lowercase Hex → [a-f0-9]+
    
    # Check if it's a common TLD
    extracted = tldextract.extract(token)
    if extracted.suffix in ["com", "net", "org", "edu", "biz", "info", "us"]:
        return r"(com|net|org|edu|biz|info|us)"

    if token.islower():  
        return r"[a-z]+"  # Lowercase word → [a-z]+
    if token.isupper():  
        return r"[A-Z]+"  # Uppercase word → [A-Z]+
    if token[:1].isupper() and token[1:].islower():  
        return r"[A-Z][a-z]+"  # Capitalized → [A-Z][a-z]+

    # Check for common days and months
    if token in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        return r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
    if token in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
        return r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

    return re.escape(token)  # Keep as literal regex otherwise

# Generate regex rules for spam tokens
regex_rules = {generate_regex(token) for token in spam_tokens}

from collections import defaultdict

# Count how many spam messages each regex matches
regex_match_count = defaultdict(int)

for regex in regex_rules:
    pattern = re.compile(regex)
    for msg in spam_messages:
        if pattern.search(msg):
            regex_match_count[regex] += 1

# Remove regex that only match 1 spam message
filtered_regex = {r for r, count in regex_match_count.items() if count > 1}

# Remove regex that match any ham message
for regex in list(filtered_regex):
    pattern = re.compile(regex)
    for msg in ham_messages:
        if pattern.search(msg):
            filtered_regex.remove(regex)
            break  # No need to check further once it matches a ham message

# Rank regex by how many spam messages they detect
ranked_regex = sorted(filtered_regex, key=lambda r: regex_match_count[r], reverse=True)


with open("spam_patterns.json", "w") as f:
    json.dump(ranked_regex, f, indent=4)

