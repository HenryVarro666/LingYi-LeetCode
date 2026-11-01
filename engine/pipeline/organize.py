"""Build / refresh the LC_Video repo layout from the Obsidian vault + rendered videos.

python organize.py VAULT ROOT [--budget 150] [--steps assets,solutions,videos,paths,index]

VAULT = the Leetcode vault (灵茶山艾府题解/, yiduobo题解/, hot100动画/, 题单动画/, 灵神科学刷题/, labuladong速成路线图/)
ROOT  = LC_Video (this repo).  Idempotent: files are only (re)written when their content changes; videos/assets
are copied only when missing.  Stops starting new work after --budget seconds (re-run to continue).
"""
import glob
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
import repo  # noqa: E402

AUTH = repo.AUTHORS  # ling -> 灵茶山艾府
SRC = {'ling': '灵茶山艾府题解', 'yiduobo': 'yiduobo题解'}
T0 = time.time()
BUDGET = 150.0
STATS = {'written': 0, 'copied': 0}


def over():
    return time.time() - T0 > BUDGET


def enc(p):
    return p.replace('%', '%25').replace(' ', '%20').replace('(', '%28').replace(')', '%29').replace('#', '%23') \
        .replace('?', '%3F').replace('<', '%3C').replace('>', '%3E')


SITE = {}
try:
    SITE = json.load(open(os.path.join(HERE, 'site.json'), encoding='utf-8'))
except (OSError, ValueError):
    pass
GITHUB = {}
try:
    GITHUB = json.load(open(os.path.join(HERE, 'github.json'), encoding='utf-8'))
except (OSError, ValueError):
    pass
ROOT_DIR = [None]


def player_url(target):
    """online player URL for a video (GitHub's web UI cannot play mp4 files)"""
    from urllib.parse import quote
    rel = os.path.relpath(target, ROOT_DIR[0]).replace(os.sep, '/')
    return f"https://{SITE['owner'].lower()}.github.io/{SITE['repo']}/?v={quote(rel, safe='/')}"


def vlink(frm_dir, target, text):
    """link to a video: the GIF next to the mp4 when it exists (GitHub shows GIFs but cannot play mp4)"""
    gif = target[:-4] + '.gif' if target.endswith('.mp4') else target
    return link(frm_dir, gif if os.path.exists(gif) else target, text)


def link(frm_dir, target, text):
    return f'[{text}]({enc(os.path.relpath(target, frm_dir))})'


def write(path, text):
    try:
        if open(path, encoding='utf-8').read() == text:
            return
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(text)
    STATS['written'] += 1


def copy(src, dst):
    if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst + '.part')
    os.replace(dst + '.part', dst)
    STATS['copied'] += 1


