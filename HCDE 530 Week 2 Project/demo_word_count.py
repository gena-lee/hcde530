import csv


# Load the CSV file
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


# Count words in each response and print a row-by-row summary
print(f"{'ID':<6} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
print("-" * 75)

word_counts = []

# Loop through each row in the responses list
for row in responses:
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    # Call our function to count words in this response
    count = count_words(response)
   # Add the word count to the word_counts list
    word_counts.append(count)

    # Truncate the response preview for display
    if len(response) > 60:
        preview = response[:60] + "..."
    else:
        preview = response

    # Print the participant ID, role, word count, and response preview
    print(f"{participant:<6} {role:<22} {count:<6} {preview}")

# Print summary statistics
print()
print("── Summary ─────────────────────────────────")
# Print the total number of responses
print(f"  Total responses : {len(word_counts)}")
# Print the shortest response
print(f"  Shortest        : {min(word_counts)} words")
# Print the longest response
print(f"  Longest         : {max(word_counts)} words")
# Print the average response length
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
