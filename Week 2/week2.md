# Week 2 — Competency 2: Code literacy and documentation

## What I worked on (and why I documented)

I practiced **code literacy and documentation** by commenting code for **intent** (not only mechanics), adding **`.cursorrules`** for project context, using **Cursor** to translate jargon, and building **dashboard-style HTML** alongside terminal output. Documentation here is part of **code literacy**: naming tradeoffs and explaining *why* a script is structured a certain way—not only that it runs.

## Specific choices in my scripts

### `demo_word_count.py`

- **`csv.DictReader` with `encoding="utf-8"` and `newline=""`**: Named keys (`row["response"]`) keep the loop readable and stable if column order changes; CSV defaults are set deliberately so text behaves predictably.
- **`count_words()` helper**: One place defines “what counts as a word,” so summaries stay consistent if that rule changes.
- **Fixed-width table, 60-character preview, then min/max/average**: Cases first, aggregate second—**progressive disclosure** and output that is easy to scan in a narrow terminal.

### `app_review_word_count.py`

- **Reviews in a Python list**: Self-contained practice so I could focus on loops and stats without file I/O yet.
- **`enumerate(..., start=1)` plus collecting `word_counts` then summary stats**: Readable review numbering without extra counters; gather counts in one pass, interpret (min/max/average) after—clearer to read and extend.

## What was challenging and what helped

New **technical jargon** slowed me down at first. **Cursor** in plain language and **instructor** check-ins when I was stuck made the material easier to connect to my own scripts.

## How this connects to my UX practice

**Code literacy** helps me align with developers on feasibility and implementation. The script choices mirror UX habits I already value: **progressive disclosure**, **scannable information architecture**, and **consistency**—documented in `week2.md` and comments so documentation reads as part of the work, not an add-on.

## Artifacts (this project)

| Artifact | Role |
| -------- | ---- |
| `.cursorrules` | Project conventions, context profile, and directory snapshot |
| `demo_word_count.py` | CSV loading and word counts (course demo script) |
| `demo_responses.csv` | Example qualitative-style responses |
| `dashboard.html` | Web view of summary-style metrics |
| `app_review_word_count.py` | Standalone script with sample reviews and summary stats |
