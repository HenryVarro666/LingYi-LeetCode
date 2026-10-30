import re as _re

DONE = {}
BASE = [5, 8, 2, 1, 3, 4]
EDGES = [[0, 1], [0, 2], [2, 3], [2, 4], [1, 5]]


class BT(list):
    """带 done 属性的 baseTime：字幕回调把「已完成的任务 → 完成时间」存在它上面，供画图读取"""
    done = {}


def _fmt(t):
    def f(S, B, r):
        env = {'B': B, 'ret': r, 'len': len, 'max': max, 'min': min}
        return _re.sub(r'\{([^{}]+)\}', lambda m: str(eval(m.group(1), env, S)), t)
    return f


def _rec(fn, var, record=False):
    def cap(S, B, ret):
        if record and S.get(var) is not None:
            DONE[S.get(var)] = ret
        bt = S.get('baseTime')
        if bt is not None:
            bt.done = dict(DONE)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _wrap(d, var):
    return {k: _rec(v if callable(v) else _fmt(v), var) for k, v in d.items()}


def _layout():
    ch = {i: [] for i in range(len(BASE))}
    for u, v in EDGES:
        ch[u].append(v)
    pos, cnt = {}, [0]

    def go(u, d):
        if not ch[u]:
            pos[u] = (cnt[0], d)
            cnt[0] += 1
            return
        for v in ch[u]:
            go(v, d + 1)
        pos[u] = (sum(pos[v][0] for v in ch[u]) / len(ch[u]), d)
    go(0, 0)
    return ch, pos, cnt[0]


