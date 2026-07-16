---
name: bedirhan-portfolio
description: Use this skill whenever working on Bedirhan Çakıroğlu's industrial-design / design-engineering portfolio at bedirhancakiroglu.com — including hero anatomy, work grid restructures, case-study rebalancing, principles copywriting, typography choices, motion refinement, and any redesign-v2 iteration. Prioritize large project imagery, verifiable outcomes, and one-section-at-a-time change over broad rewrites. Applies even when the user does not explicitly mention Bedirhan or the portfolio, as long as the working directory is this repo.
---

## What this is

An industrial designer and design engineer's portfolio, not a developer portfolio. The subject is Bedirhan Çakıroğlu — mechanical / product design, CAD, DFM/DFA, prototyping, real hardware. Documented work includes: Pioneer MKII underwater ROV nose module (TEKNOFEST Design & Presentation Award), Rockhounder recreational rock-collecting product (İTÜ 2nd Best Graduation Project), REX Mini Tank (shipped commercially through Robotistan with its own assembly catalog), Delta convertible furniture, Retroscent scent furniture (FURNITUR 2023 award), and TUS Metallbau balcony / canopy / glass-facade systems.

Target readers are hiring managers at engineering-led product companies — Bosch, ASELSAN, Roketsan, TİSAŞ, Mercedes-Benz, Porsche, BMW. Every design decision should read as if it was made for that audience.

Pair this skill with the parent `frontend-design` skill. This one supplies the subject; that one supplies the method.

## Reference language (principles only, never copy)

Draw only design principles from the following studios. Never copy their layouts, typography, palette, or brand marks.

- **Marc Newson — image-led simplicity.** The product photography and render *are* the design. Text stays minimal and out of the way. Each project gets enormous negative space around it. The site behaves like a catalog, not an essay. Tone: quiet, confident, obviously made by someone who does not need to explain themselves.
- **Layer — engineering + industrial-design storytelling.** Process is visible: sketches, prototypes, materials, mechanisms. Case studies explain why *this* material, why *this* manufacturing method, how *this* mechanism works. Technical vocabulary (tolerance, DFM, HiCAD, sheet bending, injection molding) is used deliberately when it carries information. A case study is an engineering narrative, not a mood board.
- **Karim Rashid — project rhythm and variety.** Projects do not have to look identical. A high-precision underwater vehicle and a piece of convertible furniture deserve different presentations. Rhythm and light category signals help the viewer navigate the variety without flattening it.

## Never do

- **Developer-portfolio aesthetics.** Dark terminal backgrounds, monospace body text, code-editor UI chrome, syntax highlighting theatre, "npm install my-thoughts" jokes. This is not that.
- **Glassmorphism, blobs, neon accents, gradient hero backgrounds, animated background noise, floating particles.** All of them read "AI-generated in 2025" instantly.
- **Excessive animation.** Multiple parallax layers, cursor-follow shimmer, character-by-character title reveal, full-screen intro sequence, scroll-hijack storytelling. See the `frontend-design` guidance on motion; err smaller.
- **Templated defaults.** Warm cream + terracotta serif combo, near-black + acid green accent, hairline broadsheet layouts. See `frontend-design` for the full list. Do not spend the design's freedom on these.
- **Invent project facts.** If a tolerance value, an award year, a manufacturing partner, or an engineering detail is not documented in the archive or in Bedirhan's own words, leave it out. Mark unverified claims `[TO CONFIRM]` on the page. See the Retroscent case, which states "no full-scale prototype exists" directly — that honesty is a credibility asset, not a bug.

## Always do

- **Large project imagery is the visual foundation.** Hero renders, product photography, and process shots dominate the visual weight of every layout. UI ornament and text chrome stay under ~10 % of the visual budget.
- **Surface manufacturing and engineering decisions.** When a project involved sheet bending, injection molding, glass-facade detailing, or specific CAD tooling, name it. Recruiters at engineering companies read the site for those signals.
- **Preserve the current V1 identity.** V1 earned a Braun/Rams-adjacent token system: grayscale + `#C1401F` signal red, Inter + JetBrains Mono, 8 px spacing rhythm, `--nihai-bg` deliberately dark for the case-study finale. V2 evolves this system; it does not replace it. Every new choice should feel like the same designer six months later, not a different agency.
- **Surface the verified rosettes.** TEKNOFEST Design & Presentation Award, İTÜ 2nd Best Graduation Project, FURNITUR 2023 award, REX shipped commercially through Robotistan. These belong in the visual hierarchy, not buried mid-paragraph.
- **Keep EN/DE/TR trilingual support.** The three-language build is a hire signal for the German market. Any new UI copy needs matching keys in `assets/js/i18n.js` for all three locales. A single unescaped straight quote in that file has already killed language switching once — verify `typeof window.I18N === 'object'` after every edit.
- **Honor `prefers-reduced-motion`.** Every motion rule must ship with a reduce-motion override, matching the existing pattern in `assets/css/style.css`.

## Working rules

**Modify one section at a time.** The V2 redesign rolls out as V2.1 → V2.7, each version touching only one section (Hero → Typography → Work grid → Case study → About + Capabilities → Footer → Motion refinement). Never touch two sections in the same PR. The ordered roadmap lives at `docs/exports/2026-07-16-redesign-v2-audit.html`.

**Protect `main`. Work only on the local `redesign-v2` branch.** Never push V2 code to `main`. Never overwrite V1. When Bedirhan approves an individual V2.x, it merges via its own PR under that version tag; otherwise it stays local.

**Show, don't push.** For V2 previews, publish a Claude Code artifact (HTML). Never deploy a V2 preview to a live URL.

**Reading order for a fresh session.** `docs/redesign-v2/00-brief.md` → `docs/exports/2026-07-16-redesign-v2-audit.html` → this file → the sibling `frontend-design` skill → the target section's current HTML/CSS in the repo. Do not skip.

## Copy voice

Bedirhan writes in first-person, industrial-designer-plain. Rules:

- **No marketing adjectives.** Never *passionate, innovative, cutting-edge, world-class, groundbreaking*. Cut on sight.
- **Em-dash only for quote attribution or category-code labels.** Never as a clause connector — a comma or a period does the job better.
- **Prefer verbs over nouns.** "I bent sheet metal for the enclosure" beats "sheet-metal enclosure implementation."
- **Prefer specifics over abstractions.** Numbers (tolerance, weight, jury rank, unit count), materials, tools, partner names — these earn trust. Abstractions (system-thinking, holistic, user-centered) drain it.
- **State weakness plainly.** "Foam-only prototype", "no full-scale test", "AI-generated technical drawing — flagged as such" all belong on the page and increase credibility.
- **When in doubt, cut.** A short case study is stronger than a padded one.

## Session start protocol

At the start of a fresh session, before any tool call:

1. Confirm the working directory is this repo.
2. Read the five files in the "reading order" above.
3. If Bedirhan has queued a next V2.x version, state it back and wait for approval before writing code.
4. If unclear which V2.x is next, ask.
