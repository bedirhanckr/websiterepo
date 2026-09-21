#!/usr/bin/env python3
"""Render the existing static pages in EN/DE/TR. Requires Python lxml and Node.

Edit the root HTML pages and assets/js/i18n.js, then run this script. Generated
DE/TR files are committed so Vercel still serves static files without a build.
English keeps its existing URLs; /de and /tr have independent canonical pages.
"""
from copy import deepcopy
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
import html as html_std
import json
import subprocess
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://bedirhancakiroglu.com'
LANGS = ('en', 'de', 'tr')
LOCALES = {'en': 'en_GB', 'de': 'de_DE', 'tr': 'tr_TR'}
PAGES = [ROOT / 'index.html', ROOT / 'contact/index.html', *sorted((ROOT / 'work').glob('*.html'))]

def page_path(path):
    value = '/' + path.relative_to(ROOT).as_posix()
    return value.removesuffix('index.html').rstrip('/') or '/'

PATHS = {page_path(p) for p in PAGES}

def localized(path, lang):
    return path if lang == 'en' else '/' + lang + (path if path != '/' else '')

def local_link(value, base, lang, navigation=False):
    if not value or value.startswith('#'):
        return value
    parsed = urlsplit(urljoin(ORIGIN + base, value))
    if parsed.scheme not in ('http', 'https') or parsed.netloc != urlsplit(ORIGIN).netloc:
        return value
    path = parsed.path
    if navigation:
        # Accept already-localized links when regenerating files.
        for prefix in ('/de/', '/tr/'):
            if path.startswith(prefix) and not path.startswith('/cv/'):
                path = path[len(prefix)-1:]
                break
        if path in ('/de', '/tr'):
            path = '/'
        path = path.removesuffix('index.html').rstrip('/') or '/'
        if path in PATHS:
            path = localized(path, lang)
        elif path in ('/cv', '/cv/de', '/cv/tr'):
            path = '/cv/' if lang == 'en' else '/cv/' + lang + '/'
    return urlunsplit(('', '', path, parsed.query, parsed.fragment))

def replace_inner(el, value, rich=False):
    for child in list(el):
        el.remove(child)
    el.text = None
    if not rich:
        el.text = html_std.unescape(value)
        return
    for part in html.fragments_fromstring(value):
        if isinstance(part, str):
            if len(el):
                el[-1].tail = (el[-1].tail or '') + part
            else:
                el.text = (el.text or '') + part
        else:
            el.append(part)

def plain(value):
    return ' '.join(html.fragment_fromstring(value.replace('<br>', ' '), create_parent=True).text_content().split())

def meta(head, name, value, property=False):
    attr = 'property' if property else 'name'
    found = head.xpath('./meta[@' + attr + '="' + name + '"]')
    el = found[0] if found else etree.SubElement(head, 'meta', {attr: name})
    el.set('content', value)

result = subprocess.run(['node', '-e', "const fs=require('node:fs'),vm=require('node:vm');const ctx={window:{}};vm.runInNewContext(fs.readFileSync('assets/js/i18n.js','utf8'),ctx);process.stdout.write(JSON.stringify(ctx.window.I18N));"], cwd=ROOT, check=True, capture_output=True, text=True)
DICTS = json.loads(result.stdout)
rendered = []

