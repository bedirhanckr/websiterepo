# Render Style Guide

_All hero images and case study renders should follow this guide so that the portfolio reads as a single publication, not a collection of separate projects._

---

## 1. Camera

**Primary view — 3/4 perspective**
- Horizontal rotation: 30–40° from front-facing
- Vertical elevation: 12–18° above eye level
- This reveals the primary face, one side panel, and enough of the top surface to read the object's volume
- Lens: 85–100mm equivalent (slight telephoto, minimal perspective distortion)
- No fisheye. No extreme wide-angle. No overhead bird's-eye unless the project's function requires it.

**Secondary views (within case study sections)**
- Orthographic front, top, or side: for technical/engineering sections only (CAD, DFM, mechanism detail)
- Close-up detail: 50–60mm equivalent, focused on joint, mechanism, or surface texture
- Keep secondary views consistent within each project; don't mix 3 different elevation angles in one section

**What to avoid**
- Dead-center symmetrical front view for hero shots (reads as product catalogue, not design thinking)
- Low-angle dramatic shots (products look theatrical, not engineered)
- Extreme overhead (only justified for flat objects like Spiegelau or pattern layouts)

---

## 2. Lighting

**Setup**
- Key light: upper-left, 45–50° elevation, 60–70° to the right of camera axis
- Fill light: opposite side, 50% key intensity, no hard shadow on the fill side
- Rim/edge light: slight backlight from upper-right at low intensity (5–15%) to separate the object from the background — optional, only where material contrast is low
- No colored lights. No dramatic HDRI environments with sky/sun visible.

**Character**
- Studio-style, soft diffuse key (large area light or softbox equivalent)
- Shadows: soft, present but not dominant. Shadow should confirm the object's volume, not compete with it.
- No pitch-black shadows. Minimum shadow fill ratio: 0.35.
- Specular highlights: tight and controlled. One clear highlight on the primary face. No blown-out white patches.

**What the lighting should feel like**
- Technical drawing rendered in 3D. Think Braun product photography from the 1960s: clean, no drama, all information.

---

## 3. Materials

**Default render material palette (when product material is abstract)**

| Surface type        | Appearance                          | Reflectivity |
|---------------------|-------------------------------------|--------------|
| Primary body        | Matte dark gray (#2A2B2E equivalent) | 0.05–0.08    |
| Secondary panels    | Satin mid-gray (#6B6F76 equivalent)  | 0.10–0.15    |
| Mechanical joints   | Brushed aluminum or matte black      | 0.12–0.18    |
| Accent / signal     | Signal red (#C1401F) matte           | 0.04         |

**Per-project overrides**
- Pioneer Mk2: orange FDM plastic body (real product colour), matte white sensor dome
- REX: clear/natural acrylic layers on dark chassis — translucency is authentic
- Delta: warm plywood (0.85 roughness), matte black telescopic joint
- Rockhounder: fabric texture (normal map from woven material) in dark olive/sand
- Razor: matte charcoal body + gloss-satin contrast on battery door seam

**What to avoid**
- Chrome or mirror finishes on non-metallic parts
- Subsurface scattering unless the material is genuinely translucent
- Procedural noise textures that read as "CGI" rather than "manufactured"

---

## 4. Background

**Standard: near-white warm neutral**
- Hex: #F5F4F1 (matches `--paper` token)
- Infinite floor setup: seamless curved backdrop (no visible horizon line)
- The background should be imperceptible — you should notice the product, not the environment

**Dark background: use only for nihai (final) full-bleed shots**
- Hex: #111214 (matches `--ink-900` token)
- The site's `#nihai` full-bleed treatment uses a dark ground. Renders destined for this slot should be lit for a dark context: slightly higher rim light, no ground shadow (shadow disappears into dark BG).

**What to avoid**
- Gradient backgrounds (brand blue to black, etc.)
- Environmental renders (rooms, countertops, hands holding the product) for hero/primary shots
  - Environmental context is fine for lifestyle supporting images in Prototip or Testler sections — those are photography, not CGI renders
- Coloured backdrops that echo the product colour

---

## 5. Composition

**Frame fill: 70–80%**
- The product should occupy 70–80% of the frame area
- Minimum 10% margin on all sides (breathing room)
- Never crop into the product at the frame edge

**Orientation**
- All hero images: horizontal (landscape)
- Never vertical/portrait for hero or thumbnail

**Visual weight**
- Primary face of the product should sit slightly left or right of centre — not dead-centre (centre-weighted compositions read as symmetrical product sheets, not design stories)
- 60/40 rule: if the product has a prominent feature (Pioneer sonar dome, REX sensor array, Delta mechanism joint), bias the composition so that feature is on the left third (reads first in LTR layouts)

**Multiple products / exploded views**
- Exploded views: maintain the same 3/4 camera angle; align parts along the primary axis (horizontal for long products, vertical for tall)
- Product family: same camera height, staggered depth (not aligned in a row)

---

## 6. Aspect Ratios

| Context                          | Ratio   | Notes                                              |
|----------------------------------|---------|----------------------------------------------------|
| Hero / thumbnail (home grid)     | 4 : 3   | `.thumb` class, 220px wide on desktop              |
| Single large media-slot          | 4 : 3   | Default `.media-slot` in case study sections       |
| Side-by-side media-grid pair     | 3 : 2   | Both images in the pair must use the same ratio    |
| Final nihai full-bleed           | 21 : 9  | Dark background render, site handles the crop      |
| PDF slide hero                   | 16 : 9  | 1400 × 900px, fits inside the slide canvas         |

Render at 2× resolution minimum:
- 4:3 at 1600 × 1200 px (for home thumbnail at 220px → crisp on any screen)
- 3:2 at 1800 × 1200 px (for media-grid pairs)
- 21:9 at 2520 × 1080 px (for nihai full-bleed)

---

## 7. Thumbnail Specification

The home grid thumbnail is the hiring manager's first three-second impression of each project.

**Rules**
- Always the 3/4 primary view (same angle used for the hero section)
- Product fills the frame — no empty space in the thumbnail
- Single product, no context props, no people, no text overlays
- Background: warm neutral (#F5F4F1) for all five flagships — visual consistency across the grid row
- Crop so that the most distinctive feature of the product is visible and not cut

**Per-project thumbnail brief**
- Pioneer Mk2: nose angled toward upper-left corner, torpedo form clearly readable, sensor dome prominent
- Rockhounder: bag in use posture (standing, straps tensioned), fabric texture visible, all compartments closed
- REX: slight top-down 3/4 to show chassis layers and sensor array; tracks in foreground
- Delta: mechanism in working position, hinge joint sharp, backrest and footrest implied
- Razor: vertical product, battery door visible on reverse face, charger dock in soft-focus background

---

## 8. What Makes This Portfolio's Render Style Distinctive

The renders should read as: **engineer who can visualise**. Not "visualiser who added some specs."

Every image should answer one of two questions:
1. What does this thing look like?
2. How does this thing work?

If an image answers neither, it doesn't belong in the case study.

Process images (hand sketches, foam prototypes, pool tests, pattern cutting) are treated differently: they are documentary photographs, not stylised renders. Never over-process or relight a photograph to match a render. The contrast between raw process documentation and clean final renders is intentional — it shows the journey.
