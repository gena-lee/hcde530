import csv
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    source_file = base_dir / "week3_survey_messy.csv"
    responses_file = base_dir / "responses.csv"
    cleaned_file = base_dir / "responses_cleaned.csv"

    # Step 1: Build responses.csv from the full survey file.
    with open(source_file, mode="r", newline="", encoding="utf-8") as source_in:
        source_reader = csv.DictReader(source_in)
        if source_reader.fieldnames is None:
            raise ValueError("Input CSV is missing headers.")

        with open(responses_file, mode="w", newline="", encoding="utf-8") as responses_out:
            responses_writer = csv.DictWriter(
                responses_out, fieldnames=["name", "role", "department"]
            )
            responses_writer.writeheader()

            for row in source_reader:
                responses_writer.writerow(
                    {
                        "name": row.get("participant_name") or "",
                        "role": row.get("role") or "",
                        "department": row.get("department") or "",
                    }
                )

    # Step 2: Clean responses.csv into responses_cleaned.csv.
    with open(responses_file, mode="r", newline="", encoding="utf-8") as responses_in:
        responses_reader = csv.DictReader(responses_in)
        if responses_reader.fieldnames is None:
            raise ValueError("responses.csv is missing headers.")

        fieldnames = responses_reader.fieldnames
        with open(cleaned_file, mode="w", newline="", encoding="utf-8") as cleaned_out:
            cleaned_writer = csv.DictWriter(cleaned_out, fieldnames=fieldnames)
            cleaned_writer.writeheader()

            for row in responses_reader:
                name_value = (row.get("name") or "").strip()
                if not name_value:
                    continue

                row["role"] = (row.get("role") or "").upper()
                cleaned_writer.writerow(row)


if __name__ == "__main__":
    main()
