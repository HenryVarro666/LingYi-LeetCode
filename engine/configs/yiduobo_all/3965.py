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
    author='yiduobo', technique='无向建图 + 自底向上 DFS',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1699'],
    code='''
class Solution(object):
    def finishTime(self, n, edges, baseTime):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        def dfs(now, fa):
            earliest = None
            latest = None
            for nxt in g[now]:
                if nxt == fa:
                    continue
                t = dfs(nxt, now)
                if earliest is None or earliest > t:
                    earliest = t
                if latest is None or latest < t:
                    latest = t
            
            if earliest is None:
                return baseTime[now]
            else:
                return latest + (latest - earliest) + baseTime[now]
        
        return dfs(0, -1)
''',
    setup='''class BT(list):
    done = {}
''',
    call='Solution().finishTime(6, [[0,1],[0,2],[2,3],[2,4],[1,5]], BT([5,8,2,1,3,4]))',
    expect=22,
    views=[
        dict(type='custom', draw=_make_draw('now', 'earliest', 'latest'), h=440),
        dict(type='calls', h=190, hide=('edges', 'baseTime', 'n', 'g', 'self')),
    ],
    watch=[('now', 'now', 'blue'), ('fa', lambda S: S['_inner'].get('fa')), ('t', lambda S: S['_inner'].get('t')),
           ('earliest', lambda S: S['_inner'].get('earliest'), 'cyan'), ('latest', lambda S: S['_inner'].get('latest'), 'pink')],
    captions=_wrap({
        'g = [[': lambda S, B, r: DONE.clear() or '无向建图：每条边两头都记，所以要用 `fa` 防止走回父亲',
        'g[x].append(y)': '`{x}` → `{y}`：`g[{x}] = {g[x]}`',
        'g[y].append(x)': '反向也记一条：`g[{y}] = {g[y]}`（因此邻居里会混入父亲）',
        'return dfs(0, -1)': '从根 `0` 出发，`fa = -1` 表示没有父亲；==先算儿子，再算父亲==',
        'earliest = None': '`earliest/latest` 先设为 `None`：还没见到儿子；==循环完还是 `None` 就说明是叶子==',
        'for nxt in g[now]': lambda S, B, r: f'邻居 `{S.nxt}`' if 'nxt' in S else '',
        'if nxt == fa': lambda S, B, r: f'邻居 `{S.nxt}` ' + ('就是父亲 `fa` → 跳过' if S.nxt == S.fa else f'不是父亲 `{S.fa}` → 它是儿子，往下算'),
        'continue': '跳过父亲，不能往回走',
        't = dfs(nxt, now)': lambda S, B, r: f'递归求儿子 `{S.nxt}` 的完成时间，把当前任务 `{B.now}` 当作它的 `fa`',
        'if earliest is None or earliest >': lambda S, B, r: f'`earliest = {B.earliest}`，儿子 `t = {S.t}`：' + ('还没有记录或更小 → 更新' if B.earliest is None or B.earliest > S.t else '不比它小 → 不动'),
        'earliest = t': '`earliest = {t}`',
        'if latest is None or latest <': lambda S, B, r: f'`latest = {B.latest}`，儿子 `t = {S.t}`：' + ('还没有记录或更大 → 更新' if B.latest is None or B.latest < S.t else '不比它大 → 不动'),
        'latest = t': '`latest = {t}`',
        'if earliest is None': lambda S, B, r: ('`earliest` 还是 `None` → 没有儿子，是==叶子==' if S.earliest is None else f'有儿子：`earliest = {S.earliest}`，`latest = {S.latest}`'),
        'return baseTime[now]': _rec(_fmt('叶子的完成时间就是 `baseTime[{now}] = {ret}`'), 'now', True),
        'return latest + (latest': _rec(lambda S, B, r: f'`latest + (latest - earliest) + base` = `{S.latest} + ({S.latest} - {S.earliest}) + {S.baseTime[S.now]}` = =={r}==', 'now', True),
    }, 'now'),
    skip=['latest = None', 'for x, y in edges', 'for nxt in g[now]', 'continue', 'earliest = t', 'latest = t'],
    max_steps=110,
    cards=dict(
        one_liner='叶子取 `baseTime`；非叶子 = `latest + (latest - earliest) + base`',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个任务组成以 `0` 为根的树，`edges[i] = [u, v]` 表示 `u` 是 `v` 的父任务',
                 '叶子完成时间 = `baseTime[i]`；非叶子要用儿子的最小/最大完成时间',
                 '求根任务 `0` 的完成时间',
                 '本视频：`n=6`，根任务的完成时间为 `22`'],
        quote='对于当前节点index，若其为叶子节点，那么完成时间就是baseTime[index]，反之，则先遍历其所有孩子节点并递归计算这些节点的完成时间，记录其中最小和最大作为earliest和latest。',
        quote_src='—— yiduobo 题解',
        idea=['任务呈树形：从根 `0` 向下 DFS，叶子直接返回 `baseTime`',
              '非叶子：递归每个孩子，用 `None` 起手记录 `earliest` 和 `latest`',
              '最后按题目原式 `latest + (latest - earliest) + baseTime` 算出自己的完成时间'],
        result='根任务 `0`：儿子 `12` 和 `7`，`12 + (12 - 7) + 5 = 22`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '对比灵神：灵神只存「父→子」有向边；这里建无向图，所以要传 `fa` 并跳过父亲',
                 '易错：`earliest` 初始为 `None`，要先判断 `is None` 再比较；==只看直接孩子==',
                 '原文已是 Python 3 可运行写法，只删了文档字符串（本题原文没有），无需改动'],
    ),
)
