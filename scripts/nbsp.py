#!/usr/bin/env python3
"""Keep short words off the ends of lines.

Inside <main> and <nav> of a page the script puts a non-breaking space:
  - after every one- and two-letter word and after the short function words
    of the page language listed in WORDS (so a line never ends with "a", "of",
    "the", "und", "pro", "для"), also when a comma follows the word;
  - around "×", before "→" and before a dash;
  - in Russian, before the particles "бы", "ли", "же";
  - before the last word of a paragraph, heading or list item (so the last
    line never holds a single word).

The language is read from <html lang="...">. scripts/build-i18n.py runs this
for the pages listed in its NBSP_PAGES; to run it by hand:

    python3 scripts/nbsp.py writing/references-and-benchmarks.html

The script owns every &nbsp; inside <main> and <nav>: it removes the old ones first,
so running it twice gives the same file. <pre>, <script> and <style> are left alone.
"""
import re
import sys

WORDS = {
    'en': ['the', 'and', 'for', 'but', 'nor', 'per', 'via'],
    'de': ['der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'und', 'für', 'mit', 'von', 'bei', 'aus', 'auf', 'vor', 'zur', 'zum', 'bis', 'wie', 'als'],
    'cs': ['pro', 'při', 'nad', 'pod', 'bez', 'ale', 'aby', 'ani', 'než'],
    'ru': ['без', 'для', 'над', 'под', 'при', 'про', 'обо', 'изо', 'или', 'что', 'как', 'чем'],
}
LETTER = r'[^\W\d_]'
BEFORE = r"(?<![\w’'\-/.])"
INLINE_OPEN_RE = re.compile(r'<(?:strong|em|b|i|a|span|code)\b', re.I)
BLOCK_CLOSE_RE = re.compile(r'</(?:p|li|h[1-6]|figcaption)>', re.I)
NBSP = '&nbsp;'


def rules(lang):
    short = r'(?:' + LETTER + r'{1,2}|' + '|'.join(WORDS.get(lang, [])) + r')'
    glue = re.compile(BEFORE + r'(' + short + r'[,;]?)[ \t\r\n]+(?=\S)', re.I)
    glue_end = re.compile(BEFORE + r'(' + short + r')[ \t\r\n]+$', re.I)
    return glue, glue_end


def fix_text(text, next_token, lang, glue, glue_end):
    if not text.strip():
        return text
    text = text.replace(NBSP, ' ').replace(' ', ' ')
    text = glue.sub(lambda m: m.group(1) + NBSP, text)
    text = re.sub(r'[ \t]+×[ \t]+', NBSP + '×' + NBSP, text)
    text = re.sub(r'[ \t]+([→—–])', NBSP + r'\1', text)
    if lang == 'ru':
        text = re.sub(r'[ \t]+(бы|ли|же)(?=[ \t,.;:!?)]|$)', NBSP + r'\1', text)
    if INLINE_OPEN_RE.match(next_token):
        text = glue_end.sub(lambda m: m.group(1) + NBSP, text)
    if BLOCK_CLOSE_RE.match(next_token) and len(text.split()) >= 2:
        head, sep, tail = text.rstrip().rpartition(' ')
        if sep and tail and NBSP not in tail:
            text = head + NBSP + tail
    return text


def fix_page(source):
    lang = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', source)
    lang = lang.group(1).lower()[:2] if lang else 'en'
    glue, glue_end = rules(lang)
    # Scripts, styles and <pre> blocks are kept whole, every other tag is a token of its own
    tokens = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<pre\b.*?</pre>|<[^>]+>)', source, flags=re.S | re.I)
    in_main = False
    for i, token in enumerate(tokens):
        if token.startswith('<'):
            name = re.match(r'</?\s*([a-zA-Z0-9]+)', token)
            if name and name.group(1).lower() in ('main', 'nav'):
                in_main = not token.startswith('</')
            continue
        if in_main:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else ''
            tokens[i] = fix_text(token, next_token, lang, glue, glue_end)
    return ''.join(tokens)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        with open(path, encoding='utf-8') as f:
            source = f.read()
        result = fix_page(source)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'{path}: {result.count(NBSP)} non-breaking spaces')


if __name__ == '__main__':
    main()
