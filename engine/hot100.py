"""Hot100 bookkeeping: final file names, Mac/remote render loop, Obsidian index.

python hot100.py paths                    # print config -> final video path
python hot100.py render DEST --jobs 3 --budget 160 [--dirs yiduobo,concept]
                                          # render not-yet-existing videos straight into DEST/<NN 分类>/...,
                                          # stops launching new jobs after --budget seconds (for time-limited shells)
python hot100.py index DEST               # write DEST/00 Hot100 动画索引.md
"""
import glob
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = json.load(open(os.path.join(HERE, 'hot100.json'), encoding='utf-8'))
BYNUM = {it['num']: it for it in ITEMS}
CATS = []
for it in ITEMS:
    if it['cat'] not in CATS:
        CATS.append(it['cat'])
AUTHOR = {'ling': '灵茶山艾府', 'yiduobo': 'yiduobo'}


def cat_dir(cat):
    return f'{CATS.index(cat) + 1:02d} {cat}'


def final_path(cfg_path):
    d = os.path.basename(os.path.dirname(cfg_path))
    name = os.path.splitext(os.path.basename(cfg_path))[0]
    if d == 'concept':
        idx, cat = name.split('_', 1)
        return os.path.join(cat_dir(cat), f'00 {cat} · 概念讲解.mp4')
    num = int(name)
    it = BYNUM[num]
    title = it['title'].replace('/', '／')
    return os.path.join(cat_dir(it['cat']), f'{num:04d} {title} · {AUTHOR[d]}.mp4')


def all_configs(dirs=('concept', 'ling', 'yiduobo')):
    out = []
    for d in dirs:
        out += sorted(glob.glob(os.path.join(HERE, 'configs', d, '*.py')))
    return out


def render(dest, jobs=3, budget=160, dirs=('concept', 'ling', 'yiduobo'), only=None, force=False, part=None, newer=None):
    t0 = time.time()
    for p in glob.glob(os.path.join(dest, '*', '*.part.mp4')):
        try:
            os.remove(p)
        except OSError:
            pass  # deletion may be disallowed on the mounted folder; it gets overwritten anyway
    def fresh(c):
        p = os.path.join(dest, final_path(c))
        return os.path.exists(p) and (newer is None or os.path.getmtime(p) > newer)
    todo = [c for c in all_configs(dirs) if force or not fresh(c)]
    if only:
        todo = [c for c in todo if any(o + '.py' in c for o in only)]
    if part:
        k, n = part
        todo = todo[k::n]
    running = []
    done = []
    while todo or running:
        while todo and len(running) < jobs and time.time() - t0 < budget:
            c = todo.pop(0)
            out = os.path.join(dest, final_path(c))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            part = out[:-4] + '.part.mp4'
            p = subprocess.Popen([sys.executable, os.path.join(HERE, 'make.py'), c, part],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
                                 env=dict(os.environ, PYTHONHASHSEED='0'))  # set iteration order reproducible
            running.append((p, c, part, out))
        if not running:
            break
        time.sleep(0.5)
        for r in running[:]:
            p, c, part, out = r
            if p.poll() is not None:
                running.remove(r)
                if p.returncode == 0 and os.path.exists(part):
                    os.replace(part, out)
                    done.append(os.path.relpath(c, HERE))
                else:
                    print('FAIL', c, (p.stderr.read() or '')[-400:])
    print(f'rendered {len(done)}: {done}; remaining {len(todo)}; {time.time() - t0:.0f}s')


def index(dest):
    lines = ['---', 'title: Hot100 动画索引', 'tags: [leetcode, hot100, 动画]', '---', '',
             '# 🎬 LeetCode Hot100 动画讲解', '',
             '每题两个视频：**灵茶山艾府** 和 **yiduobo** 的解法；每个分类开头有一个「概念讲解」视频（通用思想 + 模板）。',
             '视频由 `tools/lc_video` 生成：真正执行大神代码并逐行可视化。',
             '配套阅读：[[Python刷题函数/两位大神差异对照|两位大神差异对照]] · [[Python刷题函数/Python 刷题函数从零讲解|Python 刷题函数从零讲解]]', '']
    for cat in CATS:
        cd = cat_dir(cat)
        lines += [f'## {cd}', '']
        concept = os.path.join(cd, f'00 {cat} · 概念讲解.mp4')
        if os.path.exists(os.path.join(dest, concept)):
            lines.append(f'- 📘 概念讲解：[[hot100动画/{concept}|{cat} · 通用思想与模板]]')
            lines.append('')
        lines += ['| 题号 | 题目 | 灵茶山艾府 | yiduobo |', '|---|---|---|---|']
        for it in [x for x in ITEMS if x['cat'] == cat]:
            cells = []
            for d in ('ling', 'yiduobo'):
                fp = final_path(os.path.join(HERE, 'configs', d, f"{it['num']:04d}.py"))
                cells.append(f'[[hot100动画/{fp}\\|▶︎ 观看]]' if os.path.exists(os.path.join(dest, fp)) else '—')
            lines.append(f"| {it['num']} | {it['title']} | {cells[0]} | {cells[1]} |")
        lines.append('')
    open(os.path.join(dest, '00 Hot100 动画索引.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    print('index written')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'paths':
        for c in all_configs():
            print(os.path.relpath(c, HERE), '->', final_path(c))
    elif cmd == 'render':
        args = sys.argv[2:]
        dest = args[0]
        jobs = int(args[args.index('--jobs') + 1]) if '--jobs' in args else 3
        budget = float(args[args.index('--budget') + 1]) if '--budget' in args else 160
        dirs = tuple(args[args.index('--dirs') + 1].split(',')) if '--dirs' in args else ('concept', 'ling', 'yiduobo')
        only = args[args.index('--only') + 1].split(',') if '--only' in args else None
        part = tuple(int(x) for x in args[args.index('--part') + 1].split('/')) if '--part' in args else None
        newer = float(args[args.index('--newer') + 1]) if '--newer' in args else None
        render(dest, jobs, budget, dirs, only, '--force' in args, part, newer)
    elif cmd == 'index':
        index(sys.argv[2])
