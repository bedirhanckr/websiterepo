# Bedirhan Çakıroğlu portfolio — Claude working guide

_Concise entry point. Under 100 lines by design. Full guidance lives in the skills below._

## What this repo is

An industrial designer / design engineer's portfolio at **bedirhancakiroglu.com**. Static HTML/CSS/JS, no framework, no build. Vercel auto-deploys `main`. Hard deadline: **10 August 2026**.

## Skills — when to use each

Two project-level skills live under `.claude/skills/`:

- **`frontend-design`** — Anthropic's official design skill, preserved with a short repo adaptation. **Load whenever** touching visual design: aesthetic direction, tokens, typography, layout, motion, or reshaping any existing UI. This is the parent skill; every design decision passes through it first.
- **`bedirhan-portfolio`** — the subject-specific skill. **Load whenever** working on the site — redesign-v2 iterations, hero anatomy, work grid, case studies, principles, capabilities, or footer. Load it even if the user does not name Bedirhan or the portfolio, as long as the working directory is this repo. This skill sits on top of `frontend-design` and supplies the industrial-designer / design-engineer voice.

Load both together for any V2 work. `frontend-design` gives the method; `bedirhan-portfolio` gives the subject.

## Where to read for context

At the start of a fresh session, read these files in order:

1. `docs/redesign-v2/00-brief.md` — Bedirhan's V2 brief (role, rules, output format).
2. `docs/exports/2026-07-16-redesign-v2-audit.html` — 20-item audit, section reviews (rating 1–10), design direction manifesto, V2.1 → V2.7 roadmap, problems / opportunities / risks.
3. `.claude/skills/bedirhan-portfolio/SKILL.md` — subject and voice rules.
4. `.claude/skills/frontend-design/SKILL.md` — design method.
5. Any newer `docs/redesign-v2/<NN>-*.md` files Bedirhan added later (skills.md, brand notes, etc — in numeric order).

Older archive files still valid for project history: `MEMORY.md`, `PROJECT_STATUS.md`, `PRIORITY.md`, `KARAR-GUNLUGU.md`, `HANDOFF-GERMANY.md`. Read only if a decision references them.

## Working rules — non-negotiables

**Never touch `main` directly for V2 work.** V2 iterations happen on the local `redesign-v2` branch only. No push, no deploy, no PR to main from V2 until Bedirhan approves a specific version.

**Modify one section at a time.** V2 rolls out as V2.1 → V2.7. Each PR touches exactly one section (Hero → Typography → Work grid → Case study → About + Capabilities → Footer → Motion refinement). Never combine.

**Never invent project facts.** If a detail is not in Bedirhan's own words or the archive, either mark `[TO CONFIRM]` and ask him, or leave it out. The Retroscent-style "no prototype exists" disclosure is the reference for honest weakness statements.

**Preserve the current V1 identity.** V1 earned a Braun/Rams-adjacent design system (grayscale + `#C1401F` signal, Inter + JetBrains Mono, 8 px rhythm). V2 evolves it, never replaces it.

**Show, don't push.** For V2 previews, produce Claude Code HTML artifacts. Never deploy a V2 preview to a live URL.

## Session start protocol

Before any tool call in a fresh session:

1. Confirm the working directory is this repo.
2. Read the five files listed above, in order.
3. If Bedirhan has queued a next V2.x version, state it back and wait for approval before writing code.
4. If unclear which V2.x is next, ask.
