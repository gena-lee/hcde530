# Week 4 — API Data Acquisition (Assignment 4)

## Overview

I used Python to fetch Hogwarts student data from [HP-API](https://hp-api.onrender.com/), export it to CSV, and built a local HTML dashboard for exploration.

## Why I chose this API

I chose [HP-API](https://hp-api.onrender.com/) because I recently started rewatching the series and wanted to work with data I was interested in. That familiarity made it easier to sanity-check the results—for example, whether houses and ancestries looked plausible in exports and charts. It was also interesting to review the data on my final dashboard and be able to do some data visualization on Hogwarts students.

| Artifact | Purpose |
|----------|---------|
| `hp_api_students_export.py` | GET request, JSON parse, CSV export |
| `hp_students_all.csv` | Every student row (`name`, `house`, `ancestry`) |
| `hp_students_cleaned.csv` | Rows where all three fields are present |
| `hp_students_dashboard.html` | Local dashboard; dropdown switches between cleaned vs all CSV |

---

## C4 — APIs and Data Acquisition

**Endpoint:** `GET https://hp-api.onrender.com/api/characters/students` — returns JSON as a **list of objects** with fields including `name`, `house`, and `ancestry`.

**What I did:** `requests.get` with timeout → `raise_for_status()` → `response.json()` → loop with `.get()` for safe extraction → write `hp_students_all.csv` (full response) and `hp_students_cleaned.csv` (complete rows only), plus row-count messages in the console.

**API keys:** This API needs no key. For a keyed API I would use env vars or `.env` + `.gitignore`, never commit secrets.

**Claim:** I read the HP-API documentation, called the students endpoint, and parsed the JSON in Python. I exported **all** rows to one CSV and **cleaned** rows (complete `name`, `house`, and `ancestry`) to another so summaries and the dashboard can emphasize complete records without pretending missing fields never existed.

---

## HCD reflection

APIs let designers work from **real structured data** (segments, CMS content, analytics), not only mocks. Here, choosing `/characters/students` matched the assignment; `/characters` would have mixed in non-students and distorted counts. Many rows lacked house or ancestry—I kept a full export for transparency and a cleaned file for clearer charts.

In practice I would follow the same loop: pick the right endpoint, document response shape and gaps, and call out incompleteness when sharing numbers or visuals with stakeholders.
