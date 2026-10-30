"""Build the master manifest of all solutions -> pending video jobs, in study-path order.

python manifest.py DATA_ROOT OUT.json
DATA_ROOT has 灵茶山艾府题解/solutions, yiduobo题解/solutions, labuladong速成路线图, 灵神科学刷题, videos.txt
"""
import json, os, re, sys, glob

ROOT, OUT = sys.argv[1], sys.argv[2]


def fm(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    d = {}
    if not m:
        return d
    for line in m.group(1).split('\n'):
        k, _, v = line.partition(':')
        v = v.strip()
        if v.startswith('['):
            try:
                v = json.loads(v)
            except Exception:
                pass
        elif v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        d[k.strip()] = v
    return d


def norm(qid):
    qid = str(qid).strip()
    return str(int(qid)) if qid.isdigit() else qid


def key(qid):
    return f'{int(qid):04d}' if qid.isdigit() else qid.replace(' ', '_')


def sortkey(qid):
    return (0, int(qid), '') if qid.isdigit() else (1, 0, qid)


P = {}  # id -> dict


def get(qid):
    return P.setdefault(qid, dict(id=qid, key=key(qid), title=None, diff=None, rating=None, ling=None, yiduobo=None,
                                  ling_py=False, yid_code=False, db=False, paths=[], done=[]))


for f in sorted(glob.glob(os.path.join(ROOT, '灵茶山艾府题解/solutions/*.md'))):
    t = open(f, encoding='utf-8').read()
    d = fm(t)
    qid = norm(d.get('question_id', ''))
    if not qid:
        continue
    it = get(qid)
    it['title'] = d.get('question') or it['title']
    it['diff'] = d.get('difficulty') or it['diff']
    it['rating'] = d.get('rating') or None
    it['ling'] = os.path.basename(f)
    it['ling_py'] = '```python' in t or '```py\n' in t
    tags = d.get('tags', '')
    it['db'] = any(x in str(tags) for x in ('leetcode/mysql', 'leetcode/pythondata', 'leetcode/postgresql', 'leetcode/bash', 'leetcode/mssql'))

for f in sorted(glob.glob(os.path.join(ROOT, 'yiduobo题解/solutions/*.md'))):
    t = open(f, encoding='utf-8').read()
    d = fm(t)
    q = d.get('question_id', '')
    ids = q if isinstance(q, list) else [q]
    name = os.path.basename(f)[:-len(' · yiduobo.md')]
    parts = name.split(' & ')
    for i, qid in enumerate(ids):
        qid = norm(qid)
        if not qid:
            continue
        it = get(qid)
        if it['yiduobo'] is None:  # prefer the dedicated article if several
            it['yiduobo'] = os.path.basename(f)
        elif len(ids) == 1:
            it['yiduobo'] = os.path.basename(f)
        if not it['title']:
            p = parts[i] if i < len(parts) else parts[-1]
            it['title'] = p.split(' ', 1)[1] if ' ' in p else (d.get('question') or p)
        it['yid_code'] = it['yid_code'] or '```' in t
        if not it['diff']:
            m = re.search(r'· (Easy|Medium|Hard) ·', t[:3000])
            it['diff'] = m.group(1) if m else None

# existing videos
AUTH = {'灵茶山艾府': 'ling', 'yiduobo': 'yiduobo'}
for line in open(os.path.join(ROOT, 'videos.txt'), encoding='utf-8'):
    line = line.strip()
    m = re.match(r'.*/(\d{4}) .* · (灵茶山艾府|yiduobo)\.mp4$', line)
    if m:
        qid = str(int(m.group(1)))
        if qid in P:
            P[qid]['done'].append(AUTH[m.group(2)])
            P[qid].setdefault('existing', {})[AUTH[m.group(2)]] = line

# study-path order
RX = re.compile(r'\[((?:LCR|LCP|LCS|面试题)?\s?[\d.]+)\. ([^\]]+)\]\(https://leetcode\.cn/problems/([^/)]+)/?\)')
order = []
seen = set()
PATHS = [('labuladong', 'labuladong速成路线图/00-速成路线图-练法与30天题单.md'),
         ('灵神核心路线', '灵神科学刷题/01-核心路线-新手村清单.md'),
         ('灵神突击', '灵神科学刷题/02-突击-Hot100与面试150.md')]
PATHS += [('灵神题单·' + os.path.basename(f)[3:-3], os.path.relpath(f, ROOT))
          for f in sorted(glob.glob(os.path.join(ROOT, '灵神科学刷题/题单/*.md')))]
slugs = {}
for tag, rel in PATHS:
    for m in RX.finditer(open(os.path.join(ROOT, rel), encoding='utf-8').read()):
        qid = norm(m.group(1))
        slugs.setdefault(qid, m.group(3))
        if qid in P:
            if tag not in P[qid]['paths']:
                P[qid]['paths'].append(tag)
            if qid not in seen:
                seen.add(qid)
                order.append(qid)
rest = sorted((q for q in P if q not in seen), key=sortkey)
order += rest
for q, s in slugs.items():
    if q in P:
        P[q]['slug'] = s

items = []
for rank, q in enumerate(order):
    it = P[q]
    it['rank'] = rank
    todo = []
    if it['ling'] and it['ling_py'] and not it['db'] and 'ling' not in it['done']:
        todo.append('ling')
    if it['yiduobo'] and it['yid_code'] and not it['db'] and 'yiduobo' not in it['done']:
        todo.append('yiduobo')
    it['todo'] = todo
    items.append(it)
json.dump(items, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
n_l = sum('ling' in i['todo'] for i in items)
n_y = sum('yiduobo' in i['todo'] for i in items)
print(f'problems {len(items)}; todo ling {n_l}, yiduobo {n_y}; in study paths {len(seen & set(P))}; '
      f'done ling {sum("ling" in i["done"] for i in items)} yiduobo {sum("yiduobo" in i["done"] for i in items)}; '
      f'db {sum(i["db"] for i in items)}; ling no-py {sum(bool(i["ling"]) and not i["ling_py"] for i in items)}; '
      f'no title {sum(not i["title"] for i in items)}')
sp = [i for i in items if i['paths'] and i['todo']]
print('study-path problems with todo:', len(sp), 'videos', sum(len(i['todo']) for i in sp))
