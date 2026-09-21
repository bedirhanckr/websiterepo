# Maintaining the static language pages

The root HTML files (`index.html`, `contact/index.html`, `work/*.html`) and
`assets/js/i18n.js` remain the editable sources. English keeps the existing
URLs. `de/` and `tr/` are generated static pages, with translated HTML,
metadata, canonical URLs, reciprocal hreflang links and localized navigation.
They work without JavaScript. Existing `?lang=de` and `?lang=tr` URLs redirect
in the browser to the corresponding pages, retaining other queries and anchors.
Explicit language URLs take precedence over browser or saved preferences.

After editing source HTML or translations, regenerate and check:

```sh
python -m pip install -r scripts/requirements-locales.txt
python scripts/build_locales.py
python scripts/check_locales.py
node --check assets/js/main.js
node --check assets/js/i18n.js
```

Node is used only to read the existing JavaScript translation dictionary;
lxml parses the HTML. Commit generated files alongside their source edits.
Vercel continues serving static files; no hosting migration or runtime build
is required. Existing CV language routes and the PDF page are preserved.

The checks cover all 33 pages, local assets and anchor links, reciprocal
canonical language alternates, metadata consistency, navigation language,
project coverage, sitemap entries, and deterministic regeneration. They do
not measure responsive rendering, contrast, or Core Web Vitals.
