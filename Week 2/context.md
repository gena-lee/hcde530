# Project context — HCDE 530 Week 2

This file describes **who this project is for**, **how it should behave**, and **what lives in the folder**. Use it alongside `.cursorrules` (Cursor-specific rules) when onboarding yourself or collaborators.

## Background

Beginner-friendly HCDE coursework. The author is an **HCD practitioner** (not a software engineer), working in **UX research and UX design**. Code literacy here supports collaboration with developers and light use of scripts in the design process.

## Goals

- Let people **run a simple Python script** on local data.
- Optionally **view results in a web page** (dashboard-style HTML).
- Keep explanations and code **accessible to learners**.

## Audience and workflow

| Topic | Preference |
| ----- | ---------- |
| Primary audience | Mix of self, classmates/instructor, and UX teammates/stakeholders |
| Default workflow | Run the Python script first, then open the dashboard |
| Terminal output | **Quick summary** by default (not long per-row logs unless asked) |
| Dashboard | **High-level metrics** by default; deeper detail only when requested |

## Technical preferences

| Topic | Preference |
| ----- | ---------- |
| Code style | Beginner-friendly; balance **clarity** and **compactness** |
| Errors | **Fail fast** with clear, actionable messages |
| Dependencies | **Dependency-free** (standard library + plain HTML/JS) unless you explicitly ask otherwise |

## Conventions (short)

**Python:** Clear names, short docstrings on non-trivial functions, concise default output, validate files/columns early.

**CSV:** UTF-8; do not silently drop bad rows without saying why; keep transforms easy to read.

**HTML dashboards:** Prefer one standalone file; vanilla JavaScript unless you ask for a framework; clear headings and labels.

**When changing the repo:** If files are added, removed, or renamed, update the directory list below and the same section in `.cursorrules`.

## Directory structure

Keep this block in sync with the actual folder.

```
HCDE 530 Week 2 Project/
├── .cursorrules              # Cursor AI guidance and rules
├── context.md                # This file — human-readable project context
├── app_review_word_count.py  # Sample app reviews + word counts + summary
├── demo_word_count.py        # Load CSV + word counts (course demo)
├── demo_responses.csv        # Example response data
├── dashboard.html            # Standalone web dashboard
└── week2.md                  # Week 2 reflection (Competency 2)
```

## Related docs

- **`week2.md`** — Reflection on code literacy and documentation for this week.
- **`.cursorrules`** — Machine-oriented rules for Cursor (same priorities, stricter “when unsure” behavior).
