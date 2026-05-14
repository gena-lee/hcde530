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

## C6 — Data Visualization

I created Python-generated Plotly charts to communicate the main findings from the dataset. I used horizontal bar charts for ranked categories because artist and genre names are easier to read that way, and I used a country-pair similarity chart to show which profile countries shared the most top artists.

---

## C7 — Critical Evaluation and Professional Judgment

I interpreted the charts with attention to what the data can and cannot prove. I noted that Last.fm profile country data only represents Last.fm users, not whole national populations, and that the play-to-listener ratio is limited to the top global artist sample rather than every artist on the platform.
