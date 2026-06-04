# Mini Project 2: Type System Builder
## Task List

---

### Build Approach

This tool will be built with an **agent-assisted coding platform** rather than writing it manually from scratch. The goal is to focus on design decisions and prompting while the platform generates most of the code.

- **Primary platform:** **Claude Code** — full subscription, keeps the project as a standalone local file in this repo, fits the "no backend / no dependencies / runs locally" constraints
- **Optional comparison:** Bolt or Lovable — limited access, so used (if at all) for a single small experiment to compare agent-assisted approaches in the `mp2.md` reflection
- **My role:** define requirements, prompt the agent, review/refine output, test the result

### Phase 0 — Set Up Build Platform
- [ ] Confirm Claude Code is set up and can create/edit files in the `Week 8` folder
- [ ] Draft an initial prompt describing the tool (use `mp2_project_declaration.md` as the source of truth)
- [ ] (Optional) Spend a small amount of Bolt/Lovable credits on one UI experiment to compare, for the reflection
- [ ] Note the platform decision and reasoning in `mp2.md`

### Phase 1 — Setup & Data
- [ ] Get a Google Fonts API key and test that it returns font data
- [ ] Explore the Google Fonts API response: understand what fields are available (family name, category, variants/weights)
- [ ] Define the mood and use case tags to layer on top of API data (e.g. playful, minimal, editorial, brand, body text)
- [ ] Build a small mapping of font families → mood/use case labels to power filtering

### Phase 2 — Core UI (index.html)
- [ ] Set up the single HTML file with basic structure (header, step sections, preview area, export area)
- [ ] Build Step 1: filter panel (category, mood, use case) that narrows the font list
- [ ] Display filtered font results as a selectable list or card grid
- [ ] Build Step 2: primary font selection — user picks one font from filtered results
- [ ] Build Step 3: pairing suggestions — show 2–3 compatible fonts once primary is selected
- [ ] Build Step 4: paired font selection — user picks one pairing

### Phase 3 — Preview
- [ ] Load selected fonts dynamically via Google Fonts embed links
- [ ] Build the preview panel with consistent sample text: title, heading, and body copy
- [ ] Wire up the "Preview this pairing" button to render the preview
- [ ] Style the preview panel so it looks clean and readable

### Phase 4 — Type System Export
- [ ] Build the type system summary panel (typeface, paired typeface, weights, size scale, use case labels)
- [ ] Add an export option — at minimum, a copyable text block or downloadable `.txt` / `.css` snippet
- [ ] Test the full flow end-to-end: filter → select → pair → preview → export

### Phase 5 — Polish & Submission
- [ ] Review UI for decision paralysis — simplify any step that feels overwhelming
- [ ] Add helper text and labels so each step is self-explanatory
- [ ] Test in browser (Chrome + Safari at minimum)
- [ ] Write `mp2.md` reflection documenting what was built, decisions made, and limitations — including which build platform (Claude Code / Bolt) I used and how agent-assisted coding shaped the result
- [ ] Final check: API key not exposed, file runs locally by opening in browser

---

### Nice-to-Haves (if time allows)
- [ ] Let the user customize the preview sample text
- [ ] Add a size scale suggestion (e.g. 12/14/16/24/32/48px) based on use case
- [ ] Show a small specimen of each font in the filter results before selecting
