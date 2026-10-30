"""Sanity checks for the repo before pushing to GitHub.

python pipeline/check_repo.py ROOT [--fix-names]
- broken relative links in every .md (target file/folder must exist)
- leftover Obsidian wikilinks [[...]] that point into the vault
- file names that are illegal or awkward on Windows / GitHub (: * ? " < > | trailing space or dot)
- files over 50 MB (GitHub warns at 50 MB, rejects at 100 MB)
"""
import os
import re
import sys
from urllib.parse import unquote

ROOT = sys.argv[1]
SKIP_DIRS = {'_work', '.git', '__pycache__', '.obsidian'}
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^)\s]+)\)|!\[[^\]\n]*\]\(([^)\s]+)\)')
FENCE = re.compile(r'```.*?```', re.S)
WIKI = re.compile(r'\[\[((?:灵茶山艾府题解|yiduobo题解|hot_100|hot100动画|题单动画|灵神科学刷题|Python刷题函数|题目讲解)[^\]]*)\]\]')
BAD_CHARS = set(':*?"<>|\\')

broken, wikis, names, big = [], [], [], []
n_md = n_links = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for name in dn + fn:
        if any(c in BAD_CHARS for c in name) or name != name.rstrip(' .'):
            names.append(os.path.relpath(os.path.join(dp, name), ROOT))
    for f in fn:
        p = os.path.join(dp, f)
        if os.path.getsize(p) > 50 * 2**20:
            big.append(os.path.relpath(p, ROOT))
        if not f.endswith('.md'):
            continue
        n_md += 1
        text = FENCE.sub('', open(p, encoding='utf-8', errors='replace').read())
        for m in LINK.finditer(text):
            t = m.group(1) or m.group(2)
            if re.match(r'^[a-z]+:', t) or t.startswith('#'):
                continue
            n_links += 1
            target = unquote(t.split('#')[0])
            if target.startswith('<') and target.endswith('>'):
                target = target[1:-1]
            if not os.path.exists(os.path.normpath(os.path.join(dp, target))):
                broken.append((os.path.relpath(p, ROOT), t))
        for m in WIKI.finditer(text):
            wikis.append((os.path.relpath(p, ROOT), m.group(1)[:80]))

print(f'{n_md} markdown files, {n_links} relative links')
print(f'broken links: {len(broken)}')
for x in broken[:25]:
    print('  ', x)
print(f'vault wikilinks left: {len(wikis)}')
for x in wikis[:10]:
    print('  ', x)
print(f'awkward file names: {len(names)}')
for x in names[:15]:
    print('  ', x)
print(f'files > 50 MB: {len(big)}', big[:5])
