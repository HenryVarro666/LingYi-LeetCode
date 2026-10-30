def _q(S):
    if 't' not in S:
        return '`first[t]` / `last[t]`：第 t 种糖果在「所有糖果排成一排」里的第一颗 / 最后一颗的位置'
    t, d, c = S['t'], S['d'], S['c']
    lo, hi = d + 1, (d + 1) * c
    f, l = S['first'][t], S['last'][t]
    ok = not (f > hi or l < lo)
    return (f'第 {d + 1} 天能吃到的糖果编号：`[{lo}, {hi}]`　想吃的第 {t} 种：`[{f}, {l}]`　→ '
            + ('==有交集，能吃=='if ok else '==没有交集，不能吃=='))


def _bar(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cc = S['candiesCount']
    total = sum(cc)
    cv.text((x0 + 18, y0 + 4), '所有糖果排成一排（k 号·数量；下方数字是糖果编号）', 24, T['muted'], bold=True)
    W = x1 - x0 - 60
    unit = W / total
    sx = x0 + 30
    base = y0 + 120
    cols = [T['blue'], T['pink'], T['green'], T['purple'], T['orange']]
    p = 0
    for k, v in enumerate(cc):
        a = sx + p * unit
        b = sx + (p + v) * unit
        mine = 't' in S and S['t'] == k
        cv.rect((a + 1, base, b - 1, base + 56), fill=cols[k % 5], alpha=255 if mine else 120, r=4)
        cv.text(((a + b) / 2, base + 28), f'{k} 号·{v}', 21, T['bg'] if mine else T['text'], anchor='mm', bold=True)
        cv.text((a, base + 62), p + 1, 18, T['dim'], anchor='lt', mono=True)
        p += v
    cv.text((sx + total * unit, base + 62), total, 18, T['dim'], anchor='rt', mono=True)
    if 't' in S and 'd' in S:
        lo, hi = S['d'] + 1, min((S['d'] + 1) * S['c'], total)
        if lo <= total:
            a = sx + (lo - 1) * unit
            b = sx + hi * unit
            cv.rect((a, base - 46, max(b, a + 6), base - 8), fill=T['yellow'], alpha=200, r=4)
            cv.text((a, base - 52), f'这天最少吃到第 {lo} 颗，最多吃到第 {(S["d"] + 1) * S["c"]} 颗', 21, T['yellow'], anchor='lb', bold=True)
        else:
            cv.text((sx, base - 30), f'第 {lo} 颗已经超出总数 {total}：糖果最晚也吃完了', 21, T['red'], anchor='lm', bold=True)
        if 'first' in S and len(S['first']) > S['t']:
            pass


CONFIG = dict(
    num=1744, title='你能在你最喜欢的那天吃到你最喜欢的糖果吗？', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 区间相交',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def canEat(self, candiesCount, queries):

        n = len(candiesCount)
        first = []
        last = []
        s = 0
        for candies in candiesCount:
            first.append(s + 1)
            s += candies
            last.append(s)
        
        res = []
        for t, d, c in queries:
            if first[t] > (d + 1) * c or last[t] < d + 1:
                res.append(False)
            else:
                res.append(True)
        
        return res
''',
    call='Solution().canEat([7, 4, 5, 3, 8], [[0, 2, 2], [4, 2, 4], [2, 13, 1000000000]])',
    expect=[True, False, True],
    views=[
        dict(type='text', fn=_q),
        dict(type='custom', draw=_bar, h=230),
        dict(type='array', var='first', label='first', h=150),
        dict(type='array', var='last', label='last', h=150),
        dict(type='array', var='res', label='res', h=140),
    ],
    watch=[('s', 's', 'cyan'), ('t', 't', 'blue'), ('d', 'd', 'pink'), ('c', 'c', 'orange')],
    skip=['n = len', 'first = []', 'last = []', 's = 0', 'res = []'],
    captions={
        'for candies in candiesCount': '前缀和 `s`：已经排在前面的糖果数；下一种糖果有 `{candies}` 颗',
        'first.append(s + 1)': '这一种的第一颗排在 `s + 1 = {s + 1}`',
        's += candies': '`s` 加上这一种的数量 `{candies}` → `{s}`',
        'last.append(s)': '这一种的最后一颗正好是前缀和 `{s}`：这一种占 `[{first[-1]}, {last[-1]}]`',
        'for t, d, c in queries': '询问：第 `{t}` 种，第 `{d}` 天（从 0 数），每天最多 `{c}` 颗',
        'if first[t] > (d + 1) * c or last[t] < d + 1': lambda S, B, r: (
            f'每天至少 1 颗 → 第 {S.d + 1} 天最少吃到第 `{S.d + 1}` 颗；每天最多 {S.c} 颗 → 最多吃到第 `{(S.d + 1) * S.c}` 颗。'
            + (f'想吃的最早在 `{S.first[S.t]}`，比 `{(S.d + 1) * S.c}` 还大 → ==吃不到==' if S.first[S.t] > (S.d + 1) * S.c
               else f'想吃的最晚在 `{S.last[S.t]}`，比 `{S.d + 1}` 还小 → ==早已吃光=='if S.last[S.t] < S.d + 1
               else '两个区间有交集 → ==能吃到==')),
        'res.append(False)': '两个区间不相交 → 追加 `False`',
        'res.append(True)': '两个区间相交 → 追加 `True`',
    },
    cards=dict(
        one_liner='第 n 天能吃到的糖果编号是一个区间，和目标种类的区间有没有交集',
        complexity='预处理 `O(n)`，每个询问 `O(1)`，空间 `O(n)`',
        problem=['`candiesCount[i]` 是第 `i` 种糖果的数量，按种类顺序一颗颗吃，==每天至少吃 1 颗==',
                 '询问 `[type, day, cap]`：每天最多吃 `cap` 颗，第 `day` 天（从 0 数）能不能吃到第 `type` 种',
                 '本视频：`[7,4,5,3,8]`，询问 `[[0,2,2],[4,2,4],[2,13,10^9]]` → `[true,false,true]`'],
        quote='每天最多吃dailyCap[i]颗糖果，因此第n天最多吃到第dailyCap[i] * n颗糖果。相对的，每天至少吃一颗糖果，因此第n天至少需要吃掉n颗糖果。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `n` 天（从 1 数）吃到的糖果编号落在 `[n, n × cap]`',
              '想吃的那种占 `[first, last]`，前缀和 `s` 给出：`first = s[t−1] + 1`，`last = s[t]`',
              '不相交只有两种：`first > n × cap`（吃不到）或 `last < n`（早吃完）'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`day` 从 0 数，所以代码里是 `d + 1`',
                 '`(d + 1) * c` 可能很大，Python 不会溢出；别的语言要用 64 位',
                 '代码本身是 Python 3 可运行的，未做修改（`n = len(...)` 没有用到）'],
    ),
)
