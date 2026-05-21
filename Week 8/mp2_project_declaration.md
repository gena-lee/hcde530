# Mini Project 2: Type System Builder
## Project Declaration

### Problem
Font selection is a slow, often overwhelming part of the design process. Designers spend significant time browsing typefaces without a clear way to filter by design intent or know which fonts will work together. This tool addresses that by giving users a structured, guided way to find and pair fonts — and walk away with a usable type system.

### Users
Anyone working on a design project — professional designers, students, or people building personal brands. Users may not have a strong design background, so the tool needs to guide rather than overwhelm. The interaction should feel approachable enough to complete in roughly 30 minutes.

### Data
The tool pulls font data from a font API (Google Fonts is the likely candidate). Each font is organized by attributes including typeface category, mood, use case, and weight options. Users can filter by these attributes to narrow their options. Once a primary font is selected, the tool suggests compatible pairings for a second font.

### Definition of Done
A user can open the tool, filter fonts by design intent, select a primary and paired font, and export a complete type system — including typeface, weight, size scale, and use case (e.g. display, body, caption) — that they can bring directly into a brand or design project.

Once a pairing is selected, the tool renders a live visual preview using consistent sample text: a brand name (title), a short tagline (heading), and a sentence or two of placeholder copy (body). The preview loads the actual fonts via Google Fonts embeds so users see the real typefaces rendered in the browser — no image generation required. A "Preview this pairing" button triggers the preview to keep the interaction simple and avoid overwhelming the user before they're ready.

### Constraints
- Built with agent-assisted coding (low manual coding required)
- Simple, focused UI that minimizes choices at each step to reduce decision paralysis
- No backend or login required — runs locally or as a standalone file
- Avoids external dependencies where possible to keep setup easy
- Font API selection TBD; should be free and well-documented
