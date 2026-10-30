def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
PARENT = [-1, 0, 0, 1, 3]
CH = {}
for _i, _p in enumerate(PARENT):
    if _p != -1:
        CH.setdefault(_p, []).append(_i)


def _colors(S):
    if 'now' in S and S['now'] is not None and S['now'] >= 0:
        return {S['now']: 'pink'}
    if 'index' in S and S.get('index') is not None and 'level' in S:
        return {S['index']: 'yellow'}
    return {}


def _f(S):
    return S.get('self.f')


def _cell(S, r, c, v):
    if 'now' in S:
        return 'pink' if (r, c) == (S['now'], S.get('level')) else None
    if 'index' in S and 'level' in S:
        if (r, c) == (S['index'], S['level']):
            return 'yellow'
        f = S.get('self.f')
        lv = S['level']
        if lv > 0 and (r, c) == (S['index'], lv - 1):
            return 'blue'
        try:
            m = f[S['index']][lv - 1]
            if lv > 0 and m != -1 and (r, c) == (m, lv - 1):
                return 'green'
        except Exception:
            pass
    return None


def _formula(S):
    if 'now' in S:
        return f"当前在 `{S['now']}`，还要走 `k = {S['k']}` 步，`level = {S['level']}`（一次走 `2^{S['level']}` 步）"
    return '`f[i][j]`：从 `i` 往上走 `2^j` 步到达的节点；`f[i][j] = f[f[i][j-1]][j-1]`'


