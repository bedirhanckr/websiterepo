# Memory — Architecture, Positioning, Reasoning

_Living project memory, kept compressed. `KARAR-GUNLUGU.md` in this folder is the original Turkish decision log, still valid background. This file holds only what's needed to resume work correctly — historical narration is pruned once it stops being decision-relevant._

## Mission

Bedirhan Çakıroğlu's industrial design / mechanical design engineering portfolio. Website is the master source; a PDF/slide-deck version (see below) is now being built in parallel from the same content. **Hard deadline: August 10.**

Target companies: Bosch, ASELSAN, Roketsan, TİSAŞ, Mercedes-Benz, Porsche, BMW, European product-dev/ID/design-engineering roles. Optimize for hiring managers.

## Operating mode

Bedirhan checks in briefly, mostly unavailable. Don't interrupt for small decisions — pick the strongest option. Only stop if a decision genuinely requires info that can't be inferred (identity of an unlabeled object/person; ask) vs. a judgment call between acceptable options (just decide). Maintain `PROJECT_STATUS.md` / `PRIORITY.md` / `MEMORY.md` / `RENDER_QUEUE.md`, updated as state changes. Compress these files after each major task — remove stale narration, keep only current state + load-bearing lessons.

## Positioning & writing rules

Present as **Industrial Designer & Mechanical Design Engineer** — CAD, product development, mechanical design, technical drawings, prototyping, DFM, engineering thinking. Never "just" a visual designer.

- No AI-sounding buzzwords (passionate, innovative, cutting-edge, world-class, etc).
- No em-dash as a clause connector — comma/period instead. Em-dash OK only for quote attribution or category-code labels ("RZ·21 — ...").
- Never invent facts. Unverifiable → mark `[TO CONFIRM]` and say so on the page. State real weaknesses (no full-scale test, foam-only prototype) honestly — builds credibility.
- Strip academic course codes/instructor names/term references.

## Site architecture

