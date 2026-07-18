# Voynich Spatial Data

**Every token of the Voynich Manuscript's Nine Rosettes foldout (f85v–f86r), positioned and oriented on the page — free to download, verify, and build upon.**
To our knowledge this is the first complete machine-readable positioned transliteration of the Rosettes page; no prior public dataset covers it ([survey](https://github.com/voynichese/voynichese) — the closest project, voynichese.com, excludes this folio by design and stores no orientation).

Explore it live (read-only, no login): **https://voynich-sh.netlify.app/overlay.html?folio=f85v_86r** — six view modes: original page, drawings-only, transcription labels, ductus variants, digital EVA glyphs, Latin gloss.

## What is in here

| Path | Format | Contents |
|---|---|---|
| `rosettes/overlay_f85v_86r.json` | JSON | The positioned transliteration: 539 tokens with position, rotation, size and mask geometry, plus per-paragraph transforms |
| `rosettes/tokens_f85v_86r.csv` | CSV | Same tokens flattened, one row per token — easiest entry point for analysis |
| `rosettes/poly_transforms_f85v_86r.csv` | CSV | Per-paragraph crop→folio transforms |
| `rosettes/polygons_f85v_86r.json` | JSON | The 46 paragraph/region segmentation shapes (rings, ellipses, freeform) |
| `rosettes/gallows/f85v_86r_P*.json` | JSON ×46 | Raw tracings per region: per-glyph gallows polygons, ductus-variant attributions, word baseline vectors (`tokenVecs`) |
| `rosettes/transcription_placa_f85v_86r.txt` | TXT | The Rosettes transliteration in Placa reading order |
| `corpus/placa_transcription_full.json` | JSON | Full-manuscript working transliteration (Placa corpus) |
| `ductus/variants_config.json` | JSON | The ductus-variant taxonomy (K/T/P/F × grades 1/2/3) with canonical exemplar references |
| `interpretation/latin_gloss_f85v_86r.json` | JSON | **Interpretive layer** — per-token Latin glosses from the KACHOOM compositional dictionary. Working hypothesis, not established reading |
| `VERSION.json` | JSON | Snapshot date, source commit, counts |

## Coordinate frames (read this before using the data)

- **Overlay tokens** (`overlay_*.json`, `tokens_*.csv`): `x_px, y_px` are pixel coordinates on the folio image, size **2412 × 2375** for f85v–f86r (Beinecke scan crop). `angle_deg` is the label baseline rotation, degrees, clockwise-positive in screen frame (y grows downward). `0°` = left-to-right horizontal.
- **Gallows tracings** (`gallows/*.json`): coordinates live in that paragraph's **crop frame** (width normalized to 3600 px). To map a crop point to the folio: `folio_x = origin_x + crop_x / scale + offset_dx` (same for y) using that paragraph's row in `poly_transforms_*.csv`.
- **`tokenVecs`**: per-token word baseline vectors, `a` = start, `e` = end (crop frame). Orientation of the token = `atan2(e.y − a.y, e.x − a.x)`.
- **Ductus variants**: anchored to the feet at the gallows stem base — `X-1` = one right foot, `X-2` = two feet, `X-3` = no feet (X ∈ K, T, P, F).

## Method, in two lines

Region shapes, per-glyph gallows outlines and word baseline vectors were hand-traced on registered natural/UV image pairs in a purpose-built browser tool; label positions and rotations were then hand-placed and fine-tuned token by token over the page image. Every edit is versioned; this repository is a dated snapshot of that live dataset.

## License and attribution

- **Spatial data, tracings and annotations**: © Alessandro Placa (Uroboro) — released under **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Use it, remix it, publish with it — just credit.
- **Transliteration layer**: derives from the community EVA transliterations — Takeshi Takahashi's transcription and, for the Rosettes foldout, **Zandbergen–Landini ZL3b** — with editorial corrections and reading order by A. Placa. Credit them when reusing the text layer.
- **Manuscript images are not included** (Beinecke Rare Book & Manuscript Library, Yale — MS 408, public domain scans available from Yale).

## Cite as

> Placa, A. (2026). *Voynich Spatial Data: positioned transliteration and ductus annotations of Beinecke MS 408, including the Nine Rosettes foldout.* https://github.com/alessandroplaca-uro/voynich-spatial-data

Questions, corrections, collaborations: open an issue here.
