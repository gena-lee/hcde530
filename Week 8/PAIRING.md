# How Fontface Picks Pairings

This doc explains how the tool decides which fonts to suggest as a body/pairing for the primary font a user picks. No prior typography knowledge needed.

## The big idea

When you pick a primary font (say, *Playfair Display*), Fontface needs to suggest 2–3 *body* fonts that work well with it. Instead of just hardcoding "these always pair," the tool scores every font in the Google Fonts library against your primary and picks the top matches.

Three things drive the suggestions:

1. **A curated pairing map** — hand-picked "known good" pairings for ~65 popular fonts
2. **A scoring algorithm** — for everything else, math decides
3. **Tags** — every font is tagged with moods (elegant, playful, bold, etc.) and use cases (display, body-text, branding, UI), which the algorithm uses to compare fonts

All three live in [fontface/index.html](../fontface/index.html) in the JavaScript section.

---

## The two ingredients

### 1. The curated map (`PAIRING_MAP`)

A simple lookup table: *"if the user picks X, these are great body fonts."*

```js
"Playfair Display": ["Lato", "Source Sans 3", "Raleway"],
"Inter":            ["Playfair Display", "Fraunces", "Merriweather"],
"DM Sans":          ["DM Serif Display", "Fraunces", "Lora"],
```

This was assembled by hand using classic typographic conventions — serif headlines tend to pair with sans-serif body text, condensed displays pair with relaxed body fonts, and so on. It covers about 65 of the most popular Google Fonts.

### 2. The scoring algorithm (`scorePairing`)

For any other font (or to re-rank within the curated picks), every candidate gets a number based on five signals. The higher the score, the better the match.

---

## How the scoring works

Given a `primary` font and a `candidate` font, the score is:

```
score = category_contrast + mood_overlap + use_case_complement + curated_bonus + popularity_tiebreak
```

Let's break each one down.

### Signal 1 — Category contrast (+5)

The classic rule: serifs pair with sans-serifs, displays pair with workhorse sans, etc. If the candidate's category is a known good complement to the primary's, it gets +5.

The complementary category map:

```js
'serif':       pairs with ['sans-serif']
'sans-serif':  pairs with ['serif', 'display']
'display':     pairs with ['sans-serif', 'serif']
'handwriting': pairs with ['sans-serif']
'monospace':   pairs with ['serif', 'sans-serif']
```

So if your primary is a serif and the candidate is a sans-serif, +5. If both are serifs, no bonus.

### Signal 2 — Mood overlap (+1 per shared mood)

Each font is tagged with moods like *elegant*, *playful*, *minimal*, *bold*, *classic*, etc. (See `FONT_META` in the code.) The algorithm counts how many moods the two fonts share — each shared mood adds 1 point.

**Why:** Fonts that share moods feel harmonious together. *Playfair Display* (elegant, classic, bold) pairs nicely with *Cormorant Garamond* (elegant, classic, editorial) partly because both feel elegant and classical.

### Signal 3 — Use-case complement (+2)

Each font is also tagged with use cases: *display*, *branding*, *body-text*, *ui-app*. A good type *system* has one font for big stuff and one for small stuff. So:

- If the primary is best for display/branding AND the candidate is good for body-text → **+2**
- If the primary is best for body-text AND the candidate is good for display/branding → **+2**

**Why:** This is what turns a pairing into a *system*. You need different fonts for different jobs in the hierarchy.

### Signal 4 — Curated bonus (+6)

If the candidate appears in the curated `PAIRING_MAP` for this primary, it gets +6.

**Why:** This preserves all the hand-picked typographic wisdom in the map. Curated picks naturally win their slots, but they're part of the same scoring framework — not a hard override that ignores everything else.

### Signal 5 — Popularity tiebreak (tiny)

The Google Fonts API returns fonts sorted by popularity. The algorithm uses each font's rank as a tiny inverse weight — popular fonts get a small nudge.

```js
score += Math.max(0, (200 - candidateRank) / 1000);
```

**Why:** When scores tie, prefer fonts users are more likely to recognize and have used before. The weight is small enough that it never overrides real signal — it just breaks ties.