- Real root: `C:\Users\MONSTER\Desktop\portfolio-hosted\` (not `Desktop\files\`, a stale copy).
- `build.py` is broken on this machine (hardcoded Linux paths) — edit `bodies/*.html` **and** the built `work/*.html`/`index.html`/`about.html` by hand, they don't auto-sync.
- `assets/css/{tokens,style}.css` design tokens/components; `assets/js/i18n.js` EN/DE/TR dict keyed by `data-i18n`/`data-i18n-html`; `assets/js/main.js` lang switcher.
- Design language: Braun/Rams grayscale + signal red `#C1401F`, Inter + JetBrains Mono, "dim-mark" motif. No parallax/gradient/glassmorphism.
- Case study template (13 stages, `id` anchors + `case-subnav`): Problem → Araştırma → Kriterler → Konsept → Sketch → CAD → Mühendislik → DFM/DFA → Prototip → Testler → İterasyon → Nihai → Kazanım. Not every project uses all 13 (Spiegelau/Retroscent are shorter, honestly so).
- **i18n key pattern**: shared cross-project keys `cs.subnav.*`/`cs.eyebrow.*`/`cs.spec.*`/`cs.shared.result`; per-project `cs.<shortname>.<section>.<field>` (p=Pioneer, rock=Rockhounder, rex=REX, razor, hp=Herptile, urn, delta, sp=Spiegelau, retro=Retroscent). Numbered eyebrow prefixes ("01 — ") stay static/untranslated; only the label is wrapped. **Any string containing `<strong>`/`<br>` needs `data-i18n-html`, not `data-i18n`** — wrong one either strips formatting or escapes tags into visible text (bit us once on Spiegelau's `<h1>`).

## Project list — all 9 done

Pioneer Mk2, Spiegelau, Razor, Urn, Herptile, Rockhounder, Delta, Retroscent (8th, real FURNITUR 2023 award, intentionally shorter — no process docs exist, page says so), REX (9th, real shipped Robotistan product, found buried in `Stajlar/Robotistan Fabrika staj/Günler/Gün 20/`). Home order by hiring-signal strength: Pioneer → Rockhounder → REX → Razor → Herptile → Urn → Delta → Spiegelau → Retroscent. All fully translated EN/DE/TR (2026-07-09).

**Not built as case studies** (belong in the planned "Other Work" gallery instead, or excluded): Kickboard, Automotive Design sketches, Citizen Science device (identity unconfirmed), Modelmaking I/II. **Hard exclusions**: `chair soborg` (not original work), graphic-design folder (out of scope).

**Missing/blocked, waiting on Bedirhan**: Sim Racing Steering Wheel + 3D Printing product (not in archive, will upload separately). TUS Metallbau real projects (needs company URL — do not guess — + a future Germany trip for CAD files). Ground Control Box render for Pioneer addendum.

## Key lessons

- **Don't trust folder names.** Verify a sample image before writing copy — mismatched/unrelated content has turned up inside plausibly-named folders more than once (Razor's "otopsi" folder, "waterproof ideas" folder).
- **Verify CAD tool claims via file extension** (`.3dm`=Rhino, `.sldprt`=SolidWorks, `.blend`=Blender), never guess. Where no native files exist, ask Bedirhan directly rather than omit-or-guess.
- **Staging + Netlify zip are reproducible via `portfolio-hosted/rebuild-stage.ps1`** (added 2026-07-11 after `Desktop\portfolio-stage\` vanished mid-session). It derives the production subset (served HTML/CSS/JS + only referenced images + `pdf/index.html`) straight from portfolio-hosted and rebuilds `Desktop\netlify-linux.zip` with forward-slash entries. Don't hand-copy files into staging anymore — run the script (it also drops the ~42 unreferenced leftover images the old manual staging had accumulated). `bodies/home.html` is stale/unused (predates the 5-flagship curation); `index.html` is the authoritative served home file and is hand-edited.
- **After any i18n.js edit, verify `typeof window.I18N === 'object'` in a loaded page.** A single unescaped `"` inside any string (e.g. German „…" quotes pasted with a straight closing quote) is a silent site-wide kill: JS syntax error, no dict, every page falls back to hardcoded TR and language switching does nothing — pages still *look* fine. Happened 2026-07-10 (Delta DE description), caught 2026-07-11 just before deploy. Use `“` (U+201C) as the German closing quote or escape as `\"`.
- **Reference-portfolio comparisons: extract principles, deliver a structured critique, get explicit approval before applying.** This has happened twice now (a friend's Behance portfolio 2026-07-08; a "Nacho Castillo"-style minimal cover reference 2026-07-09) — both times the right move was analysis → approval → targeted transfer, not a silent redesign. **Bedirhan has since explicitly reversed the earlier "never adopt slide-deck/CV-cover-page" call** — see PDF deck section below.

## PDF / slide-deck portfolio (started 2026-07-09, skeleton complete 2026-07-10)

Parallel format at `portfolio-hosted/pdf/index.html`: self-contained single file, 1400×900 `.slide` units stacked vertically on a dark canvas, Braun tokens + signal red, Inter/JetBrains Mono with a Space Grotesk alt-font toggle (`data-font="alt"` on `<body>`).

**Structure — 53 slides (2026-07-10):**
- 1 Cover · 2 CV · 3 Contents (projects numbered 01–06, 30px red mono accent numbers, 400×88 thumbnails at 70% opacity, page ranges 04–09 / 10–15 / 16–21 / 22–27 / 28–33 / 34–53).
- Flagships × 6 pages each: cover → **sketch/ideation slot** → 2 detail pages → **additional-detail slot** → result. Order: Pioneer MKII, Rockhounder, REX Mini Tank, Delta, Electric Razor Redesign.
- Other Selected Work (20 pages): dark divider, then Herptile/Urn/Retroscent/Spiegelau at 3 pages each (existing mini-slide + sketch slot + extra slot), Kickboard 3 (2 existing + sketch slot), Automotive 3 (2 existing + extra slot), Awards summary.
- Sketch slots use `.sketch-box`, extra slots `.placeholder-box` — dashed borders, red "Placeholder" tag, note saying what goes there. **8 of 15 filled from archive 2026-07-10** (each image viewed and verified before use — the "don't trust folder names" rule paid off again: retroscent `orthographic.png` is actually a detail render, kickboard `w1.2` is market research not sketches, pioneer `ground box *.png` are raw CAD screenshots not portfolio-grade). **7 slots wait for Bedirhan**: Pioneer sketch, Rockhounder sketch+extra, REX sketch, Delta sketch, Razor extra, Retroscent sketch. Useful archive finds copied to clean paths: `razor/sketch-ideation.jpg`, `rex-tank/catalog-page-steps-{1-2,7-8}.jpg`.
- Portrait/instruction-page images in photo grids: add `fit-contain` class to the `.pg-cell` (object-fit:contain on light gray) instead of letting cover-crop eat the content.

**Conventions — don't fight the JS (all in the one `<script>` at file bottom):**
- **Never hardcode slide/page numbers in HTML** — JS generates everything at load: page numbers ("N / 53", top-right, `.slide-page-num`), deck labels ("Slide N — <name>" prepended to `.deck-label` text), per-project vertical page-indicator lines (from `data-page`/`data-total` attrs on each `.slide`; active line = longer + `#C1401F`), and red project-number badges 01–06 top-left (`projMap` id→number; **add new slide ids to `projMap` and set `data-page`/`data-total` when inserting slides**). Hardcoded numbers caused two rounds of duplicate/stale-number bugs before this was centralized.
- Indicator/badge colors are **hardcoded hex** (`#C1401F`, `#C8C5BE`), not `var(--signal)` — user reported tone inconsistency with the CSS variable across light/dark slide contexts.
- **Print CSS is in place**: `@page { size:1400px 900px; margin:0 }`, one slide per page, deck labels/font-toggle hidden. Export = Ctrl+P → Save as PDF → Margins None → Background graphics ON.
- **REX stays a flagship** (asked 2026-07-10, considered swapping with Herptile/Urn): it's the only shipped commercial product + the assembly-catalog/DFA story matches the TUS Metallbau role.
- Tools lines: Pioneer = Fusion 360 (model+render) · Photoshop; Rockhounder = Rhino · V-Ray · Photoshop; REX = Fusion 360 · Photoshop; Delta = SolidWorks (model) · Blender (render); Razor = Rhino (model) · KeyShot (render).

**Cover/CV details (approved):** cover = white card bottom-left, name/year split lines, no contact info, plus a signal-red crayon-textured SVG accent upper-right (two overlaid paths through `feTurbulence`+`feDisplacementMap`, works even in Artifact sandbox). CV = 2-column landscape from the old vertical CV PDFs; all contact info lives only here; content must fit 900px height. CAD skills read `HiCAD, SolidWorks, Rhino, Fusion 360` (Alias/CATIA removed everywhere; standalone CV PDFs still stale — no Python on machine, Bedirhan fixes at source). TUS internship = Jun 2023 – Dec 2023.

**Environment notes:** Artifact CSP blocks Google Fonts + relative image paths, so the deck looks broken *only* as an Artifact — use the dev server. **Port is 8021 now** (8010 and 8020 both got reserved by Windows) — `files/.claude/launch.json`. `files/.claude/serve.ps1` handles directory-index (`/pdf/` → `pdf/index.html`) since 2026-07-10.
