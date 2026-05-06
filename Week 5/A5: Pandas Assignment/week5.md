# Week 5 — A5: Pandas Analysis

## Overview

This note summarizes **Assignment 5 (Pandas Analysis)** / Mini-Project 1: I pull listening-related data from the **Last.fm API**, analyze it with **pandas**, and visualize results with **matplotlib**. The main deliverable is **`mp1.ipynb`** in this folder, with **`lastfm_api.py`** providing **`lastfm_call()`** and **`requirements.txt`** listing dependencies (`pandas`, `matplotlib`, `ipython`, `ipykernel`). My API key stays in **`.env`** as `LASTFM_API_KEY` (not committed to git).

## Why I chose this API

I chose the **Last.fm API** because I care about **music** and how it shows up **on a global scale**—how listening and “what counts as popular” can differ when you move across countries. I wanted to see how that plays out in real platform data, not only in headlines or charts from one market.

For **Research Question 1**, I focused on **three countries—the United States, Brazil, and South Korea**—to compare national top-artist charts side by side. That matched both my interest in cross-country listening and the notebook’s geographic comparison. If I had more time, I could narrow or extend the country list, but this trio already surfaces useful overlap-versus-difference patterns.

---

## Setup

- Loaded credentials from the environment / `.env`, then used **`lastfm_call(method, params)`** from `lastfm_api.py` for all authenticated JSON requests.
- Used **pandas** for tables (`DataFrame`, `json_normalize`, merges/aggregations) and **matplotlib** for charts.

---

## Research Question 1 — Top artists by profile country

