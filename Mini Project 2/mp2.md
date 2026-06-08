# Mini Project 2 — Fontface

## Overview

**Fontface** is a web-based type system builder. It guides users through five steps — filter fonts, pick a primary, choose a pairing, preview at real sizes, export as CSS — and produces a complete, exportable type system at the end. It is designed primarily for **non-designers** (PMs, founders, students) who need polished typography for a project but don't have the vocabulary to choose fonts confidently, while still being useful for designers who want a faster prototyping path.

**Live URL:** `https://fontface-two.vercel.app`
**Repo:** [github.com/gena-lee/hcde530/tree/main/Mini%20Project%202](https://github.com/gena-lee/hcde530/tree/main/Mini%20Project%202)

---

## C1 — Vibecoding and Rapid Prototyping

I used **Claude Code** as my primary build tool, iterating across multiple sessions over several days. The tool was excellent at the typographic craft details (font-preview lazy loading, drag-to-resize scrubbers), but I had to push back repeatedly on visual design defaults and on a flat pairing algorithm that produced repetitive results.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Deployed app with shareable URL** | `https://fontface-two.vercel.app` — anyone can use the full 5-step flow end-to-end without setup. |
| **Multiple iterations, not one prompt** | Visual hero went through ~5 iterations (starburst icon → Ff monogram → "element tile" with atomic-number styling → typographic wordmark using Inter Bold + EB Garamond Italic). Each round was a deliberate redirect, not just accepting the first output. |
| **One thing the tool did well** | The Step 4 dropdowns lazy-load font CSS via `IntersectionObserver` as options scroll into view — Claude built this correctly on the first try. I wouldn't have thought of that pattern unprompted. |
| **One thing I had to correct** | The first pairing algorithm was a hardcoded `PAIRING_MAP` of 65 fonts that produced the same 3 suggestions for any sans-serif. I asked Claude to build a tag-aware scoring system instead (category contrast + mood overlap + use-case complement). Documented in [PAIRING.md](../Week%208/PAIRING.md). |

---

## C4 — APIs and Data Acquisition

Fontface pulls its entire font catalog (~1,900 families) from the **Google Fonts Developer API** on page load, parses the JSON, filters out non-text fonts (icon and emoji families), and uses the result to power filters, the font picker, and the pairing suggestions.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **HTTP request + JSON parse** | `fetch('https://www.googleapis.com/webfonts/v1/webfonts?key=<KEY>&sort=popularity')` in `fetchFonts()` — parses the response, maps each font to `{family, category, variants, meta}`. |
| **API I found myself** | Google Fonts Developer API, not a class demo. I read the docs to understand that each family has a `category` (`serif`, `sans-serif`, `display`, `handwriting`, `monospace`) and `variants` (weight + italic combos), and used both to drive filtering and the Step 4 weight dropdowns. |
| **API key handling** | Embedded the key directly in client-side JS — but **restricted by HTTP referrer** in Google Cloud Console (`https://gena-lee.github.io/*`, `http://localhost/*`, `file:///*`). `.gitignore` doesn't work for a static client app because the key has to ship to the browser; referrer restriction is the actual defense, which I learned the hard way when Google's GitHub scanner flagged and disabled an early test key. |
| **What I do with the response** | Filter for text-only fonts, sort A–Z for the picker dropdown, populate category counts in the sidebar, and pass each font's `variants` into the weight dropdown so Step 5 only offers weights the font actually supports. |

---

## C8 — Building and Deploying a Complete Tool

Fontface is deployed and usable end-to-end: filter → pick primary → choose pairing → preview at real sizes → export as PNG or CSS. The 5-step flow, the editable type-scale chart, the drag-to-resize size labels, and the per-row weight/typeface controls all work without setup on the user's side. The biggest snag was building an AI mode I had to remove before launch.

| Piece of evidence | What I actually did |
|-------------------|---------------------|
| **Deployed tool, live URL** | `https://fontface-two.vercel.app` — Vercel auto-rebuilds on every `git push`. Backup at `https://gena-lee.github.io/hcde530/Mini%20Project%202/`. |
| **What the tool does + who it's for** | Helps non-designers and designers build a complete type system (font pairing + scale + exportable CSS) in five guided steps. Primary audience: non-designers who don't know typography vocabulary; built so anyone can land on the welcome page and ship a system in under five minutes. |
| **One thing that went wrong** | I built an "Ask AI" mode where users could describe their brand and upload moodboards, and Gemini would recommend fonts. After deploying I discovered Google's free tier had been reduced to a project-wide cap of **0 requests** on the models I needed — making the feature unusable without billing. I **removed AI mode entirely** (≈2,100 lines of CSS/JS) rather than ship a feature that broke for every visitor. A silent failure is worse than a missing feature. |
| **What I'd do differently** | Scope the AI feature realistically *before* building it. Specifically: confirm API access on the actual account type, test rate limits with a 10-request burst on day one, and skip the feature if those don't clear. Easier to not build a feature than to build it and rip it out. |

---

## Files in this project

- **[index.html](index.html)** — the entire application (single static file, no build step)
- **[poster.html](poster.html)** — a 1920×1080 poster page used for the gallery submission image
- **[../Week 8/PAIRING.md](../Week%208/PAIRING.md)** — documentation of the font pairing scoring algorithm
