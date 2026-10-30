"""More problem lists (面试经典150 / 热题173 / 字节30天 / List.md): names, render loop, index.

python sets.py paths
python sets.py render DEST --jobs 5 --budget 110 [--part 0/2] [--newer EPOCH]   # DEST = <Leetcode>/题单动画
python sets.py index DEST
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hot100  # noqa: E402

ITEMS = json.load(open(os.path.join(HERE, 'extra.json'), encoding='utf-8'))
BYNUM = {it['num']: it for it in ITEMS}
SETS = json.load(open(os.path.join(HERE, 'sets_full.json'), encoding='utf-8'))
CATS = ['哈希', '双指针', '滑动窗口', '子串', '普通数组', '矩阵', '链表', '二叉树', '图论', '回溯', '二分查找', '栈', '堆',
        '贪心算法', '动态规划', '多维动态规划', '技巧', '数学', '字符串', '设计']
AUTHOR = {'ling2': '灵茶山艾府', 'yiduobo2': 'yiduobo'}
DIRS = ('ling2', 'yiduobo2')


def cfg_category(cfg_path):
    m = re.search(r"category\s*=\s*['\"]([^'\"]+)['\"]", open(cfg_path, encoding='utf-8').read())
    c = m.group(1) if m else '其他'
    return c if c in CATS else '其他'


def cat_dir(cat):
    return f'{CATS.index(cat) + 1:02d} {cat}' if cat in CATS else '99 其他'


def final_path(cfg_path):
    d = os.path.basename(os.path.dirname(cfg_path))
    num = int(os.path.splitext(os.path.basename(cfg_path))[0])
    title = BYNUM[num]['title'].replace('/', '／')
    return os.path.join(cat_dir(cfg_category(cfg_path)), f'{num:04d} {title} · {AUTHOR[d]}.mp4')


def all_configs(dirs=DIRS):
    out = []
    for d in dirs:
        out += sorted(glob.glob(os.path.join(HERE, 'configs', d, '*.py')))
    return out


def render(dest, jobs=3, budget=160, only=None, part=None, newer=None, force=False):
    # reuse hot100's loop by temporarily swapping its path function
    hot100.final_path, old = final_path, hot100.final_path
    hot100.all_configs, old_all = (lambda dirs=None: all_configs()), hot100.all_configs
    try:
        hot100.render(dest, jobs, budget, DIRS, only, force, part, newer)
    finally:
        hot100.final_path, hot100.all_configs = old, old_all


def index(dest, hot_dest_rel='hot100动画', sets_rel='题单动画'):
    root = os.path.dirname(dest)
    lines = ['---', 'title: 题单动画索引', 'tags: [leetcode, 题单, 动画]', '---', '',
             '# 🎬 更多题单动画讲解', '',
             '面试经典 150 / LeetCode 热题 173 / 字节跳动近 30 天高频 / List.md 课后题。和 Hot100 重复的题直接链到 '
             f'[[{hot_dest_rel}/00 Hot100 动画索引|Hot100 动画]] 里的视频；其余视频按算法分类放在本文件夹。', '']

    def links(num):
        cells = []
        for d_hot, d_x in (('ling', 'ling2'), ('yiduobo', 'yiduobo2')):
            fp = None
            if num in hot100.BYNUM:
                p = hot100.final_path(os.path.join(HERE, 'configs', d_hot, f'{num:04d}.py'))
                if os.path.exists(os.path.join(root, hot_dest_rel, p)):
                    fp = f'{hot_dest_rel}/{p}'
            else:
                c = os.path.join(HERE, 'configs', d_x, f'{num:04d}.py')
                if os.path.exists(c):
                    p = final_path(c)
                    if os.path.exists(os.path.join(dest, p)):
                        fp = f'{sets_rel}/{p}'
            cells.append(f'[[{fp}\\|▶︎]]' if fp else '—')
        return cells

    for name, rows in SETS.items():
        have = 0
        body = ['| 题号 | 题目 | 灵茶山艾府 | yiduobo |', '|---|---|---|---|']
        for row in rows:
            num = row[0]
            title = (BYNUM.get(num) or hot100.BYNUM.get(num) or {}).get('title') or row[1]
            c = links(num)
            have += any(x != '—' for x in c)
            tag = ' `Hot100`' if num in hot100.BYNUM else ''
            body.append(f'| {num} | {title}{tag} | {c[0]} | {c[1]} |')
        lines += [f'## {name}（{have}/{len(rows)} 题有视频）', ''] + body + ['']
    open(os.path.join(dest, '00 题单动画索引.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    print('index written')


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'paths':
        for c in all_configs():
            print(os.path.relpath(c, HERE), '->', final_path(c))
    elif cmd == 'render':
        g = lambda k, f=str, d=None: f(args[args.index(k) + 1]) if k in args else d  # noqa: E731
        render(args[0], g('--jobs', int, 3), g('--budget', float, 160),
               args[args.index('--only') + 1].split(',') if '--only' in args else None,
               tuple(int(x) for x in g('--part').split('/')) if '--part' in args else None,
               g('--newer', float), '--force' in args)
    elif cmd == 'index':
        index(args[0])
