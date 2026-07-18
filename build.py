#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Portfolyo statik site üreticisi.
Her sayfayı iki biçimde üretir:
  - /site/*.html            (klasör yapısı, harici CSS/JS — hosting için)
  - /site-standalone/*.html (CSS+JS+i18n gömülü — her yerde açılır)
Ortak header/footer/dil-seçici tek yerde tanımlı → kod tekrarı yok.
"""
import pathlib, re, base64, mimetypes, shutil

ROOT = pathlib.Path(__file__).parent.resolve()
OUT_HOSTED = ROOT
OUT_STANDALONE = ROOT / "site-standalone"

CONTACT = {
    "email": "bedirhanckr.id@gmail.com",
    "linkedin": "https://linkedin.com/in/bedirhanckr",
    "behance": "https://behance.net/bedirhanckr",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">')

def header(prefix):
    return f'''<a class="skip-link" href="#main" data-i18n="skip">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{prefix}index.html">Bedirhan Çakıroğlu<small data-i18n="brand.role">Industrial Designer / Design Engineer</small></a>
    <div style="display:flex; align-items:center;">
      <nav class="primary-nav" id="primary-nav">
        <a href="{prefix}index.html" data-i18n="nav.work">Work</a>
        <a href="{prefix}about.html" data-i18n="nav.about">About</a>
        <a href="{prefix}index.html#contact" data-i18n="nav.contact">Contact</a>
      </nav>
      <div class="lang-switch" role="group" aria-label="Language">
        <button data-lang="en" aria-pressed="true">EN</button><span class="sep">/</span><button data-lang="de" aria-pressed="false">DE</button><span class="sep">/</span><button data-lang="tr" aria-pressed="false">TR</button>
      </div>
      <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>'''

def footer(prefix, back="footer.otherwork"):
    return f'''<footer class="site-footer" id="contact">
  <div class="wrap">
    <div class="cols">
      <div>
        <span class="dim-mark" data-i18n="nav.contact">Contact</span>
        <p style="margin-top:10px; font-size: var(--fs-500); color: var(--ink-900);" data-i18n="footer.cta">Let's build something.</p>
        <p class="footer-quote" data-i18n-html="footer.quote">"Good design is as little design as possible."<span>— Dieter Rams</span></p>
      </div>
      <div class="contact-links">
        <p><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></p>
        <p><a href="{CONTACT['linkedin']}" target="_blank" rel="noopener"><span data-i18n="contact.linkedin">LinkedIn</span> ↗</a></p>
        <p><a href="{CONTACT['behance']}" target="_blank" rel="noopener"><span data-i18n="contact.behance">Behance</span> ↗</a></p>
        <p style="margin-top:12px;"><a href="{prefix}index.html#work" data-i18n="{back}">Other work →</a></p>
      </div>
      <form class="contact-form" id="contact-form">
        <input type="text" name="name" data-i18n-placeholder="contact.form.name" placeholder="Name" required>
        <input type="email" name="email" data-i18n-placeholder="contact.form.email" placeholder="Email" required>
        <textarea name="message" data-i18n-placeholder="contact.form.message" placeholder="Message" rows="3" required></textarea>
        <button type="submit" data-i18n="contact.form.send">Send →</button>
        <p class="form-note" data-i18n="contact.form.note">Opens your email client with this pre-filled.</p>
      </form>
    </div>
    <p class="legal" data-i18n="footer.legal">© Bedirhan Çakıroğlu. Paderborn, Germany.</p>
  </div>
</footer>'''

def page(title, desc, prefix, body, back="footer.otherwork"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{FONTS}
<link rel="stylesheet" href="{prefix}assets/css/tokens.css">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>
<body>
{header(prefix)}
{body}
{footer(prefix, back)}
<script src="{prefix}assets/js/i18n.js"></script>
<script src="{prefix}assets/js/main.js"></script>
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>'''

# ---- sayfa gövdeleri ayrı dosyalarda tutuluyor (bodies/ klasörü) ----
def load_body(name):
    return (ROOT / "bodies" / f"{name}.html").read_text()

PAGES = [
    # (çıktı yolu, prefix, title, desc, body-adı, back-key)
    ("index.html", "", "Bedirhan Çakıroğlu — Industrial Designer / Design Engineer",
     "Industrial designer and design engineer working with manufacturing in mind. Underwater robotics, product design and steel structure projects.",
     "home", "footer.otherwork"),
    ("about.html", "", "About — Bedirhan Çakıroğlu",
     "Bedirhan Çakıroğlu — Industrial Designer / Design Engineer. Background in mechatronics, underwater robotics and steel structure design.",
     "about", "footer.backwork"),
    ("work/pioneer-mk2.html", "../", "Pioneer Mk2 — Underwater Explorer Nose Module | Bedirhan Çakıroğlu",
     "Nose module design for the Pioneer Mk2 underwater explorer — hydrodynamic shell and sensor mounting bracket. TEKNOFEST Design & Presentation Award.",
     "pioneer", "footer.backwork"),
    ("work/spiegelau.html", "../", "Spiegelau — Champagne Glass Design | Bedirhan Çakıroğlu",
     "A three-product champagne family for Spiegelau — chiller, flute and coupe. Full process from ideation sketches to technical drawing.",
     "spiegelau", "footer.backwork"),
    ("work/urn.html", "../", "Urn — Hot Drink Station | Bedirhan Çakıroğlu",
     "A hot drink station that runs on a transit card and builds neighborhood belonging.",
     "urn", "footer.backwork"),
    ("work/rockhounder.html", "../", "Rockhounder | Bedirhan Çakıroğlu",
     "ITU Graduation Project, 2nd Prize. A weekend rockhounding camp equipment bag, from CAD surface to paper pattern to a real fabric mock-up tested outdoors.",
     "rockhounder", "footer.backwork"),
    ("work/herptile.html", "../", "Herptile — Pregnancy Pilates Station | Bedirhan Çakıroğlu",
     "A pilates station and reformer for safe exercise during pregnancy, designed as a product and service system from sheet-metal engineering to app-based coaching.",
     "herptile", "footer.backwork"),
    ("work/delta.html", "../", "Delta — Kinematic Furniture Mechanism | Bedirhan Çakıroğlu",
     "A telescopic hinge mechanism that transitions a single body between working and reclining positions. Design for Export finalist.",
     "delta", "footer.backwork"),
    ("work/razor.html", "../", "Philips MG7720 Redesign — Repairability Engineering | Bedirhan Çakıroğlu",
     "Redesigning the battery and charging experience of a cordless shaver so it can be repaired instead of thrown away. Teardown, foam prototyping, CAD.",
     "razor", "footer.backwork"),
    ("work/retroscent.html", "../", "Retroscent — FURNITUR 2023 Award | Bedirhan Çakıroğlu",
     "An organic, mixed-material seating piece awarded Prize & Mention at FURNITUR 2023 by Türkiye Tasarım Vakfı.",
     "retroscent", "footer.backwork"),
    ("work/rex-tank.html", "../", "REX — Tracked Mini Robot Kit | Bedirhan Çakıroğlu",
     "An Arduino-based tracked mini robot kit designed during a Robotistan internship, sold as a real product with its own assembly guide.",
     "rex-tank", "footer.backwork"),
]

def build_hosted():
    for out, prefix, title, desc, body_name, back in PAGES:
        html = page(title, desc, prefix, load_body(body_name), back)
        p = OUT_HOSTED / out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)
    print(f"hosted: {len(PAGES)} sayfa yazıldı")

def inline_assets(html, prefix):
    """Harici CSS/JS/görselleri gömerek standalone hale getir."""
    tokens = (ROOT/"assets/css/tokens.css").read_text()
    style  = (ROOT/"assets/css/style.css").read_text()
    i18n   = (ROOT/"assets/js/i18n.js").read_text()
    mainjs = (ROOT/"assets/js/main.js").read_text()

    # CSS linklerini kaldır, tek <style> ekle
    html = re.sub(r'<link rel="stylesheet" href="[^"]*tokens\.css">', '', html)
    html = html.replace(f'<link rel="stylesheet" href="{prefix}assets/css/style.css">',
                        f'<style>\n{tokens}\n{style}\n</style>')
    # JS scriptlerini kaldır, tek <script> ekle
    html = html.replace(f'<script src="{prefix}assets/js/i18n.js"></script>', '')
    html = html.replace(f'<script src="{prefix}assets/js/main.js"></script>',
                        f'<script>\n{i18n}\n{mainjs}\n</script>')

    # görselleri base64 göm
    def repl(m):
        src = m.group(1)
        if src.startswith("data:") or src.startswith("http"): return m.group(0)
        # prefix'i çöz
        rel = src
        img_path = (ROOT / rel.replace(prefix, "")) if prefix and rel.startswith(prefix) else (ROOT / rel.lstrip("./"))
        # work/ alt sayfalarda ../assets → assets
        candidates = [
            ROOT / rel.replace("../", ""),
            ROOT / rel.lstrip("./"),
        ]
        for c in candidates:
            if c.exists():
                mime = mimetypes.guess_type(str(c))[0] or "image/jpeg"
                data = base64.b64encode(c.read_bytes()).decode()
                return m.group(0).replace(src, f"data:{mime};base64,{data}")
        return m.group(0)
    html = re.sub(r'src="([^"]+\.(?:jpe?g|png|webp))"', repl, html)
    # linkleri standalone dosya adlarına çevir (work/x.html → x.html, ../index.html → index.html)
    html = html.replace('href="work/', 'href="')
    html = html.replace('href="../index.html', 'href="index.html')
    html = html.replace('href="../about.html', 'href="about.html')
    html = html.replace('href="index.html', 'href="index.html')
    return html

def build_standalone():
    OUT_STANDALONE.mkdir(parents=True, exist_ok=True)
    for out, prefix, title, desc, body_name, back in PAGES:
        html = page(title, desc, prefix, load_body(body_name), back)
        html = inline_assets(html, prefix)
        # düz dosya adı (work/ kaldır)
        flat = out.replace("work/", "")
        (OUT_STANDALONE / flat).write_text(html)
    print(f"standalone: {len(PAGES)} sayfa yazıldı")

if __name__ == "__main__":
    build_hosted()
    build_standalone()
