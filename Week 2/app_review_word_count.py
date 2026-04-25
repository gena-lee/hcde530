"""Count words in made-up app reviews and print summary stats."""


def count_words(text):
    """Return the number of words in a text string."""
    return len(text.split())


# I use an in-memory list to keep the demo self-contained and predictable.
# That makes it easier to focus on analysis flow before introducing CSV input.
reviews = [
    "Love the clean layout and quick loading speed.",
    "Great features, but the search filter still feels clunky.",
    "The onboarding steps were clear and easy to follow.",
    "I like the color palette, but notifications are too frequent.",
    "Fast app overall, though I hit one crash on profile edit.",
    "Navigation is intuitive and I found everything quickly.",
    "The new update fixed most of my previous issues.",
    "I wish dark mode had stronger contrast for readability.",
    "Account setup was smooth and took less than a minute.",
    "The app is helpful, but offline mode is unreliable.",
    "Excellent performance on my phone even with many open tabs.",
    "I enjoy the reminders, but snooze options are limited.",
    "The dashboard looks polished and the metrics are easy to scan.",
    "Syncing between devices worked perfectly for me this week.",
    "Too many popups interrupt my workflow during normal use.",
    "Customer support replied quickly and solved my billing issue.",
    "The export feature saved me a lot of manual work.",
    "Please add a way to customize the home screen widgets.",
    "I appreciate the accessibility labels on most buttons.",
    "Text size settings reset sometimes after I restart the app.",
    "Overall experience is solid and dependable day to day.",
    "The calendar integration is useful but takes too long to refresh.",
    "I like how easy it is to share reports with teammates.",
    "Loading spinner appears too often on simple actions.",
    "The tutorial videos were short, clear, and actually helpful.",
    "I could not find where to update my notification preferences.",
    "Search results are relevant and appear almost instantly.",
    "The app drains battery faster than other tools I use.",
    "My favorite part is the simple workflow for recurring tasks.",
    "Settings are organized well, but labels could be clearer.",
    "I had no trouble inviting teammates to my project space.",
    "Performance improved after the last update, which is great.",
    "The app froze once when I attached a large image.",
    "I value the weekly summary emails with key activity highlights.",
    "Please make the charts easier to read on small screens.",
    "The design feels modern without being distracting or noisy.",
    "I found a typo in the help center article.",
    "Task creation is quick and the defaults are sensible.",
    "The latest release introduced a bug in comment editing.",
    "I really like the keyboard shortcuts for power users.",
    "Sharing links works well, but permissions are confusing.",
    "The app helps me stay organized across multiple projects.",
    "Some menu items are hidden and hard to discover.",
    "I appreciate that login supports both email and SSO.",
    "The search bar should support filtering by date range.",
    "Notifications arrive on time and are mostly relevant.",
    "I like the product, but pricing tiers are hard to understand.",
    "The interface is clean and does not feel overwhelming.",
    "Please add better error messages when uploads fail.",
    "Overall I would recommend this app to my team.",
]

word_counts = []

# Single pass for clarity: count words, store results, and print per-review output.
for index, review in enumerate(reviews, start=1):
    words = count_words(review)
    # Keeping raw counts lets us calculate multiple summary metrics afterward.
    word_counts.append(words)
    # Per-review output makes outliers visible before the final summary section.
    print(f"Review {index:>2}: {words:>2} words")

average = sum(word_counts) / len(word_counts)

# Final summary gives a compact "shape" of the dataset:
# size, range, and typical review length.
print()
print("Summary")
print("-" * 30)
print(f"Total reviews: {len(word_counts)}")
print(f"Shortest: {min(word_counts)} words")
print(f"Longest: {max(word_counts)} words")
print(f"Average: {average:.1f} words")