---

## What about fonts without tags?

Of the ~900 Google Fonts, only ~75 are tagged in `FONT_META`. For everything else, the algorithm derives basic tags from the font's category:

```js
'serif':       { moods: ['classic'],   uses: ['body-text'] },
'sans-serif':  { moods: ['minimal'],   uses: ['body-text', 'ui-app'] },
'display':     { moods: ['bold'],      uses: ['display'] },
'handwriting': { moods: ['playful'],   uses: ['branding'] },
'monospace':   { moods: ['clean'],     uses: ['ui-app'] },
```

This means *every* font gets reasonable suggestions — just less nuanced for the uncurated ones. Fonts with rich tags get specific pairings; fonts without get category-driven ones.

---

## The variety guarantee

Without a guard, the top 3 scores might all be the same category (e.g. three different serifs). That's not a useful type system.

So after scoring, the algorithm checks: do the top 3 picks include at least 2 different categories? If they all share one, the lowest-scoring pick gets swapped for the highest-scoring font from a different category.

**Why:** A pairing should give the user real range — a serif and a sans, not two flavors of the same thing.

---

## A worked example

Say the user picks **Playfair Display** (serif, tagged: *elegant*, *classic*, *bold*; uses: *display*, *body-text*, *branding*).

Now let's score **Lato** as a candidate (sans-serif, tagged: *minimal*, *modern*, *warm*; uses: *body-text*, *branding*, *ui-app*):

| Signal | Result | Points |
|---|---|---|
| Category contrast | serif + sans-serif = complementary | **+5** |
| Mood overlap | no shared moods | 0 |
| Use-case complement | Playfair is display-ish, Lato is body-text → match | **+2** |
| Curated bonus | Lato is in `PAIRING_MAP["Playfair Display"]` | **+6** |
| Popularity | Lato is ~rank 5 in Google Fonts | ~0.2 |
| **Total** | | **~13.2** |

Lato scores about 13.2. Other top candidates (Source Sans 3, Raleway) score similarly. The algorithm picks the top 3 and verifies they span at least 2 categories. Done — that's what shows up on the pairings page.

---

## Why this approach

A few alternatives were considered and rejected:

- **Just hand-pick everything** — doesn't scale. ~900 fonts × 3 pairings each = 2,700 decisions to maintain by hand.
- **Visual font analysis** (x-height, stroke contrast, etc.) — would require rendering fonts to a canvas and reading pixel data. Heavy, brittle, and offline-unfriendly for a single-file static app.
- **ML / crowdsourced recommendations** — overkill for a tool that runs entirely in your browser.

The tag-based scoring approach is a sweet spot: it uses real typographic principles (category contrast, mood, use-case roles), it's transparent and editable, it works for every font, and the curated map preserves hand-picked taste where it matters most.

---

## Where to find this in the code

All of this lives in [fontface/index.html](../fontface/index.html). The key pieces:

| Name | What it does |
|---|---|
| `FONT_META` | Mood + use-case tags for ~75 popular fonts |
| `CATEGORY_DEFAULT_TAGS` | Coarse tag fallbacks for untagged fonts |
| `COMPLEMENTARY_CATEGORIES` | Which categories pair well together |
| `PAIRING_MAP` | Hand-curated pairings for ~65 fonts |
| `getMetaFor(font)` | Returns the tags for a font (or category defaults) |
| `scorePairing(primary, candidate, rank)` | Computes the score |
| `getPairings(primary)` | The main entry — scores all candidates, returns top 3 with variety enforced |
| `getPairingsByFamily(family)` | Wrapper used in step 4's dropdown logic |

If you want to tweak the system, the most impactful places to edit are:

- **Adjust signal weights** in `scorePairing` — make category contrast count more, or curated picks count less, etc.
- **Add tags** to `FONT_META` — every font you tag gets nuanced pairings instead of category-default ones
- **Add curated pairings** to `PAIRING_MAP` — fastest way to override the algorithm for specific fonts

Everything is pure JavaScript with no external dependencies. The whole pairing system is about 100 lines of code.
