#!/usr/bin/env python3
"""Build the translated pages.

English pages in the repo root are the source. Text marked with data-i18n="key"
(and attributes listed in data-i18n-attrs="attr:key") is replaced with the
strings from i18n/<lang>.json and written to /<lang>/<page>.

Pages listed in NBSP_PAGES also get non-breaking spaces after short words,
in every language (scripts/nbsp.py).

Run from the repo root after any change to a page or a dictionary:

    python3 scripts/build-i18n.py

The build stops with an error if a key is missing from a dictionary or a
dictionary holds a key no page uses.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbsp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'about.html', 'writing.html', 'writing/references-and-benchmarks.html']
# Pages whose text gets non-breaking spaces after short words (see scripts/nbsp.py)
NBSP_PAGES = {'writing/references-and-benchmarks.html'}
# (code, label on the button, name in the list, word for "Language")
LANGS = [
    ('en', 'EN', 'English'),
    ('de', 'DE', 'Deutsch'),
    ('cs', 'CS', 'Čeština'),
    ('ru', 'RU', 'Русский'),
]
SOURCE = 'en'
SOURCE_STRINGS = {'lang.label': 'Language'}

TEXT_RE = re.compile(r'<(\w+)\b([^<>]*?)\sdata-i18n="([^"]+)"([^<>]*)>(.*?)</\1>', re.S)
ATTR_TAG_RE = re.compile(r'<\w+\b[^<>]*\sdata-i18n-attrs="([^"]+)"[^<>]*>')
SWITCHER_RE = re.compile(r'  <!-- lang-switcher:start -->\n.*?  <!-- lang-switcher:end -->\n', re.S)
HREF_RE = re.compile(r'href="(/[^"]*)"')


def page_path(page):
    return '' if page == 'index.html' else page[:-len('.html')]


def url(lang, page):
    path = page_path(page)
    if lang == SOURCE:
        return '/' + path
    return '/' + lang + ('/' + path if path else '')


def switcher(lang, page, label_word):
    code = next(c for l, c, _ in LANGS if l == lang)
    name = next(n for l, _, n in LANGS if l == lang)
    items = []
    for l, _, n in LANGS:
        current = ' aria-current="true"' if l == lang else ''
        items.append(f'      <a class="lang-item" href="{url(l, page)}" hreflang="{l}" lang="{l}"{current}>{n}</a>')
    return (
        '  <!-- lang-switcher:start -->\n'
        '  <div class="lang" data-lang>\n'
        f'    <button class="lang-button" type="button" aria-expanded="false" aria-controls="lang-menu" aria-label="{html.escape(label_word)}: {name}">\n'
        '      <span class="lang-globe" aria-hidden="true"></span>\n'
        f'      <span class="lang-code" aria-hidden="true">{code}</span>\n'
        '    </button>\n'
        '    <div class="lang-menu" id="lang-menu" hidden>\n'
        + '\n'.join(items) + '\n'
        '    </div>\n'
        '  </div>\n'
        '  <!-- lang-switcher:end -->\n'
    )


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def collect_source(pages):
    """English strings by key, taken from the pages themselves."""
    strings = dict(SOURCE_STRINGS)
    for page, text in pages.items():
        for m in TEXT_RE.finditer(text):
            strings[m.group(3)] = m.group(5)
        for m in ATTR_TAG_RE.finditer(text):
            for pair in m.group(1).split():
                attr, key = pair.split(':', 1)
                value = re.search(r'\s' + re.escape(attr) + r'="([^"]*)"', m.group(0))
                if not value:
                    sys.exit(f'{page}: attribute {attr} for key {key} not found')
                strings.setdefault(key, html.unescape(value.group(1)))
    return strings


def translate(text, lang, strings, page, used):
    def get(key):
        if key not in strings:
            sys.exit(f'{lang}: key "{key}" (used in {page}) is missing from i18n/{lang}.json')
        used.add(key)
        return strings[key]

    def text_sub(m):
        return f'<{m.group(1)}{m.group(2)} data-i18n="{m.group(3)}"{m.group(4)}>{get(m.group(3))}</{m.group(1)}>'

    def attr_sub(m):
        tag = m.group(0)
        for pair in m.group(1).split():
            attr, key = pair.split(':', 1)
            value = html.escape(get(key), quote=True)
            tag = re.sub(r'(\s' + re.escape(attr) + r'=")[^"]*(")', lambda a: a.group(1) + value + a.group(2), tag, count=1)
        return tag

    def href_sub(m):
        path = m.group(1)
        if path.startswith('/assets/'):
            return m.group(0)
        return f'href="/{lang}{"" if path == "/" else path}"'

    text = text.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    text = TEXT_RE.sub(text_sub, text)
    text = ATTR_TAG_RE.sub(attr_sub, text)
    text = HREF_RE.sub(href_sub, text)
    return text


def main():
    pages = {page: read(page) for page in PAGES}
    for page, text in pages.items():
        if len(SWITCHER_RE.findall(text)) != 1:
            sys.exit(f'{page}: language switcher markers not found')

    source = collect_source(pages)
    write('i18n/en.json', json.dumps(dict(sorted(source.items())), ensure_ascii=False, indent=2) + '\n')

    for lang, _, _ in LANGS:
        if lang == SOURCE:
            for page, text in pages.items():
                out = SWITCHER_RE.sub(lambda m: switcher(lang, page, source['lang.label']), text)
                write(page, nbsp.fix_page(out) if page in NBSP_PAGES else out)
            continue
        strings = json.loads(read(f'i18n/{lang}.json'))
        used = {'lang.label'}
        for page, text in pages.items():
            out = translate(text, lang, strings, page, used)
            out = SWITCHER_RE.sub(lambda m: switcher(lang, page, strings['lang.label']), out)
            write(f'{lang}/{page}', nbsp.fix_page(out) if page in NBSP_PAGES else out)
        extra = sorted(set(strings) - used)
        if extra:
            sys.exit(f'{lang}: keys not used by any page: {", ".join(extra)}')
        missing = sorted(set(source) - set(strings))
        if missing:
            sys.exit(f'{lang}: keys missing: {", ".join(missing)}')
        print(f'{lang}: {len(PAGES)} pages, {len(strings)} strings')


if __name__ == '__main__':
    main()
