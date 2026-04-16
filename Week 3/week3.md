# Week 3 Data Cleaning and Analysis

## Overview

This week focused on cleaning a messy survey dataset and analyzing participant responses.

Input dataset:
- `week3_survey_messy.csv`

Generated files:
- `responses.csv`
- `responses_cleaned.csv`
- `week3_survey_cleaned.csv`

Analysis script:
- `week3_analysis_buggy.py` (updated and debugged)

## Competency Claims

### C2: Code Literacy and Documentation

This work demonstrates C2 through reading, debugging, and documenting Python data-processing code. I identified logic and runtime issues in `week3_analysis_buggy.py` (for example, numeric parsing failures and incorrect top-5 sorting), updated the script with clearer function structure, and added documentation such as a function docstring and this written project summary.

### C5: Data Cleaning and Preparation

This work demonstrates C5 through systematic cleaning of a messy CSV dataset. I removed invalid rows with missing participant names, standardized categorical values (`role`, `department`, and `primary_tool`), corrected malformed numeric values (such as `fifteen` to `15`), and produced cleaned outputs (`responses_cleaned.csv` and `week3_survey_cleaned.csv`) ready for analysis.

## Data Cleaning Steps

The cleaning workflow included:

1. Removed rows where participant name was empty.
2. Standardized role names for consistent grouping.
3. Standardized primary tool names (for example, combining `figma` and `Figma`).
4. Corrected non-numeric experience values (for example, `fifteen` to `15`).
5. Wrote cleaned output to a new file (`week3_survey_cleaned.csv`).

## Analysis Performed

The analysis script reports:

- Response counts by role
- Average years of experience (with invalid values safely skipped)
- Top 5 highest satisfaction scores
- Participant counts by primary tool
- Plain-language summary of cleaned data:
  - row count
  - unique roles
  - number of empty name fields

## Key Results

From the current cleaned dataset:

- Total cleaned rows: 34
- Empty name fields: 0
- Roles represented:
  - Content Strategist
  - Product Manager
  - Ux Designer
  - Ux Researcher

## Notes

- The original script had a few issues that were fixed:
  - handling invalid numeric values safely
  - sorting top satisfaction scores in the correct order
  - adding primary tool summary logic
- One remaining optional improvement is preserving acronyms like `VS Code` exactly during normalization.

## How to Run

From the `Week 3` folder:

```bash
python3 clean_responses.py
python3 week3_analysis_buggy.py
```
