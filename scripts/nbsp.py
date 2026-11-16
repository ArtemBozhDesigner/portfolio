#!/usr/bin/env python3
"""Keep short words off the ends of lines.

Inside <main> of each given page the script puts a non-breaking space:
  - after every one- and two-letter word and after the short function words
    listed in WORDS (so a line never ends with "a", "of", "to", "the", "and"),
    also when a comma follows the word ("made of, a product");
  - around "×" and before "→";
  - before the last word of a paragraph, heading or list item (so the last
    line never holds a single word).

Run from the repo root after editing the text of a page:

    python3 scripts/nbsp.py writing/references-and-benchmarks.html

The script owns every &nbsp; inside <main>: it removes the old ones first,
so running it twice gives the same file.
"""
import re
import sys

WORDS = ['the', 'and', 'for', 'but', 'nor', 'per', 'via']
SHORT = r'(?:[A-Za-z]{1,2}|' + '|'.join(WORDS) + r')'
BEFORE = r"(?<![A-Za-z0-9’'\-/.])"
GLUE_RE = re.compile(BEFORE + r'(' + SHORT + r'[,;]?)[ \t\r\n]+(?=\S)', re.I)
GLUE_END_RE = re.compile(BEFORE + r'(' + SHORT + r')[ \t\r\n]+$', re.I)
INLINE_OPEN_RE = re.compile(r'<(?:strong|em|b|i|a|span|code)\b', re.I)
BLOCK_CLOSE_RE = re.compile(r'</(?:p|li|h[1-6]|figcaption)>', re.I)
NBSP = '&nbsp;'


def fix_text(text, next_token):
    if not text.strip():
        return text
    text = text.replace(NBSP, ' ').replace(' ', ' ')
    text = GLUE_RE.sub(lambda m: m.group(1) + NBSP, text)
    text = re.sub(r'[ \t]+×[ \t]+', NBSP + '×' + NBSP, text)
    text = re.sub(r'[ \t]+→', NBSP + '→', text)
    if INLINE_OPEN_RE.match(next_token):
        text = GLUE_END_RE.sub(lambda m: m.group(1) + NBSP, text)
    if BLOCK_CLOSE_RE.match(next_token) and len(text.split()) >= 2:
        head, sep, tail = text.rstrip().rpartition(' ')
        if sep and tail and NBSP not in tail:
            text = head + NBSP + tail
    return text


def fix_page(source):
    # Scripts and styles are kept whole, every other tag is a token of its own
    tokens = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', source, flags=re.S | re.I)
    in_main = False
    for i, token in enumerate(tokens):
        if token.startswith('<'):
            name = re.match(r'</?\s*([a-zA-Z0-9]+)', token)
            if name and name.group(1).lower() == 'main':
                in_main = not token.startswith('</')
            continue
        if in_main:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else ''
            tokens[i] = fix_text(token, next_token)
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
