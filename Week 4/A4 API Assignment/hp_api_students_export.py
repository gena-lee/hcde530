import csv
from pathlib import Path

import requests

# I linked the HP-API url and endpoint to the students endpoint in order to get the students data.
API_URL = "https://hp-api.onrender.com/api/characters/students"
OUTPUT_CSV = Path(__file__).resolve().parent / "hp_students_cleaned.csv"
OUTPUT_ALL_CSV = Path(__file__).resolve().parent / "hp_students_all.csv"

# I created a function to fetch the students data and listed the name, house, and ancestry of the students.
def fetch_students() -> list[dict]:
    """Fetch all students from the HP API endpoint."""
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list):
        raise ValueError("Unexpected API response format. Expected a list.")

    return payload

# I created a main function to run the script and save the data to a CSV file.
def main() -> None:
    students = fetch_students()
    complete_rows: list[dict[str, str]] = []
    all_rows: list[dict[str, str]] = []
    skipped = 0
# I wanted to loop through each student record and collect name, house, and ancestry.
# This avoids repeating the same extraction code for every row.
    for student in students:
        name = student.get("name", "") or ""
        house = student.get("house", "") or ""
        ancestry = student.get("ancestry", "") or ""
        row = {"name": name, "house": house, "ancestry": ancestry}
        all_rows.append(row)

        if not (name and house and ancestry):
            skipped += 1
            continue
# I printed the name, house, and ancestry of each student to see the final data.
        print(f"Name: {name}, House: {house}, Ancestry: {ancestry}")
        complete_rows.append(row)
# I then saved the data to two separate CSV files. One of all the students and one of the complete rows.
# I wanted to create a clean version of the dataset that only showed students with all three fields, but still keep the original dataset.
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "house", "ancestry"])
        writer.writeheader()
        writer.writerows(complete_rows)

    with open(OUTPUT_ALL_CSV, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "house", "ancestry"])
        writer.writeheader()
        writer.writerows(all_rows)
# I printed the number of complete rows and total rows saved to the console.
    print(f"\nSaved {len(complete_rows)} complete rows to {OUTPUT_CSV}")
    print(f"Saved {len(all_rows)} total rows to {OUTPUT_ALL_CSV}")
    print(f"Skipped {skipped} rows missing at least one field.")

# I then ran the script to save the data to the CSV files.
if __name__ == "__main__":
    main()
