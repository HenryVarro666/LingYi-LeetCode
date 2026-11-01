PARENTS = [-1, 2, 0, 2, 0]
NN = len(PARENTS)
CH = {v: [] for v in range(NN)}
for _w in range(1, NN):
    CH[PARENTS[_w]].append(_w)
PRE = []


def _pre(v):
    PRE.append(v)
    for c in CH[v]:
        _pre(c)


_pre(0)
SZ, SC = {}, {}


def _sz(v):
    s = sc = 1
    for c in CH[v]:
        t = _sz(c)
        s += t
        sc *= t
    SZ[v] = s
    SC[v] = sc * (NN - s if v > 0 else 1)
    return s


_sz(0)
DEPTH = {0: 0}
for _v in PRE[1:]:
    DEPTH[_v] = DEPTH[PARENTS[_v]] + 1
XP = {}
_leaf = [0]


def _xp(v):
    if not CH[v]:
        XP[v] = _leaf[0]
        _leaf[0] += 1
    else:
        for c in CH[v]:
            _xp(c)
        XP[v] = (XP[CH[v][0]] + XP[CH[v][-1]]) / 2


_xp(0)


def _sub(x):
    out = {x}
    for c in CH[x]:
        out |= _sub(c)
    return out


def _state(S, B):
    inner = S['_inner']
    v = inner.get('v')
    line = S.get('_line', 0)
    if v is None:
        return None, set(), set(), False
    anc = set()
    x = v
    while x > 0:
        x = PARENTS[x]
        anc.add(x)
    fin = {x for x in range(NN) if PRE.index(x) < PRE.index(v) and x not in anc}
    kids = CH[v]
    w = inner.get('w')
    if line >= 18:
        part = kids
    elif w is not None and line == 14 and ((B.get('_inner') or {}).get('w') == w):
        part = kids
    elif w is not None and line in (16, 17):
        part = kids[:kids.index(w) + 1]
    elif w is not None:
        part = kids[:kids.index(w)]
    else:
        part = []
    for c in part:
        fin |= _sub(c)
    return v, anc, fin, line >= 20


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    v, anc, fin, scored = _state(S, B)
    cv.text((x0 + 18, y0 + 4), '橙 = 当前，蓝 = 祖先，绿 = 已返回（附 score）', 22, T['muted'], bold=True)
    nl = max(XP.values()) + 1
    md = max(DEPTH.values()) + 1
    W = x1 - x0 - 80
    sp = min(150, W / nl)
    dy = min(120, (y1 - y0 - 110) / md)
    rad = 26
    sx = x0 + 40 + (W - sp * nl) / 2 + sp / 2
    pos = {k: (sx + XP[k] * sp, y0 + 70 + DEPTH[k] * dy + rad) for k in range(NN)}
    for k in range(1, NN):
        cv.line([pos[PARENTS[k]], pos[k]], T['border'], 3)
    for k in range(NN):
        X, Y = pos[k]
        if k == v:
            fill, ol = T['orange'], T['yellow']
        elif k in fin:
            fill, ol = T['green'], T['border']
        elif k in anc:
            fill, ol = T['blue'], T['border']
        else:
            fill, ol = T['panel2'], T['border']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=ol, width=3)
        cv.text((X, Y), k, 26, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if k in fin or (k == v and scored):
            cv.text((X, Y + rad + 8), f'score {SC[k]}', 20, T['green'], anchor='mt', bold=True)


def _cap_loop(S, B, ret):
    v = S['_inner']['v']
    kids = S.g[v]
    w = S['_inner'].get('w')
    if w is None or w not in kids:
        return f'节点 `{v}` 没有子节点（`g[{v}] = []`）→ 直接算它自己的分数'
    if (B.get('_inner') or {}).get('w') == w:
        return f'`{v}` 的儿子 `{kids}` 都处理完了 → 循环结束，下面算「剩下那块」'
    return f'遍历 `{v}` 的子节点：下一个是 `w = {w}`，先去算它的子树大小'


def _cap_mul(S, B, ret):
    i = S['_inner']
    return (f'儿子 `{i["w"]}` 的子树有 `sz = {i["sz"]}` 个点：`size` 累加成 `{i["size"]}`；'
            f'删掉 `{i["v"]}` 后它是独立的一块，`score` × {i["sz"]} → {i["score"]}')


def _cap_size(S, B, ret):
    i = S['_inner']
    return f'`size += sz`：以 `{i["v"]}` 为根的子树目前有 `{i["size"]}` 个点'


def _cap_rest(S, B, ret):
    i = S['_inner']
    return (f'`{i["v"]}` 不是根：整棵树去掉它的子树，剩下 `n - size = {S.n} - {i["size"]} = {S.n - i["size"]}` 个点，'
            f'这也是一块 → `score` = =={i["score"]}==')


def _cap_gt(S, B, ret):
    i = S['_inner']
    return (f'`score = {i["score"]}` 比 `max_score = {S.max_score}` 大 → 创下新纪录' if i['score'] > S.max_score
            else f'`score = {i["score"]}` 没超过 `max_score = {S.max_score}` → 不是新纪录')


CONFIG = dict(
    num=2049, title='统计最高分的节点数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 一次算出子树大小与分数（Go 原文转写）',
    tags=['灵神题单·链表树与回溯', '难度分 1912'],
    code='''
class Solution:
    def countHighestScoreNodes(self, parents: List[int]) -> int:
        n = len(parents)
        g = [[] for _ in range(n)]
        for w in range(1, n):
            v = parents[w]
            g[v].append(w)  # 建树

        ans = 0
        max_score = 0
        def dfs(v: int) -> int:
            nonlocal ans, max_score
            size = score = 1
            for w in g[v]:
                sz = dfs(w)
                size += sz  # 统计以 v 为根的子树的大小
                score *= sz  # 由于是二叉树所以 score 最大约为 (1e5/3)^3，在 64 位整数范围内
            if v > 0:
                score *= n - size  # 如果不是根节点，还要乘上「整棵树去掉以 v 为根的子树后，剩余的部分」
            if score > max_score:
                max_score, ans = score, 1
            elif score == max_score:
                ans += 1
            return size
        dfs(0)
        return ans
''',
    call='Solution().countHighestScoreNodes([-1, 2, 0, 2, 0])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=170),
    ],
    watch=[('v', lambda S: S['_inner'].get('v'), 'blue'), ('size', lambda S: S['_inner'].get('size')),
           ('score', lambda S: S['_inner'].get('score'), 'yellow'), ('max_score', 'max_score', 'orange'), ('ans', 'ans', 'green')],
    skip=['nonlocal', 'g = [[]', 'n = len', 'for w in range(1, n)', 'v = parents[w]', 'ans = 0', 'max_score = 0', 'size += sz', 'if v > 0'],
    captions={
        'g[v].append': '建树：节点 `{w}` 的父亲是 `{v}`，挂到 `g[{v}]` 里 → `g = {g}`',
        'size = score = 1': '先把自己算作 `size = 1`；`score` 从 1 开始连乘',
        'for w in g[v]': _cap_loop,
        'sz = dfs(w)': '递归求儿子 `{w}` 的子树大小 `sz`',
        'score *= sz': _cap_mul,
        'score *= n - size': _cap_rest,
        'if score > max_score': _cap_gt,
        'max_score, ans = score, 1': '最高分刷新为 `{max_score}`，取得的节点数重置为 `1`',
        'elif score == max_score': lambda S, B, ret: ('`score == max_score` → 并列最高' if S.score == S.max_score else '`score` 小于最高分 → 什么也不做'),
        'ans += 1': '并列最高：`ans = {ans}`',
        'return size': '把子树大小 `{ret}` 返回给父节点去乘',
    },
    cards=dict(
        one_liner='删掉一个点，剩下的就是它的各个子树加上「其余部分」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树的根是 `0`，`parents[i]` 是 `i` 的父节点',
                 '删掉一个节点，剩下若干子树，==分数 = 各子树大小之积==',
                 '求最高分的节点有几个。示例 `[-1,2,0,2,0]` → `3`'],
        quote='删除与 v 相连的边，剩余部分可以分为两类：以 v 的子节点为根的子树；整棵树去掉以 v 为根的子树后，剩余的部分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['剩余部分分两类：==v 的各个儿子子树==，以及==整棵树去掉 v 的子树后剩下的==',
              '从 0 出发跑一次 DFS，边算子树大小 `size`，边把儿子子树大小连乘进 `score`',
              '非根节点再乘 `n - size`，然后和 `max_score` 比，顺手维护计数 `ans`'],
        result='运行结束，返回 `3`：节点 1、3、4 的分数都是最高分 4',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`nonlocal` 代替闭包捕获 `ans`、`maxScore`）',
                 '时间 `O(n)`，空间 `O(n)`；每个点只递归一次',
                 '易错：根节点没有「剩下的那块」，不能乘 `n - size`（此时为 0）',
                 '原文提醒：二叉树最多乘三项，分数不会爆 64 位整数；Python 本身不会溢出'],
    ),
)
