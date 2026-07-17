---
name: visual-audit
description: Use this skill when auditing, critiquing, or triaging visual assets on Bedirhan's portfolio — hero renders, product photography, hand sketches, technical drawings, prototype photos, exploded views. Apply portfolio-grade criteria: does this image belong on a hire-me page for engineering-led product companies, or does it hurt the reader's trust in the designer. Load whenever the working directory is this repo and images are being reviewed, chosen, replaced, retouched, or CSS-treated. Complements bedirhan-portfolio and frontend-design.
---

## What this skill does

A portfolio-grade image is one that a hiring manager at Bosch, ASELSAN, Mercedes or Porsche can look at for two seconds and think "this person builds real things". Anything short of that hurts. This skill gives the rubric for that judgment, plus the concrete moves when an image fails.

The audit is honest, not encouraging. A weak render is weaker than no render at all — negative space is on-brand for this site; filler is not.

## The seven checks

Run every image against these, in order. First fail is enough to flag the asset.

1. **Subject clarity.** Can a stranger identify the object in half a second? A cropped bracket, an in-progress sketch corner, or an ambiguous rendered blob all fail. Product photography and hero renders should show the whole object, oriented so its function reads immediately.
2. **Lighting integrity.** Renders: does the light behave physically — one clear key, believable shadows, no HDRI over-glow. Photos: no phone-flash flatness, no yellow tungsten cast on a "clean product" shot, no mixed color temperature. Sketches: pencil pressure and ink weight consistent, not muddy from a phone camera.
3. **Background discipline.** Product renders sit on a neutral seamless background or a documented environment. No default gray studio gradient with radial vignette. Sketches show clean paper, not a lit desk photo of a page. Prototype photos: garage floor / cluttered workbench = flag unless the mess *is* the point (materials study, in-context test).
4. **Resolution and compression.** Long edge ≥ 1600 px for a hero, ≥ 1200 px for a case-study frame, ≥ 800 px for a thumbnail. No JPEG blocking around high-contrast edges, no visible chroma banding. WebP at quality 82 – 88 is the target.
5. **Color grade coherence.** Across a single case study, all images share one grade (white balance, black point, saturation). Mixing a neutral CAD render with a warm phone snapshot on the same page reads as a scrapbook, not a portfolio.
6. **Portfolio-grade craft signal.** Does the image itself demonstrate the discipline the caption claims? An exploded view claims CAD skill — it must be a real assembly explosion, not a labeled screenshot with drop shadows. A hand sketch claims sketching ability — proportions, perspective, and line confidence all count.
7. **Honesty match.** If the caption says "prototype" the image is a prototype, not a render. If the caption says "concept sketch" it is not a render with pencil filter applied. Mismatch destroys credibility harder than a weak image would.

## Verdict categories

After the seven checks, sort each asset into exactly one bucket.

- **Portfolio-grade.** Ships as is.
- **CSS-recoverable.** Grade issue only — desaturate + neutral background overlay + hard crop can bring it up. Fix in CSS, do not reshoot. Note the exact CSS treatment.
- **Reframe / re-crop.** Composition problem, pixels are fine. Give the target crop box.
- **Reshoot / re-render.** Craft or lighting is the problem. Specify the target: camera + lens + light setup for a photo, or engine + camera + light rig for a render.
- **Cut.** Not fixable in reasonable time before deadline; the page is stronger without it. Explicitly recommend removal.

## Voice for critique

Direct, technical, no encouragement padding.

- Name the specific defect, not "could be better".
- Give the fix (or removal) in one sentence.
- Never call a bad image "interesting" or "unique". A hiring manager will not.
- Bedirhan can take honest feedback; do not soften on his behalf.

## When you deliver the audit

Structure the report as a table: `file` · `bucket` · `defect` · `fix in one line`. No preamble, no summary paragraph. If a case study has more than three flagged images, flag the case study itself for a Layer-style visual reset rather than image-by-image fixes.

## What this skill does NOT do

- It does not repaint sketches or re-render CAD models. I cannot open Blender, KeyShot, Photoshop or a scanner. When the verdict is "reshoot / re-render", the actual work is Bedirhan's; this skill gives the brief.
- It does not judge captions or copy. Content-side critique lives in `bedirhan-portfolio`.
- It does not choose motion or layout. Layout / motion critique lives in `frontend-design` and the V2 audit doc.