- **Question:** Who are the top artists on Last.fm for users who set their **profile country** to the **United States**, **Brazil**, and **South Korea**, and how **similar** are those national charts?
- **API:** [`geo.getTopArtists`](https://www.last.fm/api/show/geo.getTopArtists) (country-scoped chart).
- **What I did:** Fetched top artists per country, built side‑by‑side / ranked views, and analyzed **overlap** (who appears in one chart vs another) to discuss **geographic bias** and how much Last.fm activity in each country reflects “global” popularity vs local tastes.
- **Caveat:** Country is **self-reported profile location**, not physical residency or market sales data.

---

## Research Question 2 — Tags with the largest audience (genre proxy)

- **Question:** Which Last.fm **tags** have the most **listeners**, using the API’s notion of audience size?
- **API:** [`chart.getTopTags`](https://www.last.fm/api/show/chart.getTopTags) with a limit of **50** tags (`LIMIT_TAGS = 50`).
- **Metric:** **`reach`** — users associated with each tag on Last.fm (via tag metadata); tags are treated as a loose **genre** proxy.
- **What I did:** Normalized the API response, sorted tags by **`reach`**, inspected tables, and plotted **top tags by reach** (horizontal bar chart).

---

## Research Question 3 — Play-to-listener ratio by primary tag

- **Question:** Among artists on Last.fm’s **global chart**, how does **`playcount / listeners`** (plays per listener) vary when artists are grouped by a **primary tag** from [`artist.getTopTags`](https://www.last.fm/api/show/artist.getTopTags)?
- **Population:** **100** artists from [`chart.getTopArtists`](https://www.last.fm/api/show/chart.getTopArtists) (`RQ3_TARGET_N = 100`), fetched with pagination and **deduplicated** by MusicBrainz ID or name so repeats do not dominate.
- **Per artist:** [`artist.getInfo`](https://www.last.fm/api/show/artist.getInfo) for `playcount` and `listeners`; **`artist.getTopTags`** for the **first tag** as **primary “genre”**.
- **Aggregation:** Grouped by **`genre_tag`**, required at least **`MIN_ARTISTS_PER_TAG = 5`** artists per tag before ranking, and compared **median** (and weighted) **plays per listener** across tags; plotted top tags.
- **Artifacts:** The notebook can save **`rq3_chart100_df.pkl`** and **`rq3_artists_df.pkl`** so RQ3 cells can reload after a kernel restart without repeating every API call.

---

## Limitations (across the project)

Last.fm **tags** are not a strict genre taxonomy; **`reach`**, **`playcount`**, and **`listeners`** are **platform-specific** and **time-dependent**. Results should be read as snapshots of behavior **on Last.fm**, not as universal truth about all listeners worldwide.

---

## C5: Data Analysis with Pandas

**What the rubric asks for:** A notebook or script that loads data and answers at least one specific question, uses **at least two** pandas operations (e.g. `groupby`, `fillna`, `value_counts`, `merge`), and includes a **written interpretation** of what the numbers mean—not only code output.

**How MP1 meets that (strong claim, not “I used pandas”):**

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Dataset + question** | I treat Last.fm API responses as datasets: **RQ1** compares national top-artist charts; **RQ2** ranks global tags by audience; **RQ3** compares **plays per listener** across **primary tags** for chart artists. Each part answers one precise question. |
| **Pandas operations (examples)** | **`pd.json_normalize`** on nested JSON; **`pd.concat`** to stack per-country or per-page results; **`groupby`** with **`.agg`** for RQ3 (median play/listener, counts, sums); **`sort_values`** after ranking tags by `reach`; **`drop_duplicates`** on chart artists so MBID/name repeats do not skew RQ3; **`pd.to_numeric(..., errors="coerce")`** to coerce bad/missing numerics; **`.loc`** to filter tags with enough artists (`MIN_ARTISTS_PER_TAG`). That is well over two distinct operation *types*. |
| **Missing / messy data** | Coercing listeners/playcounts with **`errors="coerce"`**, skipping artists with no listeners or no tags in the enrichment loop, and deduplicating the chart are explicit handling choices—not assumed-clean data. |
| **Interpretation** | In **`mp1.ipynb`** markdown cells I explain what overlap between country charts *means* for geographic bias (RQ1), why **`reach`** is a platform-specific “audience” measure (RQ2), and how median plays-per-listener by tag should be read as a rough comparison under the primary-tag simplification (RQ3). **`week5.md`** is an additional narrative summary. |

**One sentence I could put in a portfolio:** *“I used `groupby('genre_tag').agg(...)` on enriched chart artists and filtered to tags with at least five artists, then sorted by median plays per listener—so the ranking reflects multi-artist tags, not one outlier.”*

---

## C6: Visualization (additional work)

**What the rubric asks for:** At least one **Python-generated chart** (matplotlib, seaborn, or pandas `.plot()`), a **justification for chart type**, and a **Jupyter notebook on GitHub** with code, outputs, and markdown so a reader can follow the reasoning.

**How MP1 meets that:**

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Charts in Python** | In **`mp1.ipynb`** I build **matplotlib** figures with **`fig, ax = plt.subplots(...)`** and **`ax.barh(...)`** for (1) **top tags by `reach`** (RQ2) and (2) **top tags by median plays per listener** (RQ3), subject to the minimum-artists rule. |
| **Why horizontal bars** | Tag names are **many categories** with **long text labels**. A **horizontal bar chart** keeps labels readable and ranks categories along one axis—similar to the rubric’s example about satisfaction by role. Vertical bars or pie charts would fight label overlap or imply parts-of-a-whole incorrectly. |
| **Notebook + narrative** | Code, printed tables, plots, and markdown explanations live in **`mp1.ipynb`**. After you push this repo to GitHub, replace the placeholder below with your notebook URL for submissions that ask for a link. |

**GitHub (fill in after you publish):** `[your repo URL]/blob/[branch]/Week 5/A5: Pandas Assignment/mp1.ipynb`

---

## Files (MP1 folder)

| File | Role |
|------|------|
| `mp1.ipynb` | Full analysis and write-up for RQ1–RQ3 |
| `lastfm_api.py` | API key resolution + `lastfm_call()` |
| `requirements.txt` | Python dependencies for the environment |
| `.env` | Local API key (gitignored) |
| `rq3_chart100_df.pkl`, `rq3_artists_df.pkl` | Optional RQ3 caches (regenerated by re-running cells) |
