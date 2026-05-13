# Week 6 — A6: Visualization

## Overview

This note summarizes **Assignment 6 (Visualization)** / Mini-Project 1B. I used the offline Last.fm dataset in `Last.fm_Data.json` and the notebook `mp1b.ipynb` to create visualizations about music listening patterns across countries and genres.

The analysis focuses on three questions: which top artists appear by profile country, which global genres have the widest reach, and which genres among the top global artists have the highest play-to-listener ratios. The main goal of this assignment was to choose chart types that make the findings easy to understand, while also explaining the limitations of Last.fm account data.

---

## C3 — Data Cleaning and File Handling

I loaded a nested JSON file, `Last.fm_Data.json`, and converted specific sections of it into pandas DataFrames. I cleaned columns such as `@attr.rank`, `listeners`, `reach`, and play-to-listener metrics by renaming fields and converting values to numeric types before graphing.

---

## C5 — Data Analysis with Pandas

I used pandas to answer three research questions about Last.fm listening patterns. I filtered top artists by country, compared country pairs using overlap and Jaccard similarity, ranked global genres by `reach`, and sorted genres by median play-to-listener ratio.

---

## C6 — Data Visualization

I created Python-generated Plotly charts to communicate the main findings from the dataset. I used horizontal bar charts for ranked categories because artist and genre names are easier to read that way, and I used a country-pair similarity chart to show which profile countries shared the most top artists.

---

## C7 — Critical Evaluation and Professional Judgment

I interpreted the charts with attention to what the data can and cannot prove. I noted that Last.fm profile country data only represents Last.fm users, not whole national populations, and that the play-to-listener ratio is limited to the top global artist sample rather than every artist on the platform.
