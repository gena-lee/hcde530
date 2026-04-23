import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


BASE_URL = "https://hcde530-week4-api.onrender.com/reviews"
OUTPUT_DIR = Path(__file__).resolve().parent
CSV_OUTPUT = OUTPUT_DIR / "reviews_category_helpful_votes.csv"
TOP_RATED_CSV_OUTPUT = OUTPUT_DIR / "top_rated_reviews_all_apps.csv"


def fetch_all_reviews(limit=100):
    """Fetch all review records using pagination."""
    offset = 0
    all_reviews = []

    while True:
        params = {"offset": offset, "limit": limit}
        url = f"{BASE_URL}?{urlencode(params)}"
        with urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        reviews = data.get("reviews", [])
        all_reviews.extend(reviews)

        returned = data.get("returned", len(reviews))
        total = data.get("total", 0)

        if returned == 0 or offset + returned >= total:
            break

        offset += returned

    return all_reviews


def main():
    reviews = fetch_all_reviews()

    rows = []
    top_rated_rows = []
    for review in reviews:
        category = review.get("category")
        helpful_votes = review.get("helpful_votes")
        print(f"Category: {category}, Helpful votes: {helpful_votes}")
        rows.append({"category": category, "helpful_votes": helpful_votes})
        top_rated_rows.append(
            {
                "id": review.get("id"),
                "app": review.get("app"),
                "category": category,
                "rating": review.get("rating"),
                "helpful_votes": helpful_votes,
            }
        )

    top_rated_rows.sort(
        key=lambda row: (
            row["rating"] if row["rating"] is not None else -1,
            row["helpful_votes"] if row["helpful_votes"] is not None else -1,
        ),
        reverse=True,
    )

    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["category", "helpful_votes"])
        writer.writeheader()
        writer.writerows(rows)

    with open(TOP_RATED_CSV_OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["id", "app", "category", "rating", "helpful_votes"]
        )
        writer.writeheader()
        writer.writerows(top_rated_rows)

    print(f"\nSaved {len(rows)} rows to {CSV_OUTPUT}")
    print(f"Saved {len(top_rated_rows)} rows to {TOP_RATED_CSV_OUTPUT}")


if __name__ == "__main__":
    main()
