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
