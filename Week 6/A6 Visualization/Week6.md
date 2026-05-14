# Week 6 — A6: Visualization

## Overview

This note summarizes **Assignment 6 (Visualization)** / Mini-Project 1B. I used the offline Last.fm dataset in `Last.fm_Data.json` and the notebook `mp1b.ipynb` to create visualizations about music listening patterns across countries and genres.

The analysis focuses on three questions: which top artists appear by profile country, which global genres have the widest reach, and which genres among the top global artists have the highest play-to-listener ratios. The main goal of this assignment was to choose chart types that make the findings easy to understand, while also explaining the limitations of Last.fm account data.

---

## Chart Justifications

- **RQ1 — Top artists by profile country:** I used a horizontal bar chart because artist names are easier to read on the y-axis, and the bars make listener counts easy to compare within each country. For country overlap, I used a country-pair similarity chart so each pair appears once and the reader can quickly see that the United States and South Korea overlap the most.
- **RQ2 — Global genres by reach:** I used a horizontal bar chart because the question is about ranking genres from highest to lowest reach. This chart helps the reader see that rock has the widest reach among the Last.fm genre tags in my dataset.
- **RQ3 — Play-to-listener ratio by genre:** I used a horizontal bar chart because it clearly ranks the five genres with the highest median play-to-listener ratios. This helps the reader compare play intensity across genres and see that R&B has the highest ratio in the top global artist sample.

---

## Limitations

Last.fm **profile country** is self-reported and reflects where users say they are, not actual residency or market sales data — so country-based charts describe Last.fm user behavior, not national listening habits at large. **Tags** are user-applied and do not form a strict genre taxonomy, meaning two artists tagged "rock" may sound nothing alike. **`reach`**, **`playcount`**, and **`listeners`** are platform-specific and time-dependent; the numbers are a snapshot of Last.fm activity at the moment of the API call, not a stable measure of global popularity. The **play-to-listener ratio** analysis is further scoped to the top global artist sample only, so genres that are popular on Last.fm but underrepresented in that chart may not appear at all.

---

## C6 — Data Visualization

I created Python-generated Plotly charts to communicate the main findings from the dataset. I used horizontal bar charts for ranked categories because artist and genre names are easier to read that way, and I used a country-pair similarity chart to show which profile countries shared the most top artists.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Charts in Python** | In `mp1b.ipynb` I build **Plotly** figures for all three research questions: a horizontal bar chart of top artists per country (RQ1), a country-pair similarity chart showing how much national top-artist lists overlap (RQ1), a horizontal bar chart of top genres by global reach (RQ2), and a horizontal bar chart of top genres by median play-to-listener ratio (RQ3). |
| **Why these chart types** | Artist and genre names are long text labels — **horizontal bar charts** keep them readable and rank categories along one axis without label overlap. The **country-pair similarity chart** is used for RQ1 overlap because each pair should appear only once; a matrix or grouped bar would either duplicate pairs or require the reader to mentally combine two cells. |
| **Notebook + narrative** | Code, rendered Plotly outputs, and markdown explanations live in `mp1b.ipynb`. Each chart is followed by an interpretation cell explaining what the visual shows and what it cannot prove. |

---

## C7 — Critical Evaluation and Professional Judgment

I interpreted the charts with attention to what the data can and cannot prove. I noted that Last.fm profile country data only represents Last.fm users, not whole national populations, and that the play-to-listener ratio is limited to the top global artist sample rather than every artist on the platform.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Data source critique** | I flag in the notebook that `geo.getTopArtists` uses self-reported profile country, not physical location or streaming market data — so the country charts reflect who is active on Last.fm in that region, not a census of national listening. |
| **Metric limitations** | For RQ2 I explain that `reach` is a Last.fm-internal audience measure, not a cross-platform popularity score. For RQ3 I note that grouping by a single primary tag is a simplification, and that the ratio only covers the 100 artists on the global chart at time of fetch. |
| **Scope boundaries stated** | Each research question is scoped explicitly (e.g. "among the top 100 global chart artists") so the reader knows the finding applies to that sample, not to all music or all Last.fm users. |