def fm(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    d = {}
    if m:
        for line in m.group(1).split('\n'):
            k, _, v = line.partition(':')
            d[k.strip()] = v.strip().strip('"')
    return d


ID_RX = re.compile(r'^(\d{4}|LCR \d+|LCP \d+|LCS \d+|面试题 [\d.]+|meituan-\d+) ')


def id_of(name):
    m = ID_RX.match(name)
    if not m:
        return None
    s = m.group(1)
    return str(int(s)) if s.isdigit() else s


class Ctx:
    def __init__(self, vault, root):
        self.vault, self.root = vault, root
        ROOT_DIR[0] = root
        self.items = repo.items()
        self.by_id = {it['id']: it for it in self.items}
        self.docs = path_docs(vault)
        for src, dst in self.docs:
            PATH_DOCS[src] = dst
        self.extras = extra_files(vault)
        for full, rel, is_md in self.extras:
            if is_md:
                PATH_DOCS[os.path.relpath(full, vault)[:-3]] = rel
        names = {}
        for k, rel in PATH_DOCS.items():
            names.setdefault(os.path.basename(k), []).append(rel)
        for n, rels in names.items():
            if len(rels) == 1 and n != 'README':
                BASENAME_DOCS[n] = rels[0]
        PATH_DOCS['hot100动画/00 Hot100 动画索引'] = '刷题路径/题单/LeetCode 热题 100.md'
        PATH_DOCS['题单动画/00 题单动画索引'] = '索引.md'
        for it in self.items:
            for a, rel in (it.get('existing') or {}).items():
                VIDEO_MAP[rel] = repo.video(it, a)
        for f in glob.glob(os.path.join(vault, 'hot100动画', '*', '00 * · 概念讲解.mp4')):
            cat = os.path.basename(os.path.dirname(f))
            VIDEO_MAP[os.path.relpath(f, vault)] = f'分类概念视频/{cat} · 概念讲解.mp4'
        build_alias(self)

    def p(self, rel):
        return os.path.join(self.root, rel)

    def has_video(self, it, a):
        return os.path.exists(self.p(repo.video(it, a)))

    def has_sol(self, it, a):
        return bool(it.get(a))


# ------------------------------------------------------------------ markdown rewriting
PATH_DOCS = {}  # vault-relative doc path without .md -> repo-relative .md path
BASENAME_DOCS = {}  # unique doc basename (without .md) -> repo-relative path (Obsidian short links)
VIDEO_MAP = {}  # vault-relative video path -> repo-relative video path
ALIAS = {}  # ling "pointer" solutions ("本题和 X 一样，请看我的题解") : problem id -> referenced problem id
KNOWN_PREFIXES = ('灵茶山艾府题解', 'yiduobo题解', 'hot_100', 'hot100动画', '题单动画', '灵神科学刷题', 'labuladong速成路线图',
                  'Python刷题函数', '题目讲解', '00 ', '2026-', 'DP_abstract', 'bio_abstract', 'Notes', 'List', 'output/', 'tools/')

# extra material copied from the vault: (vault path, repo path); directories are copied recursively
EXTRA_MD = [
    ('灵茶山艾府题解/题单', '刷题路径/灵神原版题单'),
    ('Python刷题函数', '学习笔记/Python刷题函数'),
    ('题目讲解', '学习笔记/题目讲解'),
    ('hot_100', '学习笔记/Hot100笔记'),
    ('2026-10-14', '学习笔记/错题记录/2026-10-14'),
    ('DP_abstract.md', '学习笔记/动态规划题单（系统分类版）.md'),
    ('bio_abstract.md', '学习笔记/二分题单（结构化总结）.md'),
    ('Notes.md', '学习笔记/方法论与题单入口.md'),
    ('List.md', '学习笔记/刷题清单.md'),
    ('二分查找_课后题.md', '学习笔记/课后题/二分查找_课后题.md'),
    ('反转链表_课后题.md', '学习笔记/课后题/反转链表_课后题.md'),
]
EXTRA_COPY_EXT = ('.py', '.ipynb', '.json', '.csv', '.png', '.jpg', '.svg')
EXTRA_SKIP = ('__pycache__', '.DS_Store', 'cookies', '.pyc')
PLAIN_PROB_DOCS = ('学习笔记/动态规划题单（系统分类版）.md', '学习笔记/二分题单（结构化总结）.md', '学习笔记/刷题清单.md',
                   '学习笔记/方法论与题单入口.md')


def extra_files(v):
    """-> [(src_abs, repo_rel, is_md)] for the extra material"""
    out = []
    for src, dst in EXTRA_MD:
        p = os.path.join(v, src)
        if os.path.isfile(p):
            out.append((p, dst, p.endswith('.md')))
        elif os.path.isdir(p):
            for dp, dn, fn in os.walk(p):
                dn[:] = [d for d in dn if not any(x in d for x in EXTRA_SKIP)]
                for f in sorted(fn):
                    if any(x in f for x in EXTRA_SKIP):
                        continue
                    full = os.path.join(dp, f)
                    rel = os.path.join(dst, os.path.relpath(full, p))
                    if f.endswith('.md'):
                        out.append((full, rel, True))
                    elif f.endswith(EXTRA_COPY_EXT):
                        out.append((full, rel, False))
    for f in sorted(glob.glob(os.path.join(v, 'bytedance', '*.csv'))):
        out.append((f, '刷题路径/题单/数据/' + os.path.basename(f), False))
    for f in sorted(glob.glob(os.path.join(v, '*.py'))):
        out.append((f, '我的代码/' + os.path.basename(f), False))
    return out


def build_alias(ctx):
    for it in ctx.items:
        if not it.get('ling') or it.get('ling_py'):
            continue
        try:
            t = open(os.path.join(ctx.vault, SRC['ling'], 'solutions', it['ling']), encoding='utf-8').read()
        except OSError:
            continue
        sol = re.split(r'\n> ## 分类题单', t.split('[!success]', 1)[-1])[0]
        if len(sol) > 900 or not re.search(r'(请看|详见|见\s*\[|同\s*\[|一样|做法|题解)', sol):
            continue
        m = re.search(r'\[((?:LCR |LCP |面试题 )?\d+(?:\.\d+)?)\. [^\]]+\]\(https://leetcode\.cn/problems/', sol)
        w = re.search(r'\[\[灵茶山艾府题解/solutions/([^|\]]+)', sol)
        ref = None
        if m:
            ref = m.group(1)
            ref = str(int(ref)) if ref.isdigit() else ref
        elif w:
            ref = id_of(w.group(1))
        if ref:
            if ref != it['id'] and ref in ctx.by_id:
                ALIAS[it['id']] = ref


def ling_alias_video(ctx, it):
    """(repo video path, referenced id) when this problem's ling solution just points to another problem's video"""
    ref = ALIAS.get(it['id'])
    if ref and not ctx.has_video(it, 'ling'):
        r = ctx.by_id[ref]
        if ctx.has_video(r, 'ling'):
            return ctx.p(repo.video(r, 'ling')), ref
    return None


def rewrite_wikilinks(text, ctx, frm_dir, author_hint=None):
    def sub(m):
        target, _, alias = m.group(1).partition('|')
        t = target.split('#')[0].strip()
        alias = alias or os.path.basename(t)
        for a, src in SRC.items():
            if t.startswith(src + '/solutions/'):
                qid = id_of(t[len(src) + len('/solutions/'):])
                it = ctx.by_id.get(qid)
                if it and it.get(a):
                    return link(frm_dir, ctx.p(repo.solution(it, a)), alias)
                return alias
        if t.endswith('.mp4'):
            v = VIDEO_MAP.get(t)
            return vlink(frm_dir, ctx.p(v), alias) if v else alias
        tt = t[:-3] if t.endswith('.md') else t
        if tt in PATH_DOCS:
            return link(frm_dir, ctx.p(PATH_DOCS[tt]), alias)
        if os.path.basename(tt) in BASENAME_DOCS:
            return link(frm_dir, ctx.p(BASENAME_DOCS[os.path.basename(tt)]), alias)
        if re.fullmatch(r'\d+\.py', t) and os.path.exists(os.path.join(ctx.vault, t)):
            return link(frm_dir, ctx.p('我的代码/' + t), alias)
        if t.startswith(KNOWN_PREFIXES):
            return alias
        return m.group(0)  # not a vault link (e.g. an array literal like [[1,2]])
    return re.sub(r'(?<!!)\[\[([^\[\]\n]+?)\]\]', sub, text)


def callouts(text):
    # Obsidian callouts -> plain blockquote with a bold title (renders on GitHub too)
    return re.sub(r'^> \[!(\w+)\][+-]? ?(.*)$', lambda m: f'> **{m.group(2) or m.group(1)}**', text, flags=re.M)


# ------------------------------------------------------------------ steps
def step_assets(ctx):
    for a, src in SRC.items():
        s = os.path.join(ctx.vault, src, 'assets')
        d = ctx.p(f'题解/_assets/{AUTH[a]}')
        for f in sorted(os.listdir(s)):
            if over():
                return
            if f.startswith('_'):
                continue
            if not os.path.exists(os.path.join(d, f)):
                copy(os.path.join(s, f), os.path.join(d, f))


def solution_md(ctx, it, a):
    src = os.path.join(ctx.vault, SRC[a], 'solutions', it[a])
    t = open(src, encoding='utf-8').read()
    out = ctx.p(repo.solution(it, a))
    d = os.path.dirname(out)
    t = t.replace('](../assets/', '](' + enc(os.path.relpath(ctx.p(f'题解/_assets/{AUTH[a]}'), d)) + '/')
    t = rewrite_wikilinks(t, ctx, d)
    if a == 'ling':
        t = t.replace('](/u/', '](https://leetcode.cn/u/').replace('](/problems/', '](https://leetcode.cn/problems/')
    t = callouts(t)
    return out, t, fm(t)


def problem_readme(ctx, it, meta):
    d = ctx.p(repo.folder(it))
    name = os.path.basename(repo.folder(it))
    slug = meta.get('question_slug') or ''
    if not slug:
        m = re.search(r'leetcode\.cn/problems/([^/)\s]+)', meta.get('problem_url', ''))
        slug = m.group(1) if m else it.get('slug', '')
    head = [f"# {it['id']}. {it['title']}", '']
    bits = [b for b in [it.get('diff'), f"难度分 {it['rating']}" if it.get('rating') else None,
                        f'[力扣原题](https://leetcode.cn/problems/{slug}/)' if slug else None] if b]
    head.append(' · '.join(bits))
    if it.get('paths'):
        head += ['', '所在刷题路径：' + '、'.join(it['paths'])]
    head += ['', '| 作者 | 题解 | 动画讲解 |', '|---|---|---|']
    for a in ('ling', 'yiduobo'):
        sol = link(d, ctx.p(repo.solution(it, a)), '📄 题解') if it.get(a) else '—'
        vid = (vlink(d, ctx.p(repo.video(it, a)), '▶︎ 动画（GIF）') + ' · ' + link(d, ctx.p(repo.video(it, a)), 'mp4 文件')
               if ctx.has_video(it, a) else '—')
        if vid == '—' and a == 'ling' and ling_alias_video(ctx, it):
            v, ref = ling_alias_video(ctx, it)
            vid = f'灵神这篇题解指向 {ref} 题的题解，请看那道题的视频：' + vlink(d, v, f'▶︎ {os.path.basename(v)[:-4]}')
        head.append(f'| {AUTH[a]} | {sol} | {vid} |')
    gifs = []
    for a in ('ling', 'yiduobo'):
        v = ctx.p(repo.video(it, a))
        if ctx.has_video(it, a) and os.path.exists(v[:-4] + '.gif'):
            gifs += [f'### {AUTH[a]}', '', f'![{name} · {AUTH[a]}]({enc(os.path.basename(v)[:-4] + ".gif")})', '']
    if gifs:
        head += ['', '## 动画讲解', '', '> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。', ''] + gifs
    stmt = meta.get('_stmt')
    if stmt:
        head += ['', '## 题目描述', '', stmt]
    head += ['', '---', link(d, ctx.p(f'题解/{repo.bucket(it)}/README.md'), f'↑ 返回 {repo.bucket(it)}') + ' · '
             + link(d, ctx.p('索引.md'), '总索引') + ' · ' + link(d, ctx.p('README.md'), '仓库首页'), '']
    return '\n'.join(head)


def step_solutions(ctx):
    for it in ctx.items:
        if over():
            return
        meta = {}
        for a in ('ling', 'yiduobo'):
            if it.get(a):
                out, t, m = solution_md(ctx, it, a)
                write(out, t)
                if a == 'ling':
                    meta.update(m)
                    sm = re.search(r'> \*\*题目描述\*\*\n((?:>.*\n?)+)', t)
                    if sm:
                        meta['_stmt'] = re.sub(r'^> ?', '', sm.group(1), flags=re.M).strip()
                else:
                    for k, v in m.items():
                        meta.setdefault(k, v)
        write(os.path.join(ctx.p(repo.folder(it)), 'README.md'), problem_readme(ctx, it, meta))


def step_videos(ctx):
    for it in ctx.items:
        for a, rel in (it.get('existing') or {}).items():
            if over():
                return
            copy(os.path.join(ctx.vault, rel), ctx.p(repo.video(it, a)))
    for f in sorted(glob.glob(os.path.join(ctx.vault, 'hot100动画', '*', '00 * · 概念讲解.mp4'))):
        cat = os.path.basename(os.path.dirname(f))
        copy(f, ctx.p(f'分类概念视频/{cat} · 概念讲解.mp4'))


def problem_links(ctx, it, frm_dir):
    parts = [link(frm_dir, ctx.p(repo.folder(it)), '📂')]
    for a in ('ling', 'yiduobo'):
        bits = []
        if it.get(a):
            bits.append(link(frm_dir, ctx.p(repo.solution(it, a)), '灵神' if a == 'ling' else 'yiduobo'))
        if ctx.has_video(it, a):
            bits.append(vlink(frm_dir, ctx.p(repo.video(it, a)), '▶︎'))
        elif a == 'ling' and ling_alias_video(ctx, it):
            v, ref = ling_alias_video(ctx, it)
            bits.append(vlink(frm_dir, v, f'▶︎（见 {ref}）'))
        if bits:
            parts.append(' '.join(bits))
    return ' · '.join(parts)


PROB_RX = re.compile(r'\[((?:LCR|LCP|LCS|面试题)?\s?[\d.]+)\. ([^\]]+)\]\((https://leetcode\.cn/problems/[^)]+)\)')
WIKI_PROB = re.compile(r'\[\[(?:灵茶山艾府题解|yiduobo题解)/solutions/[^|\]]*\|((?:LCR|LCP|LCS|面试题)?\s?[\d.]+)\. ([^\]]+)\]\]')
PLAIN_PROB = re.compile(r'^(\s*[-*] (?:\[[ xX]\] )?)((?:LCR |LCP |面试题 )?\d+(?:\.\d+)?)\. ?(\S[^（(\s]*)')


def rewrite_path_doc(ctx, text, out_rel):
    frm_dir = os.path.dirname(ctx.p(out_rel))
    lines = []
    plain = out_rel in PLAIN_PROB_DOCS
    for line in text.split('\n'):
        m = PROB_RX.search(line)
        w = None if m else WIKI_PROB.search(line)
        if w and line.lstrip().startswith(('- ', '* ')):
            qid = w.group(1).strip()
            qid = str(int(qid)) if qid.isdigit() else qid
            it = ctx.by_id.get(qid)
            new = line[:w.start()] + f'{w.group(1).strip()}. {w.group(2)}' + rewrite_wikilinks(line[w.end():], ctx, frm_dir)
            if it:
                new = new.rstrip() + ' — ' + problem_links(ctx, it, frm_dir)
            lines.append(new)
            continue
        p = None if (m or w or not plain) else PLAIN_PROB.match(line)
        if p:
            qid = p.group(2)
            qid = str(int(qid)) if qid.isdigit() else qid
            it = ctx.by_id.get(qid)
            new = rewrite_wikilinks(line, ctx, frm_dir)
            if it and it['title'].replace(' ', '')[:2] == p.group(3).replace(' ', '')[:2]:
                new = new.rstrip() + ' — ' + problem_links(ctx, it, frm_dir)
            lines.append(new)
            continue
        if m and line.lstrip().startswith(('- ', '|', '* ')):
            qid = m.group(1).strip()
            qid = str(int(qid)) if qid.isdigit() else qid
            it = ctx.by_id.get(qid)
            head, rest = line[:m.end()], line[m.end():]
            hot = '🔥' in rest
            if line.lstrip().startswith('|'):
                lines.append(rewrite_wikilinks(line, ctx, frm_dir))
                continue
            rest = re.sub(r'\[\[[^\]]*\]\]', '', rest)
            rest = re.sub(r'(📂|🎬|🔥)', '', rest)
            rest = re.sub(r'(\s*[·—]\s*)+$', '', rest)
            rest = re.sub(r'\s*·\s*(·\s*)+', ' · ', rest).rstrip()
            new = head + (' 🔥' if hot else '') + rest
            if it:
                new += ' — ' + problem_links(ctx, it, frm_dir)
            lines.append(new)
        else:
            lines.append(rewrite_wikilinks(line, ctx, frm_dir))
    return '\n'.join(lines)


def list_doc(ctx, title, rows, out_rel, intro=''):
    d = os.path.dirname(ctx.p(out_rel))
    have = 0
    body = ['| 题号 | 题目 | 难度 | 灵茶山艾府 | yiduobo |', '|---|---|---|---|---|']
    for num, name in rows:
        it = ctx.by_id.get(str(num))
        cells = []
        for a in ('ling', 'yiduobo'):
            if not it:
                cells.append('—')
                continue
            bits = []
            if it.get(a):
                bits.append(link(d, ctx.p(repo.solution(it, a)), '📄'))
            if ctx.has_video(it, a):
                bits.append(vlink(d, ctx.p(repo.video(it, a)), '▶︎'))
            elif a == 'ling' and ling_alias_video(ctx, it):
                bits.append(vlink(d, ling_alias_video(ctx, it)[0], f'▶︎见{ling_alias_video(ctx, it)[1]}'))
            cells.append(' '.join(bits) or '—')
        if it and (ctx.has_video(it, 'ling') or ctx.has_video(it, 'yiduobo')):
            have += 1
        t = link(d, ctx.p(repo.folder(it)), name) if it else name
        body.append(f"| {num} | {t} | {(it or {}).get('diff') or ''} | {cells[0]} | {cells[1]} |")
    return '\n'.join([f'# {title}', '', intro, f'共 {len(rows)} 题，{have} 题已有动画讲解。', ''] + body + [''])


def path_docs(v):
    docs = []  # (vault rel without .md, repo rel)
    for f in sorted(glob.glob(os.path.join(v, 'labuladong速成路线图', '*.md'))):
        docs.append((os.path.relpath(f, v)[:-3], '刷题路径/labuladong速成路线图/' + os.path.basename(f)))
    for f in sorted(glob.glob(os.path.join(v, '灵神科学刷题', '*.md'))) + sorted(glob.glob(os.path.join(v, '灵神科学刷题', '题单', '*.md'))):
        rel = os.path.relpath(f, v)
        docs.append((rel[:-3], '刷题路径/' + rel))
    return docs


def step_paths(ctx):
    v = ctx.vault
    for src, dst in ctx.docs:
        t = open(os.path.join(v, src + '.md'), encoding='utf-8').read()
        write(ctx.p(dst), rewrite_path_doc(ctx, t, dst))
    # problem lists
    hot = json.load(open(os.path.join(ENGINE, 'hot100.json'), encoding='utf-8'))
    cats = []
    for x in hot:
        if x['cat'] not in cats:
            cats.append(x['cat'])
    out_rel = '刷题路径/题单/LeetCode 热题 100.md'
    d = os.path.dirname(ctx.p(out_rel))
    parts = ['# LeetCode 热题 100', '', '按官方分类排列；每个分类先看「概念讲解」视频，再按顺序做题。', '']
    for i, c in enumerate(cats):
        cv = ctx.p(f'分类概念视频/{i + 1:02d} {c} · 概念讲解.mp4')
        parts += [f'## {i + 1:02d} {c}', '']
        if os.path.exists(cv):
            parts += ['📘 ' + vlink(d, cv, f'{c} · 概念讲解视频'), '']
        sub = list_doc(ctx, '', [(x['num'], x['title']) for x in hot if x['cat'] == c], out_rel).split('\n')
        parts += sub[sub.index('| 题号 | 题目 | 难度 | 灵茶山艾府 | yiduobo |'):]
    write(ctx.p(out_rel), '\n'.join(parts))
    sets = json.load(open(os.path.join(ENGINE, 'sets_full.json'), encoding='utf-8'))
    for name, rows in sets.items():
        fn = name.replace('/', '／').replace('·', '-').replace('  ', ' ').strip()
        write(ctx.p(f'刷题路径/题单/{fn}.md'), list_doc(ctx, name, [(r[0], r[1]) for r in rows], f'刷题路径/题单/{fn}.md'))


def rewrite_rel_links(ctx, text, src_full, out_rel):
    """markdown links in a copied vault note that point at other vault files -> the matching repo file"""
    from urllib.parse import unquote
    full2repo = getattr(ctx, '_full2repo', None)
    if full2repo is None:
        full2repo = {os.path.normpath(f): r for f, r, _ in ctx.extras}
        for k, r in PATH_DOCS.items():
            full2repo.setdefault(os.path.normpath(os.path.join(ctx.vault, k + '.md')), r)
        ctx._full2repo = full2repo
    frm_dir = os.path.dirname(ctx.p(out_rel))

    def sub(m):
        label, t = m.group(1), m.group(2)
        if re.match(r'^[a-z]+:', t) or t.startswith('#'):
            return m.group(0)
        tgt = unquote(t.split('#')[0])
        if tgt.startswith('<') and tgt.endswith('>'):
            tgt = tgt[1:-1]
        if os.path.exists(os.path.normpath(os.path.join(frm_dir, tgt))):
            return m.group(0)  # already fine inside the repo
        v = os.path.normpath(os.path.join(os.path.dirname(src_full), tgt))
        r = full2repo.get(v) or full2repo.get(v + '.md')
        if r is None and v.endswith('.py') and os.path.dirname(v) == os.path.normpath(ctx.vault):
            r = '我的代码/' + os.path.basename(v)
        return link(frm_dir, ctx.p(r), label) if r and os.path.exists(ctx.p(r)) else m.group(0)
    return re.sub(r'(?<!!)\[([^\]\n]*)\]\(([^)\s]+)\)', sub, text)


def step_extras(ctx):
    """灵神原版题单、学习笔记、我的代码、字节高频数据 (see EXTRA_MD / extra_files)"""
    for full, rel, is_md in ctx.extras:
        if over():
            return
        if is_md:
            t = open(full, encoding='utf-8').read()
            write(ctx.p(rel), callouts(rewrite_rel_links(ctx, rewrite_path_doc(ctx, t, rel), full, rel)))
        else:
            copy(full, ctx.p(rel))


def step_index(ctx):
    buckets = {}
    for it in ctx.items:
        buckets.setdefault(repo.bucket(it), []).append(it)

    def bkey(b):
        return (0, int(b[:4])) if b[:4].isdigit() else (1, b)
    top = ['# 题号总索引', '', '每个题号区间一个文件夹；点进去是该区间所有题目的列表，每题一个文件夹（题解 + 视频）。', '',
           '| 区间 | 题目数 | 灵神题解 | yiduobo 题解 | 灵神视频 | yiduobo 视频 |', '|---|---|---|---|---|---|']
    tot = [0] * 5
    for b in sorted(buckets, key=bkey):
        its = sorted(buckets[b], key=lambda x: (int(x['id']) if x['id'].isdigit() else 0, x['id']))
        d = ctx.p(f'题解/{b}')
        rows = ['| 题号 | 题目 | 难度 | 灵茶山艾府 | yiduobo |', '|---|---|---|---|---|']
        c = [len(its), 0, 0, 0, 0]
        for it in its:
            cells = []
            for k, a in enumerate(('ling', 'yiduobo')):
                bits = []
                if it.get(a):
                    bits.append(link(d, ctx.p(repo.solution(it, a)), '📄'))
                    c[1 + k] += 1
                if ctx.has_video(it, a):
                    bits.append(vlink(d, ctx.p(repo.video(it, a)), '▶︎'))
                    c[3 + k] += 1
                elif a == 'ling' and ling_alias_video(ctx, it):
                    bits.append(vlink(d, ling_alias_video(ctx, it)[0], f'▶︎见{ling_alias_video(ctx, it)[1]}'))
                cells.append(' '.join(bits) or '—')
            rows.append(f"| {it['id']} | {link(d, ctx.p(repo.folder(it)), it['title'])} | {it.get('diff') or ''} | {cells[0]} | {cells[1]} |")
        write(os.path.join(d, 'README.md'), '\n'.join([f'# {b}', '', f'共 {c[0]} 题 · 视频 {c[3] + c[4]} 个', '',
                                                       '[↑ 总索引](../../索引.md)', ''] + rows + ['']))
        top.append(f"| {link(ctx.root, d, b)} | {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} |")
        tot = [x + y for x, y in zip(tot, c)]
    top.append(f'| **合计** | {tot[0]} | {tot[1]} | {tot[2]} | {tot[3]} | {tot[4]} |')
    write(ctx.p('索引.md'), '\n'.join(top + ['']))
    sub = [re.sub(r'\]\(题解/', '](', line) for line in top]  # same table, links relative to 题解/
    sub[0] = '# 题解'
    write(ctx.p('题解/README.md'), '\n'.join(sub + ['', '题解里的图片在 `_assets/`。', '',
                                               link(ctx.p('题解'), ctx.p('README.md'), '↑ 仓库首页'), '']))
    json.dump(dict(problems=tot[0], ling_solutions=tot[1], yiduobo_solutions=tot[2], ling_videos=tot[3],
                   yiduobo_videos=tot[4], concept_videos=len(glob.glob(ctx.p('分类概念视频/*.mp4'))),
                   updated=time.strftime('%Y-%m-%d %H:%M')),
              open(ctx.p('engine/stats.json'), 'w'), ensure_ascii=False, indent=1)


def step_folders(ctx):
    """README.md for each top-level folder, so GitHub shows a table of contents when you open it"""
    def md_title(p):
        try:
            m = re.search(r'^# (.+)$', open(p, encoding='utf-8').read(), re.M)
            return m.group(1).strip() if m else os.path.basename(p)[:-3]
        except OSError:
            return os.path.basename(p)[:-3]

    def listing(folder, intro, exts=('.md',), recurse=True):
        d = ctx.p(folder)
        lines = []
        for dp, dn, fn in os.walk(d):
            dn.sort()
            rel = os.path.relpath(dp, d)
            depth = 0 if rel == '.' else rel.count(os.sep) + 1
            if not recurse and depth:
                continue
            if depth and depth <= 2:
                lines.append(('  ' * (depth - 1)) + f'- **{os.path.basename(dp)}/**')
            for f in sorted(fn):
                if f == 'README.md' or not f.endswith(exts) or depth > 2:
                    continue
                p = os.path.join(dp, f)
                t = md_title(p) if f.endswith('.md') else f
                lines.append(('  ' * depth) + '- ' + link(d, p, t))
        return '\n'.join([f'# {os.path.basename(folder)}', '', intro, ''] + lines + ['', link(d, ctx.p('README.md'), '↑ 仓库首页'), ''])

    write(ctx.p('刷题路径/README.md'), listing('刷题路径',
          '按顺序刷题的路线：labuladong 速成路线图、灵神「如何科学刷题」核心路线与 12 个题单、灵神原版题单（按知识点分节），'
          '以及 Hot100 / 面试经典 150 / 热题 173 / 字节高频等常见题单。每道题后面都挂了两位作者的题解和动画视频。'))
    write(ctx.p('学习笔记/README.md'), listing('学习笔记',
          'Python 刷题函数讲解、两位大神写法差异对照、DP / 二分题单总结、Hot100 逐题笔记、逐行讲解和错题记录。',
          exts=('.md', '.ipynb')))
    d = ctx.p('分类概念视频')
    vids = sorted(f for f in os.listdir(d) if f.endswith('.mp4')) if os.path.isdir(d) else []
    write(os.path.join(d, 'README.md'), '\n'.join(['# 分类概念视频', '', 'Hot100 的 17 个分类，每类一个「通用思想 + 模板」讲解视频，建议刷该类题之前先看。', '']
          + [f'- {vlink(d, os.path.join(d, v), v[:-4])}' for v in vids] + ['', link(d, ctx.p('README.md'), '↑ 仓库首页'), '']))
    d = ctx.p('我的代码')
    rows = ['| 文件 | 题目 |', '|---|---|']
    for f in sorted(os.listdir(d) if os.path.isdir(d) else [], key=lambda x: (len(x), x)):
        if not f.endswith('.py'):
            continue
        it = ctx.by_id.get(f[:-3])
        rows.append(f"| {link(d, os.path.join(d, f), f)} | {link(d, ctx.p(repo.folder(it)), it['id'] + '. ' + it['title']) if it else ''} |")
    write(os.path.join(d, 'README.md'), '\n'.join(['# 我的代码', '', '自己刷题时写的解法，文件名就是题号；右边链到该题的题解和动画视频。', ''] + rows
          + ['', link(d, ctx.p('README.md'), '↑ 仓库首页'), '']))
    write(ctx.p('engine/configs/README.md'), '''# 视频配置

每个视频对应一个配置文件（`<4 位题号>.py`，定义 `CONFIG` 字典），格式见 [../README.md](../README.md)。

| 目录 | 内容 |
|---|---|
| `ling/`、`yiduobo/` | Hot100 两位作者的视频 |
| `concept/` | Hot100 17 个分类的概念讲解 |
| `ling2/`、`yiduobo2/` | 面试经典 150 / 热题 173 / 字节高频 / List.md 里的其余题 |
| `ling_all/`、`yiduobo_all/` | 其余全部题解（灵神原文只有 Go 的，按原逻辑逐行转写为 Python，配置里有注明） |
| `skipped/` | 做不了的题和原因（`.resolved` 表示后来已经做出来了） |
| `failed/` | 曾经没通过检查的配置和错误信息（有 `.fixed` 标记的已修复） |
''')


def step_readme(ctx):
    st = json.load(open(ctx.p('engine/stats.json'), encoding='utf-8'))
    vids = st['ling_videos'] + st['yiduobo_videos'] + st['concept_videos']
    size = 0
    for dp, dn, fn in os.walk(ctx.p('题解')):
        size += sum(os.path.getsize(os.path.join(dp, f)) for f in fn if f.endswith('.mp4'))
    for f in glob.glob(ctx.p('分类概念视频/*.mp4')):
        size += os.path.getsize(f)
    paths = []
    for src, dst in ctx.docs:
        if os.path.basename(dst).startswith('README'):
            continue
        t = open(ctx.p(dst), encoding='utf-8').read()
        m = re.search(r'^# (.+)$', t, re.M)
        paths.append(f"- [{m.group(1) if m else os.path.basename(dst)[:-3]}]({enc(dst)})")
    lists = sorted(glob.glob(ctx.p('刷题路径/题单/*.md')))
    ling_list = sorted(glob.glob(ctx.p('刷题路径/灵神原版题单/*.md')))
    notes = [('学习笔记/Python刷题函数/Python 刷题函数从零讲解.md', 'Python 刷题函数从零讲解（两位大神代码里用到的函数）'),
             ('学习笔记/Python刷题函数/两位大神差异对照.md', '两位大神差异对照（同一需求两人怎么写 + Hot100 逐题对照）'),
             ('学习笔记/Python刷题函数/两位大神变量命名对照.md', '两位大神变量命名对照'),
             ('学习笔记/动态规划题单（系统分类版）.md', '动态规划题单（系统分类版）'),
             ('学习笔记/二分题单（结构化总结）.md', '二分题单（结构化总结）'),
             ('学习笔记/方法论与题单入口.md', '方法论与题单入口'),
             ('学习笔记/题目讲解/00 题目讲解 MOC.md', '逐行逐变量的小白讲解'),
             ('学习笔记/Hot100笔记', 'Hot100 逐题笔记'),
             ('学习笔记/课后题', '专题课后题（二分查找 / 反转链表）')]
    notes = [f'- [{t}]({enc(p)})' for p, t in notes if os.path.exists(ctx.p(p))]
    T = f'''# LingYi-LeetCode · 灵一刷题

**灵**茶山艾府 + **yi**duobo：两位大神的 LeetCode 题解，每道题配一段**逐行执行代码**的动画讲解视频，再按刷题路径串起来。

> 视频不是录屏：把大神的原版代码**真正跑一遍**（`sys.settrace` 逐行追踪），从真实变量画出数组、指针、哈希表、栈、链表、树、网格和 DP 表，字幕讲清每一步「为什么」，动画和代码一定对得上。每个视频 1–3 分钟：题意 → 大神原文思路 → 逐行动画 → 复杂度与易错点。

## 收录（{st['updated']} 更新）

| | 题目 | 灵茶山艾府 | yiduobo | 合计 |
|---|---|---|---|---|
| 题解 | {st['problems']} | {st['ling_solutions']} | {st['yiduobo_solutions']} | {st['ling_solutions'] + st['yiduobo_solutions']} |
| 动画视频 | — | {st['ling_videos']} | {st['yiduobo_videos']} | {vids}（含 {st['concept_videos']} 个分类概念视频），约 {size / 2**30:.1f} GB |

全部题号见 [索引.md](索引.md)。

🎬 每个视频都有 GIF 动图版：在 GitHub 上点开任意题目文件夹，README 里直接播放；也可以下载同名 mp4（能暂停、拖进度条）。

## 下载

- **题解文字版**（全部题解 Markdown + 刷题路径 + 学习笔记，不含图片和视频）：[下载/LingYi-LeetCode-题解文字版.zip]({enc('下载/LingYi-LeetCode-题解文字版.zip')})
- **题解 + mp4 视频**（按题号分卷，每卷约 1.5 GB，解压后目录结构与仓库一致）：{('[Releases 页面](https://github.com/' + GITHUB['owner'] + '/' + GITHUB['repo'] + '/releases/latest)') if GITHUB.get('owner') else '见本仓库的 Releases 页面'}
- 也可以 `git clone` 整个仓库（约 30 GB，含 GIF 和 mp4）。

## 怎么用

1. 选一条刷题路径（下面），按顺序做题。
2. 每道题后面：📂 = 题目文件夹，`灵神` / `yiduobo` = 题解原文，▶︎ = 动画（GIF，GitHub 上直接能看）。
3. 题目文件夹的 `README.md`：两份题解链接、两段动画讲解（GIF）、题面；同名 mp4 可下载。

## 刷题路径

{chr(10).join(paths)}

**灵神原版题单**（按知识点分节，每题挂题解和视频）

{chr(10).join(f"- [{os.path.basename(f)[:-3]}]({enc(os.path.relpath(f, ctx.root))})" for f in ling_list)}

**常见题单**（表格：题号 / 题目 / 两位作者的题解与视频）

{chr(10).join(f"- [{os.path.basename(f)[:-3]}]({enc(os.path.relpath(f, ctx.root))})" for f in lists)}

**分类概念视频**：Hot100 的 17 个分类，每类一个通用思想 + 模板讲解，见 [分类概念视频/](分类概念视频/)。

## 学习笔记

{chr(10).join(notes)}

另有 [我的代码/](我的代码/)：刷题时自己写的解法。

## 目录结构

```
LingYi-LeetCode/
├── 题解/<题号区间>/<NNNN 题名>/     每题一个文件夹：README（链接 + 动画 + 题面）、灵茶山艾府.md、yiduobo.md、动画 .gif 和 .mp4
├── 题解/_assets/                     题解里的图片
├── 分类概念视频/                     17 个分类的概念讲解
├── 刷题路径/                         labuladong 速成路线图、灵神「如何科学刷题」+ 12 个题单、灵神原版题单、Hot100 / 面试 150 / 热题 173 / 字节高频
├── 学习笔记/                         Python 刷题函数、两位大神差异对照、DP / 二分题单总结、Hot100 笔记、逐行讲解
├── 我的代码/
├── 索引.md                           全部题号
├── 下载/                             题解文字版压缩包
└── engine/                           视频生成器（Python）+ 每个视频的配置文件 engine/configs/
```

## 视频是怎么做的

见 [engine/README.md](engine/README.md)（配置格式、视图类型、字幕模板）和 [engine/pipeline/README.md](engine/pipeline/README.md)（批量生成流水线）。依赖：Python ≥ 3.10（推荐 3.12）、`pillow`、`pygments`、`ffmpeg`、Noto Sans CJK 字体，可选 `av`（PyAV，快 3–5 倍）。

```bash
cd engine
python make.py configs/ling/0011.py --steps     # 看每一步的字幕
python make.py configs/ling/0011.py out.mp4     # 渲染一个视频
```

## 版权与致谢

- 题解原文版权归原作者：[灵茶山艾府](https://leetcode.cn/u/endlesscheng/)（力扣题解，[B 站 @灵茶山艾府](https://space.bilibili.com/206214)）、[yiduobo](https://www.zhihu.com/people/yiduobo)（知乎「每日 leetcode」专栏）。每篇题解开头都保留了原文链接。题面来自 [力扣](https://leetcode.cn/)。刷题路径整理自 [labuladong](https://labuladong.online/) 和灵茶山艾府的题单。
- 本仓库为学习交流整理，非商业用途。如有侵权请提 issue，会第一时间处理。
- 动画视频与 `engine/` 代码为本仓库原创；`engine/` 代码以 [MIT 许可](engine/LICENSE) 开源。
'''
    write(ctx.p('README.md'), T)
    write(ctx.p('.gitignore'), '_work/\n_site/\n**/__pycache__/\n*.pyc\n*.part.mp4\n*.part.gif\nengine/out/\nengine/preview/\n.DS_Store\n.obsidian/\n')
    write(ctx.p('.gitattributes'), '*.mp4 binary\n*.gif binary\n*.png binary\n*.jpg binary\n')


STEPS = {'extras': step_extras, 'assets': step_assets, 'solutions': step_solutions, 'videos': step_videos, 'paths': step_paths, 'index': step_index,
         'readme': step_readme, 'folders': step_folders}

if __name__ == '__main__':
    vault, root = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    if '--budget' in args:
        BUDGET = float(args[args.index('--budget') + 1])
    steps = args[args.index('--steps') + 1].split(',') if '--steps' in args else list(STEPS)
    ctx = Ctx(vault, root)
    for s in steps:
        if s in ('paths', 'index', 'readme', 'extras', 'folders') or not over():
            STEPS[s](ctx)
            print(f'{s}: done' if not over() else f'{s}: STOPPED (budget) — re-run', flush=True)
    print(f"written {STATS['written']} files, copied {STATS['copied']} files, {time.time() - T0:.0f}s")
