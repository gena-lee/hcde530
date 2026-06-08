# Fontface

A web-based **type system builder** that helps you pick fonts, pair them, preview them at real sizes, and export the result as ready-to-use CSS. Built for designers and non-designers alike.

**Try it live →** [https://fontface-two.vercel.app](https://fontface-two.vercel.app)

---

## What it does

Fontface walks you through five guided steps and produces a complete typographic system at the end:

1. **Filter Fonts** — Browse Google's full font library, narrow down by category, mood, or use case
2. **Pick Primary** — Choose your headline font
3. **Choose Pairing** — Pick from suggested body fonts curated to complement your primary
4. **Preview** — See the two fonts working together at real sizes; drag any size label to adjust, swap fonts live
5. **Export** — Get a fully editable type scale chart and download it as a ready-to-paste CSS file or PNG

No signup, no setup. Open the link, build a type system in under five minutes.

## Who it's for

- **Non-designers** (PMs, founders, students, anyone building a brand or side project) who need typography that feels considered but don't have the vocabulary to choose fonts confidently
- **Designers** who want a faster way to prototype font pairings without opening Figma + Google Fonts + a CSS file in three different tabs

## How it works

Fontface uses the **Google Fonts Developer API** to pull every available font family (~1,900) with its weights and categories. A custom **scoring algorithm** then suggests pairings based on category contrast (serif + sans-serif), shared mood tags (e.g. both "elegant"), and complementary use cases (display ↔ body). For ~65 popular fonts the suggestions are hand-curated; for everything else, the algorithm derives sensible defaults.

The pairing logic is documented in detail at [`../Week 8/PAIRING.md`](../Week%208/PAIRING.md).

## Running it locally

Fontface is a single static HTML file. To run locally:

```bash
cd "Mini Project 2"
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

You'll need a Google Fonts API key embedded in `index.html` (free at [aistudio.google.com](https://aistudio.google.com/apikey) or [Cloud Console](https://console.cloud.google.com/apis/credentials)). For the deployed version the key is HTTP-referrer-restricted to the live URL.

## Tech

Single-file vanilla HTML / CSS / JavaScript — no frameworks, no build step. The only external dependencies are the Google Fonts API for the font catalog and `html2canvas` (CDN) for PNG export.

## Files

- **[index.html](index.html)** — the entire application
- **[poster.html](poster.html)** — a 1920×1080 poster page for gallery submissions
- **[mp2.md](mp2.md)** — competency claims and reflection for HCDE 530 MP2