def _make_draw(cur, lo, hi):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        ch, pos, nleaf = _layout()
        bt = S.get('baseTime')
        done = getattr(bt, 'done', {}) if bt is not None else {}
        x = S.get(cur)
        sp = min(150, (x1 - x0 - 120) / max(1, nleaf - 1))
        sx = x0 + (x1 - x0 - sp * (nleaf - 1)) / 2
        dy = 128
        R = 26

        def P(u):
            return sx + pos[u][0] * sp, y0 + 70 + pos[u][1] * dy
        cv.text((x0 + 18, y0 + 6), '任务树（蓝 = 正在算，绿 = 已算出完成时间）', 22, T['muted'], bold=True)
        for u in ch:
            for v in ch[u]:
                cv.line([P(u), P(v)], T['border'], 3)
        for u in ch:
            X, Y = P(u)
            fill = T['green'] if u in done else (T['blue'] if u == x else T['panel2'])
            cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['yellow'] if u == x else T['border'], width=3, r=R)
            cv.text((X, Y), u, 26, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
            cv.text((X, Y + R + 14), f'base={BASE[u]}', 18, T['dim'], anchor='mm')
            if u in done:
                s = f'完成 {done[u]}'
                w = cv.tlen(s, 20, bold=True) + 16
                cv.rect((X - w / 2, Y + R + 28, X + w / 2, Y + R + 54), fill=T['panel'], outline=T['green'], width=2, r=8)
                cv.text((X, Y + R + 41), s, 20, T['green'], anchor='mm', bold=True)
        if x is not None:
            e, l = S.get(lo), S.get(hi)
            if isinstance(e, (int, float)) and l is not None and e != float('inf'):
                X, Y = P(x)
                cv.text((X + R + 10, Y - 14), f'earliest={e}', 18, T['cyan'], anchor='lm', bold=True)
                cv.text((X + R + 10, Y + 8), f'latest={l}', 18, T['pink'], anchor='lm', bold=True)
    return draw


CONFIG = dict(
    num=3965, title='任务完成时间 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 DFS 模拟',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1699'],
    code='''
class Solution:
    def finishTime(self, n: int, edges: list[list[int]], baseTime: list[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)  # 题目保证 x 是 y 的父节点

        def dfs(x: int) -> int:
            if not g[x]:  # x 是叶子
                return baseTime[x]
            earliest = inf
            latest = 0
            for y in g[x]:
                t = dfs(y)
                earliest = min(earliest, t)
                latest = max(latest, t)
            return latest * 2 - earliest + baseTime[x]

        return dfs(0)
''',
    setup='''class BT(list):
    done = {}
''',
    call='Solution().finishTime(6, [[0,1],[0,2],[2,3],[2,4],[1,5]], BT([5,8,2,1,3,4]))',
    expect=22,
    views=[
        dict(type='custom', draw=_make_draw('x', 'earliest', 'latest'), h=440),
        dict(type='calls', h=190, hide=('edges', 'baseTime', 'n', 'g')),
    ],
    watch=[('x', 'x', 'blue'), ('t', lambda S: S['_inner'].get('t')), ('earliest', lambda S: S['_inner'].get('earliest'), 'cyan'),
           ('latest', lambda S: S['_inner'].get('latest'), 'pink')],
    captions=_wrap({
        'g = [[': lambda S, B, r: DONE.clear() or '`g[x]` 存任务 `x` 的所有==子任务==，先建好邻接表',
        'g[x].append': '`{x}` 是 `{y}` 的父节点 → `g[{x}] = {g[x]}`（题目保证有向，不用记 `y→x`）',
        'return dfs(0)': '从根任务 `0` 开始自底向上 DFS：==儿子的完成时间先算出来，才能算父亲==',
        'if not g[x]': lambda S, B, r: f'任务 `{S.x}` ' + ('没有子任务 → 是==叶子==' if not S.g[S.x] else f'有子任务 `{S.g[S.x]}` → 非叶子，要看儿子的完成时间'),
        'return baseTime[x]': _rec(_fmt('叶子的完成时间就是 `baseTime[{x}] = {ret}`'), 'x', True),
        'earliest = inf': '`earliest` 取儿子完成时间的==最小值==，初始为无穷大',
        'latest = 0': '`latest` 取儿子完成时间的==最大值==，初始 `0`（完成时间 ≥ 1）',
        'for y in g[x]': '遍历任务 `{x}` 的子任务 `{y}`',
        't = dfs(y)': lambda S, B, r: f'递归求子任务 `{S.y}` 的完成时间' if 't' not in S or S.get('t') == B.get('t') else f'子任务 `{S.y}` 完成时间 `t = {S.t}`',
        'earliest = min': '`earliest = min({B.earliest}, {t})` = =={earliest}==',
        'latest = max': '`latest = max({B.latest}, {t})` = =={latest}==',
        'return latest * 2': _rec(lambda S, B, r: f'`latest*2 - earliest + base` = `{S.latest}*2 - {S.earliest} + {S.baseTime[S.x]}` = =={r}==：即 `latest + ((latest - earliest) + base)`', 'x', True),
    }, 'x'),
    skip=['for y in g[x]', 'for x, y in edges'],
    max_steps=90,
    cards=dict(
        one_liner='父任务的完成时间 = `latest*2 - earliest + base`，自底向上算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个任务组成以 `0` 为根的树，`edges[i] = [u, v]` 表示 `u` 是 `v` 的父任务',
                 '叶子完成时间 = `baseTime[i]`；非叶子：`latest + ((latest - earliest) + baseTime[i])`',
                 '`earliest/latest` 是==子任务==完成时间的最小/最大值',
                 '本视频：`n=6`，示例树，根任务 `0` 的完成时间为 `22`'],
        quote='按题意模拟即可，写一个自底向上的 DFS。注意：计算的是儿子的最小最大完成时间，不是子树中的所有节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先建有向邻接表 `g`：题目保证 `x` 是 `y` 的父节点，不用建反向边',
              '`dfs(x)` 返回任务 `x` 的完成时间：叶子直接返回 `baseTime[x]`',
              '非叶子遍历儿子，维护 `earliest` 和 `latest`，把公式化简成 `latest*2 - earliest + baseTime[x]`'],
        result='根任务 `0`：儿子完成时间 `12` 和 `7`，`12*2 - 7 + 5 = 22`',
        summary=['时间 `O(n)`，空间 `O(n)`（`g` 和递归栈）',
                 '易错：`earliest/latest` 只看==直接儿子==的完成时间，不是整棵子树',
                 '公式 `latest + (latest - earliest) + base` 合并成 `latest * 2 - earliest + base`',
                 '同类题：「§3.3 自底向上 DFS」；`n` 最大 `10^5`，Python 递归深度需要注意'],
    ),
)
