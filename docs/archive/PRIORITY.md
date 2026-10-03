# Priority — Highest Impact First

_Deadline: August 10. Optimize for hiring-manager impression at Bosch / ASELSAN / Roketsan / TİSAŞ / Mercedes-Benz / Porsche / BMW and similar engineering-led product companies._

## Done (compressed — see `MEMORY.md` / `PROJECT_STATUS.md` for detail if needed)

All 9 case studies built and verified (Urn, Herptile, Rockhounder, Delta, Retroscent, REX, plus the original Pioneer/Spiegelau/Razor). Behance reference-portfolio audit applied (merged disclosure sections, verified Tools lines, full-bleed hero images, hiring-signal home order). Full EN/DE/TR translation of all 9 case studies, verified. ROV title wording, duplicate-site question, a Retroscent factual overclaim, Alias/CATIA removal, and TUS internship dates — all fixed (2026-07-09).

## Active — PDF/slide-deck portfolio

1. **Full 53-slide skeleton done** at `pdf/index.html` (2026-07-10): Cover, CV, Contents, 5 flagships × 6 pages, Other Selected Work × 20 pages. Structure approved through iterative feedback; sketch/ideation + additional-detail pages are placeholder slots.
2. **8 of 15 placeholders already filled from the archive** (2026-07-10 overnight, all images verified visually — see PROJECT_STATUS.md). **7 slots still need Bedirhan's scans**: Pioneer sketch, Rockhounder sketch + extra, REX sketch, Delta sketch, Razor extra, Retroscent sketch. Upload to `assets/img/<project>/` — will now happen from the Germany PC (see `HANDOFF-GERMANY.md`).
0. **FIRST on the Germany PC: Netlify deploy** — drag `Desktop\netlify-linux.zip` (2026-07-11 build) onto app.netlify.com Deploys. Fixes live descriptions + removes publicly exposed internal docs.
3. Then: final pass + PDF export via browser print (print CSS ready: `@page 1400px 900px`, one slide per page).
4. Standalone CV PDFs still need Alias/CATIA removed and intern dates fixed — blocked, no Python on this machine; Bedirhan fixes at source or we regenerate from the new HTML deck later.

_Note: an earlier version of this file said never to adopt a slide-deck layout, Space Grotesk, or a CV-as-cover-page — Bedirhan explicitly reversed that 2026-07-09 after seeing a reference he liked. That guidance is void; the slide deck above is the current direction._

## Active — Website visual overhaul (after the PDF deck settles)

4. Reference-portfolio-informed polish: ~~more white space between case-study sections~~ (done 2026-07-11: 96px desktop / 64px mobile), ~~trim overlong paragraphs (Urn, Herptile) ~30%~~ (done 2026-07-11: 7 worst paragraphs, all 3 languages; `cs.urn.arastirma.p` left as-is), annotated arrow+label callouts on mechanism/assembly images (Delta hinge, REX standoffs, Rockhounder panels), consistent render backgrounds where multiple renders exist per project.
5. Image container / aspect-ratio review per project — pick each image's natural best ratio rather than forcing one everywhere. Don't touch the `#nihai` full-bleed treatment, already correct.
6. Render consistency pass — reuse/crop existing renders before generating anything new; log real gaps in `RENDER_QUEUE.md`.
7. Thumbnail redesign on the home grid, only where a thumbnail doesn't communicate the project at a glance.
8. "Other Work" gallery for Automotive Design sketches — after the above.
9. `robots.txt` → `Allow: /` once visual pass + gallery are done.
10. Global hiring-manager critique pass + "How I Work" capabilities section redesign — last, judges the finished site.
11. `build.py` path fix — nice for maintainability, not blocking.

## Standing flags

- TUS Metallbau: blocked on company URL (do not guess) + Bedirhan's next Germany trip for CAD files.
- Retroscent pafta origin: assumed AI/Photoshop-made, softened the DFM claim, still unconfirmed which project exactly.
- Decided against as full case studies: Kickboard, Citizen Science device, Modelmaking I/II.
