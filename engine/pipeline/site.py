"""Build the GitHub Pages player site (GitHub's web UI cannot play mp4 files).

python pipeline/site.py VAULT ROOT OUT_DIR
-> OUT_DIR/index.html, videos.json, .nojekyll   (published to the gh-pages branch by publish.sh)

The page lists every problem (search / filter by study path and difficulty) and plays a video with ?v=<repo path>.
Videos stay in the main branch; the page downloads the mp4 from raw.githubusercontent.com and plays it from a
blob URL (raw serves mp4 as application/octet-stream, which some browsers refuse to stream directly).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import organize as O  # noqa: E402
import repo  # noqa: E402

VAULT, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
ctx = O.Ctx(VAULT, ROOT)
site = O.SITE

hot = {str(x['num']) for x in json.load(open(os.path.join(O.ENGINE, 'hot100.json'), encoding='utf-8'))}
sets = json.load(open(os.path.join(O.ENGINE, 'sets_full.json'), encoding='utf-8'))
SET_TAG = {'面试经典 150 题': '面试经典150', 'LeetCode 热题 173 道': '热题173', '字节跳动 · 近 30 天高频': '字节高频',
           '字节跳动 · 近 3 个月高频': '字节高频', '字节跳动 · 近 6 个月高频': '字节高频'}
set_of = {}
for name, rows in sets.items():
    tag = SET_TAG.get(name)
    if tag:
        for r in rows:
            set_of.setdefault(str(r[0]), set()).add(tag)

items = []
for it in ctx.items:
    e = {'i': it['id'], 't': it['title'], 'd': it.get('diff') or '', 'f': repo.folder(it)}
    if it.get('rating'):
        e['r'] = int(float(it['rating']))
    for a, k in (('ling', 'l'), ('yiduobo', 'y')):
        if ctx.has_video(it, a):
            e[k] = repo.video(it, a)
        if it.get(a):
            e[k + 's'] = repo.solution(it, a)
    al = O.ling_alias_video(ctx, it)
    if al:
        e['la'] = [os.path.relpath(al[0], ROOT), al[1]]
    tags = list(it.get('paths') or [])
    if it['id'] in hot:
        tags.append('Hot100')
    tags += sorted(set_of.get(it['id'], ()))
    if tags:
        e['p'] = tags
    items.append(e)

concepts = sorted(f'分类概念视频/{f}' for f in os.listdir(os.path.join(ROOT, '分类概念视频')) if f.endswith('.mp4'))
data = {'owner': site['owner'], 'repo': site['repo'], 'branch': site.get('branch', 'main'),
        'concepts': concepts, 'items': items}
json.dump(data, open(os.path.join(OUT, 'videos.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(open(os.path.join(HERE, 'site_index.html'), encoding='utf-8').read())
nv = sum(('l' in e) + ('y' in e) for e in items) + len(concepts)
print(f'site: {len(items)} problems, {nv} videos -> {OUT}')
