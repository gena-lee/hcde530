import csv


# I used DictReader so each column name becomes a key.
# That makes the loop below easier to read.
filename = "demo_responses.csv"
responses = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        responses.append(row)


def count_words(response):
    """Count the number of words in a response string.

    Takes a string, splits it on whitespace, and returns the word count.
    Used to measure response length across all participants.
    """
    return len(response.split())


# I print a compact table first so I can quickly scan for outliers
# before looking at aggregate stats.
print(f"{'ID':<6} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
print("-" * 75)

word_counts = []

# This single pass balances clarity and efficiency:
# compute metrics and prepare readable output at the same time.
for row in responses:
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    # Helper function keeps counting behavior consistent everywhere.
    count = count_words(response)
   # Add the word count to the word_counts list
    word_counts.append(count)

    # Truncate the response preview for display
    if len(response) > 60:
        preview = response[:60] + "..."
    else:
        preview = response

    # Fixed-width formatting makes it easy to compare rows visually.
    print(f"{participant:<6} {role:<22} {count:<6} {preview}")

# Summary is separated from row output so the script supports
# both detailed inspection (top section) and quick takeaway (bottom section).
print()
print("── Summary ─────────────────────────────────")
# I include count + min/max/avg as a minimal descriptive snapshot.
print(f"  Total responses : {len(word_counts)}")
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