CONFIG = dict(
    num=1483, title='树节点的第 K 个祖先', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='倍增 DP（f[i][j] 表示走 2^j 步）',
    tags=['链表树与回溯', '难度分 2115'],
    code='''
class TreeAncestor(object):

    def __init__(self, n, parent):

        self.p = 0
        self.pow2 = [1]
        while self.pow2[-1] < n - 1:
            self.p += 1
            self.pow2.append(self.pow2[-1] + self.pow2[-1])
        
        self.f = [[None] * (self.p + 1) for _ in range(n)]
        for level in range(self.p + 1):
            for index in range(n):
                if level == 0:
                    self.f[index][level] = parent[index]
                elif self.f[index][level - 1] != -1:
                    self.f[index][level] = self.f[self.f[index][level - 1]][level - 1]
                else:
                    self.f[index][level] = -1

    def getKthAncestor(self, node, k):

        now = node
        level = self.p
        while now != -1 and k > 0:
            while k < self.pow2[level]:
                level -= 1
            
            now = self.f[now][level]
            k -= self.pow2[level]
        
        return now
''',
    call='''t = TreeAncestor(5, [-1, 0, 0, 1, 3])
[t.getKthAncestor(4, 3), t.getKthAncestor(4, 2), t.getKthAncestor(2, 2)]''',
    expect=[0, 1, -1],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(_tree_view(CH, 0, _colors, '树（黄 = 正在填表的节点，粉 = 查询时走到的节点）'), h=340),
        dict(type='array', var='self.pow2', label="pow2：可以一步走的距离", h=170, cell=60),
        dict(type='table', var=_f, label='f[i][j]：行 = 节点 i，列 = j（· = 未填）', rows=list(range(5)), cols=[0, 1, 2],
             color=_cell, cell=66, h=340),
    ],
    watch=['self.p', 'level', 'index', ('now', 'now', 'pink'), 'k'],
    max_steps=72,
    skip=['for index in range', 'if level == 0', 'while now != -1'],
    captions={
        'self.pow2 = [1]': '`pow2[j] = 2^j`，先放 `1`',
        'self.p = 0': '`p` 记录最高的 `j`：要覆盖到 `n - 1` 步',
        'while self.pow2[-1] < n - 1': lambda S, B, ret: (f"`{S['self.pow2'][-1]} < n - 1 = {S.n - 1}`：还不够，继续翻倍" if S['self.pow2'][-1] < S.n - 1
                                                         else f"`{S['self.pow2'][-1]} >= {S.n - 1}`：够覆盖整棵树的深度，停"),
        'self.p += 1': '多一档：`p` = {self.p}',
        'self.pow2.append': '`pow2` 加一项：`{self.pow2[-1]}` = 前一项 + 前一项',
        'self.f = [[None]': '`f` 是 `n` 行 `p + 1` 列的表，先全部留空',
        'for level in range': '外层枚举 `level`：先填完走 `2^(level-1)` 步，才能填 `2^level` 步',
        'for index in range': '处理节点 `index = {index}`',
        'if level == 0': lambda S, B, ret: ('`level == 0`：走 1 步，就是父亲' if S.level == 0 else '`level > 0`：要用上一列拼'),
        'self.f[index][level] = parent[index]': '`f[{index}][0] = parent[{index}]` = =={self.f[index][0]}==',
        'elif self.f[index][level - 1] != -1': lambda S, B, ret: (f"`f[{S.index}][{S.level - 1}] = {S['self.f'][S.index][S.level - 1]}`：走过一半还在树里，可以再走一半" if S['self.f'][S.index][S.level - 1] != -1
                                                                 else f"`f[{S.index}][{S.level - 1}] = -1`：走一半就出树了，这一格也是 `-1`"),
        'self.f[index][level] = self.f[self.f[index][level - 1]]': '`f[i][j] = f[f[i][j-1]][j-1]`：`f[{index}][{level}]` = ==`{self.f[index][level]}`==',
        'self.f[index][level] = -1': '`f[{index}][{level}] = -1`：祖先不存在',
        'now = node': '从 `{now}` 出发，还要走 `k = {k}` 步',
        'level = self.p': '从最大的一档 `level = {level}` 开始试',
        'while now != -1 and k > 0': lambda S, B, ret: (f'`now = {S.now}`，`k = {S.k}`：还没走完，继续' if (S.now != -1 and S.k > 0)
                                                        else (f'`k = 0`：恰好走完' if S.k == 0 else '`now = -1`：祖先不够，结束')),
        'while k < self.pow2[level]': lambda S, B, ret: (f"`k = {S.k} < 2^{S.level} = {S['self.pow2'][S.level]}`：这一步迈太大，降一档" if S.k < S['self.pow2'][S.level]
                                                          else f"`k = {S.k} >= 2^{S.level} = {S['self.pow2'][S.level]}`：这一档可以走"),
        'level -= 1': '`level` 降到 {level}',
        'now = self.f[now][level]': '查表走 `2^{level}` 步：到 ==`{now}`==',
        'k -= self.pow2[level]': '剩下 `k = {k}` 步',
        'return now': '答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='f[i][j] 记下走 2^j 步到哪，k 拆成几段 2 的幂',
        complexity='预处理 `O(n log n)`，每次询问 `O(log k)`',
        problem=['树由 `parent` 数组给出，根是 `0`',
                 '`getKthAncestor(node, k)`：往上第 `k` 个祖先，没有就返回 `-1`',
                 '本视频：`parent = [-1,0,0,1,3]`，查 `(4,3)`、`(4,2)`、`(2,2)`'],
        quote='令f[i][j]表示从节点i开始，朝根节点走2^j步之后走到的节点……f[i][j] = f[i\'][j - 1] = f[f[i][j - 1]][j - 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['当成动态规划：`j = 0` 是父亲；`j > 0` 把 `2^j` 拆成两个 `2^(j-1)`',
              '填表顺序：先填完一整列（`level`），再填下一列',
              '查询：每次选 ==不超过剩余步数== 的最大一档 `pow2`，走完就减掉',
              '步数不够时 `f` 已是 `-1`，循环自然结束'],
        summary=['预处理 `O(n log n)`，询问 `O(log k)`',
                 '`p` 由 `pow2[-1] >= n - 1` 决定：最多走 `n - 1` 步',
                 '`f[i][j-1] == -1` 时直接填 `-1`，避免下标 `-1` 取到最后一行',
                 '原文就是 Python 3 可运行的写法，代码未做改动',
                 '对比灵神：灵神按 `k` 的二进制位从低到高跳；这里从高到低选最大的一档'],
    ),
)