for source in PAGES:
    source_text = source.read_text()
    base = '/' + source.relative_to(ROOT).as_posix()
    route = page_path(source)
    for lang in LANGS:
        doc = html.document_fromstring(source_text)
        d = DICTS[lang]
        doc.set('lang', lang)
        doc.set('data-static-locale', lang)
        for attr, rich in [('data-i18n', False), ('data-i18n-html', True)]:
            for el in doc.xpath('//*[@' + attr + ']'):
                key = el.get(attr)
                if key not in d:
                    raise ValueError(f'Missing {lang} translation: {key} in {source.name}')
                replace_inner(el, d[key], rich)
        for el in doc.xpath('//*[@data-i18n-placeholder]'):
            el.set('placeholder', d[el.get('data-i18n-placeholder')])
        for el in doc.xpath('//*[@data-i18n-aria-label]'):
            el.set('aria-label', d[el.get('data-i18n-aria-label')])
        for el in doc.xpath('//button[contains(@class,"theme-toggle")]'):
            el.set('aria-label', d['ui.theme']); el.set('title', d['ui.theme'])
        for el in doc.xpath('//button[contains(@class,"nav-toggle")]'):
            el.set('aria-label', d['ui.menu'])
        for el in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," lang-switch ")]'):
            el.set('aria-label', d['ui.language'])
        # Resolve assets and navigation from each original document, not the
        # generated directory. Cross-page links stay in the selected language.
        for el in doc.iter():
            if not isinstance(el.tag, str): continue
            for attr in ('src', 'href', 'poster', 'action'):
                if el.get(attr):
                    el.set(attr, local_link(el.get(attr), base, lang, el.tag == 'a' and attr == 'href'))
            if el.get('srcset'):
                candidates=[]
                for candidate in el.get('srcset').split(','):
                    pieces=candidate.strip().split()
                    candidates.append(' '.join([local_link(pieces[0],base,lang), *pieces[1:]]))
                el.set('srcset', ', '.join(candidates))
        # Language links work without JavaScript and preserve the current page.
        for el in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," lang-switch ")]//*[@data-lang]'):
            target=el.get('data-lang'); el.tag='a'
            for attr in ('type', 'aria-pressed', 'aria-current', 'class'):
                el.attrib.pop(attr, None)
            el.set('href', localized(route,target));el.set('hreflang',target);el.set('lang',target)
            if target == lang:
                el.set('class','is-active');el.set('aria-current','true')
        head=doc.find('head')
        url=ORIGIN+localized(route,lang)
        if route == '/':
            title=d['seo.home.title'];description=d['seo.home.desc']
        elif route == '/contact':
            title=d['seo.contact.title'];description=d['seo.contact.desc']
        else:
            heading=doc.xpath('//h1')[0]
            title=plain(etree.tostring(heading,encoding='unicode',method='html',with_tail=False))+' | Bedirhan Çakıroğlu'
            lede=doc.xpath('//*[@data-i18n and contains(@data-i18n,".lede")]')[0].text_content()
            description=' '.join(lede.split())
            if len(description)>190:
                description=description[:187].rsplit(' ',1)[0]+'…'
        head.find('title').text=title
        meta(head,'description',description)
        for name,value in [('og:title',title),('og:description',description),('og:url',url),('og:locale',LOCALES[lang])]:meta(head,name,value,True)
        meta(head,'twitter:title',title);meta(head,'twitter:description',description)
        for el in head.xpath('./meta[@property="og:locale:alternate"]'):head.remove(el)
        for target in LANGS:
            if target != lang:etree.SubElement(head,'meta',{'property':'og:locale:alternate','content':LOCALES[target]})
        for el in head.xpath('./link[@rel="canonical" or @hreflang]'):head.remove(el)
        etree.SubElement(head,'link',{'rel':'canonical','href':url})
        for target in (*LANGS,'x-default'):
            etree.SubElement(head,'link',{'rel':'alternate','hreflang':target,'href':ORIGIN+localized(route,'en' if target=='x-default' else target)})
        for el in head.xpath('./script[@type="application/ld+json"]'):
            data=json.loads(el.text)
            def visit(node):
                if isinstance(node,list):
                    for item in node:visit(item)
                elif isinstance(node,dict):
                    if node.get('@type') in ('CreativeWork','ContactPage','WebPage'):
                        node.update({'url':url,'name':title.split(' | ')[0],'description':description,'inLanguage':lang})
                        if 'headline' in node:node['headline']=title.split(' | ')[0]
                    if node.get('@type')=='BreadcrumbList':
                        if '@id' in node:node['@id']=url+'#breadcrumb'
                        for item in node.get('itemListElement',[]):
                            if item.get('position')==1:item['name']=d['cs.crumb.home']
                            if item.get('position')==2 and route.startswith('/work/'):item['name']=d['nav.work']
                            if 'item' in item:item['item']=ORIGIN+local_link(item['item'],base,lang,True)
                    for value in node.values():visit(value)
            visit(data);el.text='\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n'
        # Static translations remain visible even when JavaScript is disabled.
        old=head.xpath('./noscript[@data-locale-fallback]')
        for el in old:head.remove(el)
        ns=etree.SubElement(head,'noscript',{'data-locale-fallback':''})
        etree.SubElement(ns,'style').text='[data-reveal]{opacity:1!important;transform:none!important}'
        output=source if lang=='en' else ROOT/lang/source.relative_to(ROOT)
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text('<!DOCTYPE html>\n'+etree.tostring(doc,encoding='unicode',method='html')+'\n')
        rendered.append((route,lang,url))

# Replace only the portfolio/contact records; keep the existing CV records.
sitemap=ROOT/'sitemap.xml'; tree=etree.parse(str(sitemap), etree.XMLParser(remove_blank_text=True)); ns='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'
root=tree.getroot()
image_ns='http://www.google.com/schemas/sitemap-image/1.1'
images={}
for entry in root:
    route=urlsplit(entry.findtext('{'+ns+'}loc') or '').path.rstrip('/') or '/'
    if route in PATHS:
        images[route]=[deepcopy(image) for image in entry.findall('{'+image_ns+'}image')]
for entry in list(root):
    loc=entry.findtext('{'+ns+'}loc') or ''
    if not urlsplit(loc).path.startswith('/cv'):
        root.remove(entry)
for route,lang,url in rendered:
    entry=etree.SubElement(root,'{'+ns+'}url');etree.SubElement(entry,'{'+ns+'}loc').text=url
    for target in (*LANGS,'x-default'):
        etree.SubElement(entry,'{'+xhtml+'}link',rel='alternate',hreflang=target,href=ORIGIN+localized(route,'en' if target=='x-default' else target))
    for image in images.get(route,[]):entry.append(deepcopy(image))
etree.indent(tree, space='  ')
sitemap.write_bytes(etree.tostring(tree,encoding='UTF-8',xml_declaration=True,pretty_print=True))
print(f'Rendered {len(rendered)} static pages and updated sitemap.xml.')
