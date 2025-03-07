import tldextract

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
