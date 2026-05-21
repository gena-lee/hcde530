# Mini Project 1 — Last.fm Listening Analysis

## Overview

This mini project analyzes real listening behavior data pulled from the **Last.fm API**. The dataset is stored in `Last.fm_Data.json` and the full analysis lives in `mp1b.ipynb`.

The analysis focuses on three research questions: which top artists appear across three countries (US, Brazil, South Korea), which global genres have the widest reach, and which genres among the top 100 global artists have the highest play-to-listener ratios. The goal was to use pandas to answer specific questions about cross-cultural music overlap and listening intensity, then communicate the findings through charts with honest limitations stated.

---

## Chart Justifications

- **RQ1 — Top artists by profile country:** I used a horizontal bar chart because artist names are long and easier to read on the y-axis. For overlap, I used a country-pair similarity heatmap so each pair appears once and the reader can quickly spot that the US and South Korea share the most artists (Jaccard = 0.60).
- **RQ2 — Global genres by reach:** I used a horizontal bar chart to rank genres from highest to lowest reach. It makes it immediately clear that rock has the widest global reach in the Last.fm tag dataset.
- **RQ3 — Play-to-listener ratio by genre:** I used a horizontal bar chart to rank the five genres with the highest median play-to-listener ratios, making it easy to compare play intensity and see that R&B leads.

---

## Limitations

Last.fm **profile country** is self-reported — the country charts reflect Last.fm user behavior, not national listening habits at large. **Tags** are user-applied and do not form a strict genre taxonomy, so two artists tagged "rock" may sound nothing alike. **`reach`**, **`playcount`**, and **`listeners`** are platform-specific and time-dependent; the numbers are a snapshot at the moment of the API call, not a stable measure of global popularity. The **play-to-listener ratio** analysis is scoped to the top 100 global chart artists only, so genres underrepresented in that chart may not appear.

---

## C4 — APIs and Data Acquisition

I pulled structured data from the Last.fm API using Python, stored the responses in `Last.fm_Data.json`, and kept my API key out of version control using a `.env` file.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **HTTP request + JSON parsing** | In `lastfm_api.py` I use `urllib.request` to call Last.fm endpoints (e.g. `geo.getTopArtists`, `chart.getTopArtists`, `tag.getTopTags`) and parse the JSON responses directly into pandas DataFrames. |
| **API I found and used myself** | I used the Last.fm public API (`ws.audioscrobbler.com/2.0/`), which I chose because it exposes real listening behavior across users worldwide and matched my interest in cross-cultural music patterns. |
| **API key handling** | My API key is stored in a `.env` file and loaded via `resolve_lastfm_api_key()` in `lastfm_api.py`. The `.env` file is excluded from version control so the key is never committed to GitHub. |
| **Endpoint explanation** | `geo.getTopArtists` returns the top artists for a given profile country. `chart.getTopArtists` returns the global top 100. `tag.getTopTags` returns the most-used genre tags with reach and tagging counts. I filtered, joined, and stored the results in `Last.fm_Data.json` for offline analysis. |

---

## C5 — Data Analysis with Pandas

I used pandas to answer three specific analytical questions about the dataset, using multiple operations including renaming columns, type conversion, filtering, sorting, and building pivot-style structures.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Loads dataset and answers specific questions** | `mp1b.ipynb` loads `Last.fm_Data.json` into multiple DataFrames and answers all three research questions with code and written interpretations. |
| **Multiple pandas operations** | I used `pd.DataFrame()`, `rename()`, `pd.to_numeric()`, `isnull().sum()`, boolean filtering (`rq1_df[rq1_df["rank"] <= 10]`), `sort_values()`, and `pd.DataFrame(1.0, index=..., columns=...)` to build the Jaccard similarity matrix. |
| **Handling data quality issues** | The original `@attr.rank` and `listeners` columns were stored as strings in the JSON. I used `pd.to_numeric(..., errors="coerce")` to convert them and confirmed with `df.info()` that the types were correct before analyzing. I also found that 2 rows had missing `mbid` values, which I noted but did not need to fix since `mbid` was not used in the analysis. |
| **Written interpretation** | Each code output has a markdown interpretation cell explaining what the result means — not just the numbers. For example, I noted that the wide listener count range (min 496, max 242K) is driven by South Korea having far fewer Last.fm users than the US, not by the artists themselves being less popular globally. |

---

## C6 — Data Visualization

I built Plotly charts in Python to communicate the findings from all three research questions. Each chart is followed by a markdown cell explaining the finding and the chart type choice.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Charts in Python** | In `mp1b.ipynb` I build Plotly figures for all three research questions: a horizontal bar chart of top artists per country (RQ1), a country-pair similarity heatmap (RQ1 overlap), a horizontal bar chart of top genres by global reach (RQ2), and a horizontal bar chart of genres by median play-to-listener ratio (RQ3). |
| **Why these chart types** | Artist and genre names are long text labels — horizontal bar charts keep them readable and rank categories cleanly. The similarity heatmap is used for RQ1 overlap so each country pair appears once, making it faster to compare than a table or grouped bar. |
| **Notebook + narrative** | Code, rendered Plotly outputs, and markdown explanations live in `mp1b.ipynb`. Each chart is preceded or followed by an interpretation cell explaining what the visual shows and what it cannot prove. |

---

## C7 — Critical Evaluation and Professional Judgment

I evaluated the data source and metrics critically before drawing conclusions, and I stated scope boundaries explicitly so the findings are not overstated.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Data source critique** | I flag in the notebook that `geo.getTopArtists` uses self-reported profile country, not physical location or market data — so the country charts describe Last.fm user behavior in that region, not a census of national listening habits. |
| **Metric limitations** | For RQ2 I explain that `reach` is a Last.fm-internal measure, not a cross-platform popularity score. For RQ3 I note that grouping each artist by a single primary tag is a simplification, and that the play-to-listener ratio only covers the 100 artists on the global chart at the time of the API call. |
| **Unexpected result flagged** | The US and South Korea had the highest artist overlap (Jaccard = 0.60) despite South Korea having much lower absolute listener counts. I noted this as a surprising finding and explained that it is likely driven by globally mainstream artists appearing on both charts, and that the low listener counts reflect the smaller Last.fm user base in South Korea — not lower actual popularity. |
| **Scope boundaries stated** | Each research question is scoped explicitly (e.g. "among the top 100 global chart artists," "among Last.fm users who list their profile country as…") so the reader knows the finding applies to that sample only. |
