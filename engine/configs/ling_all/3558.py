_EDGES = [[1, 2], [1, 3], [3, 4], [3, 5], [4, 6]]
_POS = {1: (1.5, 0), 2: (0.5, 1), 3: (2.5, 1), 4: (1.9, 2), 5: (3.1, 2), 6: (1.9, 3)}
_PAR = {2: 1, 3: 1, 4: 3, 5: 3, 6: 4}


def _anc(x):
    out = []
    while x in _PAR:
        x = _PAR[x]
        out.append(x)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner') or {}
    cur = inner.get('x')
    path = set(_anc(cur)) if cur else set()
    width, height = x1 - x0 - 120, y1 - y0 - 90
    sx = x0 + 60 + width * 0.12
    sw = width * 0.76 / 3.1
    sy, sh = y0 + 90, (height - 40) / 3.2
    P = lambda v: (sx + _POS[v][0] * sw, sy + _POS[v][1] * sh)
    cv.text((x0 + 18, y0 + 4), '树（根 = 1）：黄 = 当前 dfs 的节点，蓝 = 正在等它返回的祖先', 22, T['muted'], bold=True)
    for a, b in _EDGES:
        cv.line([P(a), P(b)], T['blue'] if (b in path or b == cur) and (a in path or a == cur) else T['border'], 4)
    for v in _POS:
        X, Y = P(v)
        fill = T['yellow'] if v == cur else (T['blue'] if v in path else T['panel2'])
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, r=30, outline=T['border'])
        cv.text((X, Y), v, 28, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
    if cur:
        X, Y = P(cur)
        if 'd' in inner:
            cv.text((X + 42, Y), f"d = {inner['d']}", 24, T['yellow'], anchor='lm', bold=True)


def _for_cap(si, bi):
    if 'y' in bi and si.get('y') == bi['y']:
        return f"`{si['x']}` 的邻居都看完了，`d = {si['d']}`：往下最多 {si['d']} 条边"
    pre = f"孩子 `{bi['y']}` 返回了，`d` 变成 =={bi['d']}==；" if 'y' in bi else ''
    return pre + f"继续看 `{si['x']}` 的下一个邻居 `{si['y']}`"


def _txt(S):
    if 'k' in S:
        k = S['k']
        return f'最深节点离根 `{k}` 条边：奇数个 1 的选法 = `2^(k−1)` = `2^{k - 1}` = =={2 ** (k - 1)}=='
    return 'dfs 返回的是「以 x 为根的子树，从 x 往下最多几条边」'


CONFIG = dict(
    num=3558, title='给边赋权值的方案数 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 求最大深度 + 2^(k-1)',
    tags=['自底向上 DFS', '组合计数', '难度分 1845'],
    code='''
class Solution:
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        MOD = 1_000_000_007
        n = len(edges) + 1
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def dfs(x: int, fa: int) -> int:
            d = 0
            for y in g[x]:
                if y != fa:  # 不递归到父节点
                    d = max(d, dfs(y, x) + 1)
            return d

        k = dfs(1, 0)
        return pow(2, k - 1, MOD)
''',
    call=f'Solution().assignEdgeWeights({_EDGES})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=170),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=['x', 'fa', 'd', ('k', 'k', 'green')],
    skip=['MOD = ', 'n = len', 'g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'def dfs'],
    captions={
        'd = 0': '`dfs({x}, {fa})`：先假设 `x` 往下走不动，深度 `d = 0`',
        'for y in g[x]': lambda S, B, r: _for_cap(S['_inner'], B['_inner']),
        'if y != fa': lambda S, B, r: (f'`{S.y} != {S.fa}` → 是孩子，递归下去' if S.y != S.fa else f'`{S.y}` 就是父节点 `{S.fa}`，不能走回头路 → 跳过'),
        'd = max': '先递归求孩子 `{B.y}` 的子树深度：`dfs({B.y}, {B.x})`，回来后 `+1` 把边 `{B.x}→{B.y}` 算上',
        'return d': '`x = {x}` 往下最多 `{ret}` 条边，返回给父节点',
        'k = dfs': '最深节点离根 `k = {k}` 条边（只看这条路径，其余边随便）',
        'return pow': '边权只能是 1 或 2：和为奇数 ⇔ 有奇数个 1。`k` 个位置选奇数个，一共 `2^(k−1)` = `2^{k - 1}` = =={ret}==',
    },
    cards=dict(
        one_liner='只看根到最深节点那条路径：k 条边里选奇数个设成 1，共 2^(k-1) 种',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树根为 1，每条边权重设为 `1` 或 `2`',
                 '任选一个最深的节点 `x`，求根到 `x` 路径边权和为==奇数==的赋值方案数',
                 '其余不在路径上的边忽略；示例：`edges=[[1,2],[1,3],[3,4],[3,5],[4,6]]` → `4`'],
        quote='设从 1 到 x 的路径中有 k 条边。由于边权只能是 1 或 2，必须有奇数个 1，才能使边权之和是奇数。定理：从 k 个不同元素中，选奇数个数，有 2^(k-1) 种选法。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先求 `k`：最深节点离根多少条边，就是树的最大深度（前置题 104）',
              '2 不改变奇偶，所以和为奇数 ⇔ ==1 的个数为奇数==',
              '`k` 个位置选奇数个，方案数 `2^(k-1)`；用 `pow(2, k-1, MOD)` 取模'],
        summary=['时间 `O(n)`，空间 `O(n)`（建图 + 递归栈）',
                 '`dfs(y, x)` 要传父节点 `fa`，否则无向图会走回头路',
                 '`k` 是边数而不是节点数；`pow(2, k-1, MOD)` 内置取模幂',
                 '`n` 最大 `10^5`，Python 递归深度可能不够；这里只演示小树'],
    ),
)
