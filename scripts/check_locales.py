#!/usr/bin/env python3
"""Check committed locale pages, navigation, metadata and generation stability."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import subprocess
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://bedirhancakiroglu.com'
SOURCES = [Path('index.html'), Path('contact/index.html'), *sorted(Path('work').glob('*.html'))]
PAGES = [Path(prefix) / p for prefix in ('', 'de', 'tr') for p in SOURCES]
errors = []
def check(condition, message):
    if not condition: errors.append(message)
def route(path):
    return '/' + path.as_posix().removesuffix('index.html').rstrip('/') if path != Path('index.html') else '/'
def target(value, current):
    parts = urlsplit(value)
    path = ROOT / unquote(parts.path).lstrip('/') if parts.path else ROOT / current
    if path.is_dir(): path /= 'index.html'
    return path, parts.fragment

docs={path:html.parse(str(ROOT/path)) for path in PAGES}
for path,doc in docs.items():
    lang=path.parts[0] if path.parts[0] in ('de','tr') else 'en'
    label=str(path)
    check(doc.getroot().get('lang')==lang, label+': incorrect HTML language')
    check(doc.getroot().get('data-static-locale')==lang,label+': missing static locale')
    check(doc.xpath('//link[@rel="canonical"]/@href')==[ORIGIN+route(path)],label+': incorrect canonical')
    check(doc.xpath('//meta[@property="og:url"]/@content')==[ORIGIN+route(path)],label+': incorrect og:url')
    title=doc.xpath('//title/text()')
    check(title==doc.xpath('//meta[@property="og:title"]/@content')==doc.xpath('//meta[@name="twitter:title"]/@content'),label+': inconsistent sharing title')
    check(bool(doc.xpath('//meta[@name="description"]/@content')),label+': missing description')
    alternates={el.get('hreflang'):el.get('href') for el in doc.xpath('//link[@hreflang]')}
    check(set(alternates)=={'en','de','tr','x-default'},label+': missing alternates')
    check(len(set(alternates.values()))==3,label+': alternates must be distinct')
    for language,url in alternates.items():
        dest,_=target(url,path)
        check(dest.exists(),label+': alternate missing '+url)
        if dest.exists():
            alternate_doc=html.parse(str(dest))
            check(alternate_doc.xpath('//link[@rel="canonical"]/@href')==[url],label+': alternate is not canonical '+url)
    check(len(doc.xpath('//*[contains(@class,"lang-switch")]/a'))==3,label+': language links must work without JS')
    check(bool(doc.xpath('//noscript[@data-locale-fallback]')),label+': no-JS reveal fallback missing')
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        import json
        json.loads(node.text)
    for el in doc.xpath('//*[@href or @src or @srcset]'):
        values=[el.get(attr) for attr in ('href','src') if el.get(attr)]
        if el.get('srcset'): values += [part.strip().split()[0] for part in el.get('srcset').split(',')]
        for value in values:
            parts=urlsplit(value)
            if parts.netloc or parts.scheme: continue
            dest,fragment=target(value,path)
            check(dest.exists(),label+': missing asset/link '+value)
            if fragment and dest.suffix=='.html' and dest.exists():
                parsed=html.parse(str(dest))
                check(bool(parsed.xpath('//*[@id=$id]',id=fragment)),label+': missing anchor '+value)
            if el.tag=='a' and not el.get('data-lang') and parts.path:
                relative=dest.relative_to(ROOT)
                if relative in PAGES:
                    dest_lang=relative.parts[0] if relative.parts[0] in ('de','tr') else 'en'
                    check(dest_lang==lang,label+': navigation changes language '+value)

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
site=etree.parse(str(ROOT/'sitemap.xml'))
urls=site.xpath('//s:loc/text()',namespaces=ns)
check(len(urls)==len(set(urls)),'duplicate sitemap URLs')
for path in PAGES: check(ORIGIN+route(path) in urls,'missing sitemap page '+str(path))
for prefix in ('','de','tr'):
    d=docs[Path(prefix)/'index.html']
    check(len(d.xpath('//a[contains(@class,"project-card") or contains(@class,"sw-card")]'))==9,'home must retain all nine projects')
    check(not d.xpath('//section[@class="featured-work"]'),'duplicate featured-work collection')
    check(bool(d.xpath('//*[@class="hero-actions"]/a[contains(@href,"contact")]')),'missing hero contact action')

# The second generation must not accumulate locale prefixes, alter source
# facts, or drift the sitemap. This also exercises translation completeness.
tracked=[ROOT/p for p in PAGES]+[ROOT/'sitemap.xml']
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
subprocess.run(['python','scripts/build_locales.py'],cwd=ROOT,check=True)
for p in tracked:check(before[p]==hashlib.sha256(p.read_bytes()).hexdigest(),'generation drift: '+str(p.relative_to(ROOT)))
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(PAGES)} pages; metadata, reciprocal alternates, links/assets, anchors, language-preserving navigation, nine projects and reproducible generation.')
