import csv
from pathlib import Path

import requests


API_URL = "https://hp-api.onrender.com/api/characters/students"
OUTPUT_CSV = Path(__file__).resolve().parent / "hp_students_name_house_ancestry.csv"
OUTPUT_ALL_CSV = Path(__file__).resolve().parent / "hp_students_all_name_house_ancestry.csv"


def fetch_students() -> list[dict]:
    """Fetch all students from the HP API endpoint."""
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list):
        raise ValueError("Unexpected API response format. Expected a list.")

    return payload


def main() -> None:
    students = fetch_students()
    complete_rows: list[dict[str, str]] = []
    all_rows: list[dict[str, str]] = []
    skipped = 0

    for student in students:
        name = student.get("name", "") or ""
        house = student.get("house", "") or ""
        ancestry = student.get("ancestry", "") or ""
        row = {"name": name, "house": house, "ancestry": ancestry}
        all_rows.append(row)

        if not (name and house and ancestry):
            skipped += 1
            continue

        print(f"Name: {name}, House: {house}, Ancestry: {ancestry}")
        complete_rows.append(row)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "house", "ancestry"])
        writer.writeheader()
        writer.writerows(complete_rows)

    with open(OUTPUT_ALL_CSV, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "house", "ancestry"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nSaved {len(complete_rows)} complete rows to {OUTPUT_CSV}")
    print(f"Saved {len(all_rows)} total rows to {OUTPUT_ALL_CSV}")
    print(f"Skipped {skipped} rows missing at least one field.")


if __name__ == "__main__":
    main()
