def _tree_pos(ch, root=0):
    """一般树自动布局：叶子按顺序排开，父亲在孩子中间。返回 {节点: (x 0~1, 深度)}"""
    pos, cnt = {}, [0]
    leaves = sum(1 for _ in _leaves(ch, root))
    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = ((cnt[0] + 0.5) / leaves, d); cnt[0] += 1
        else:
            for k in kids:
                go(k, d + 1)
            pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)
    go(root, 0)
    return pos


def _leaves(ch, u):
    kids = ch.get(u, [])
    if not kids:
        yield u
    for k in kids:
        yield from _leaves(ch, k)


def _gt_draw(cv, S, B, box, T, ch, pos, edges, node_fn, extra=None, title=''):
    """edges: [(父,子,颜色名或None,虚线)]；node_fn(S,u)->(填充色, 主文字, 副文字)"""
    x0, y0, x1, y1 = box
    maxd = max(d for _, d in pos.values())
    W, H = x1 - x0 - 300, y1 - y0 - 110
    P = {u: (x0 + 110 + px * W, y0 + 70 + (d / max(maxd, 1)) * H) for u, (px, d) in pos.items()}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for a, b, col, dash in edges:
        pa, pb = P[a], P[b]
        if dash == 'arc':  # 从孩子 b 绕一道弧线指向 a（向左侧鼓出）
            cx, cy = min(pa[0], pb[0]) - 110, (pa[1] + pb[1]) / 2
            pts = [((1 - t) ** 2 * pb[0] + 2 * (1 - t) * t * cx + t * t * pa[0],
                    (1 - t) ** 2 * pb[1] + 2 * (1 - t) * t * cy + t * t * pa[1]) for t in [0.12 + 0.76 * i / 30 for i in range(31)]]
            cv.line(pts, T[col], 5)
            cv.arrow(pts[-3], pts[-1], T[col], 5, 16)
        elif dash:
            cv.dashed(pb, pa, T[col], 4)
        else:
            cv.line([pa, pb], T[col] if col else T['border'], 4 if col else 3)
    R = 24
    for u, (X, Y) in P.items():
        fill, main, sub = node_fn(S, u)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[fill] if isinstance(fill, str) else fill, outline=T['border'], r=R, width=2)
        cv.text((X, Y), main, 24, T['text'] if fill == 'panel2' else T['bg'], anchor='mm', bold=True, mono=True)
        if sub:
            cv.text((X + R + 8, Y), sub, 20, T['text'], anchor='lm', bold=True)
    if extra:
        extra(cv, P, T)
    return P
NUMS = [1, 5, 5, 4, 11]
EDGES2 = [[0, 2], [2, 1], [2, 4], [1, 3]]
CH = {0: [2], 2: [1, 4], 1: [3]}
PARENT = {c: p for p, ks in CH.items() for c in ks}
POS = _tree_pos(CH)


def _up(u):
    r = [u]
    while r[-1] in PARENT:
        r.append(PARENT[r[-1]])
    return r  # u, 父, ..., 根


def _depth(u):
    return len(_up(u)) - 1


def _comp(u, x, y):
    cuts = [c for c in (x, y) if c in _up(u)]
    if not cuts:
        return 'root'
    return max(cuts, key=_depth)


def _node(S, u):
    I = S['_inner']
    in_, out, xo = S.get('in_'), S.get('out'), S.get('xor')
    sub = ''
    if in_ and in_[u] > 0:
        sub = f'^{xo[u]}  [{in_[u]},{out[u]}]' if out[u] > 0 else f'[{in_[u]},…]'
    if 'ans' in I and 'x' in I and 'y' in I:
        c = _comp(u, I['x'], I['y'])
        return ('green' if c == 'root' else 'pink' if c == I['x'] else 'cyan'), str(u), sub
    if I.get('x') == u:
        return 'yellow', str(u), sub
    return 'panel2', str(u), sub


def _draw(cv, S, B, box, T):
    I = S['_inner']
    pair = 'ans' in I and 'x' in I and 'y' in I
    edges = []
    for a, ks in CH.items():
        for b in ks:
            cut = pair and b in (I['x'], I['y'])
            edges.append((a, b, 'red' if cut else None, bool(cut)))
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='树（节点右侧：^子树异或值  [in, out] 时间戳）' + ('；红虚线 = 删掉的两条边，三种颜色 = 三个连通块' if pair else ''))


def _abc(S):
    I = S['_inner']
    if 'ans' in I and 'a' in I and S['_line'] >= LN_A:
        return f"三块异或：`a = {I['a']}`，`b = {I['b']}`，`c = {I['c']}` → 最大 − 最小 = =={max(I['a'], I['b'], I['c']) - min(I['a'], I['b'], I['c'])}=="
    if 'ans' in I and 'x' in I and 'y' in I:
        return f"删 `{I['x']}` 与父亲的边、`{I['y']}` 与父亲的边：当前 `ans = {S['ans']}`" if S['ans'] != float('inf') else f"删 `{I['x']}` 与父亲的边、`{I['y']}` 与父亲的边"
    return ''


CODE = '''
class Solution:
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        xor, in_, out = [0] * n, [0] * n, [0] * n
        clock = 0
        def dfs(x: int, fa: int) -> None:
            nonlocal clock
            clock += 1
            in_[x] = clock  # 递
            xor[x] = nums[x]
            for y in g[x]:
                if y != fa:
                    dfs(y, x)
                    xor[x] ^= xor[y]
            out[x] = clock  # 归
        dfs(0, -1)

        # 判断 x 是否为 y 的祖先
        def is_ancestor(x: int, y: int) -> bool:
            return in_[x] < in_[y] <= out[x]

        ans = inf
        # 枚举：删除 x 与 x 父节点之间的边，删除 y 与 y 父节点之间的边
        for x in range(2, n):
            for y in range(1, x):
                if is_ancestor(x, y):  # x 是 y 的祖先
                    a, b, c = xor[y], xor[x] ^ xor[y], xor[0] ^ xor[x]
                elif is_ancestor(y, x):  # y 是 x 的祖先
                    a, b, c = xor[x], xor[x] ^ xor[y], xor[0] ^ xor[y]
                else:  # x 和 y 分别属于两棵不相交的子树
                    a, b, c = xor[x], xor[y], xor[0] ^ xor[x] ^ xor[y]
                ans = min(ans, max(a, b, c) - min(a, b, c))
                if ans == 0:  # 不可能变小
                    return 0  # 提前返回
        return ans
'''
_L = CODE.lstrip('\n').split('\n')
LN_A = next(i for i, l in enumerate(_L, 1) if 'a, b, c =' in l)

CONFIG = dict(
    num=2322, title='从树中删除边的最小分数', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 时间戳 · 枚举两条边分类讨论',
    tags=['灵神题单', '链表树与回溯', '难度分 2392'],
    code=CODE,
    call='Solution().minimumScore([1,5,5,4,11], [[0,2],[2,1],[2,4],[1,3]])',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='xor', label='xor（子树异或和）', cell=60, h=110),
        dict(type='calls', h=90, hide=()),
        dict(type='text', fn=_abc),
    ],
    watch=[('x', "x if 'x' in _inner else '–'", 'yellow'), ('y', "y if 'y' in _inner and 'ans' in _inner else '–'", 'cyan'), ('clock', "clock if 'clock' in _inner or 'ans' not in _inner else '–'", 'blue'), ('ans', "ans if 'ans' in _inner else '–'", 'green')],
    skip=['for x, y in edges', 'g[x].append', 'g[y].append', 'nonlocal clock', 'clock += 1', 'for x in range(2, n)', 'for y in range(1, x)', 'if ans == 0', 'return in_[x] < in_[y] <= out[x]', 'for y in g[x]', 'if y != fa', 'n = len(nums)', 'g = [[]', 'xor, in_, out =', 'clock = 0', 'xor[x] = nums[x]'],
    max_steps=100,
    captions={
        'in_[x] = clock': '进入 `{x}`（==递==）：`clock` 加一，`in_[{x}] = {clock}`',
        'xor[x] ^= xor[y]': '孩子 `{y}` 的子树异或和 `{xor[y]}` 并进来：`xor[{x}] = {xor[x]}`',
        'out[x] = clock': '离开 `{x}`（==归==）：`out[{x}] = {clock}`，子树里最大的时间戳就是它',
        'dfs(0, -1)': '以 `0` 为根 DFS：同时算出子树异或和 `xor` 和时间戳 `in_/out`',
        'if is_ancestor(x, y)': lambda S, B, r: f'枚举 `x = {S.x}`、`y = {S.y}`：删它们各自与父亲的边。`{S.x}` 是 `{S.y}` 的祖先吗？`in_[{S.x}] < in_[{S.y}] <= out[{S.x}]` 即 `{S.in_[S.x]} < {S.in_[S.y]} <= {S.out[S.x]}` → ==' + ('是' if S.in_[S.x] < S.in_[S.y] <= S.out[S.x] else '不是') + '==',
        'elif is_ancestor(y, x)': lambda S, B, r: f'反过来：`{B.y}` 是 `{B.x}` 的祖先吗？`in_[{B.y}] < in_[{B.x}] <= out[{B.y}]` 即 `{B.in_[B.y]} < {B.in_[B.x]} <= {B.out[B.y]}` → ==' + ('是' if B.in_[B.y] < B.in_[B.x] <= B.out[B.y] else '不是，两棵子树不相交') + '==',
        'dfs(y, x)': '递归孩子 `{y}`',
        'a, b, c = xor[y], xor[x] ^ xor[y], xor[0] ^ xor[x]': '情况 1（x 在上）：`y` 子树自成一块 `{a}`；`x` 子树去掉 `y` 子树 `{b}`；剩下的 `{c}`',
        'a, b, c = xor[x], xor[x] ^ xor[y], xor[0] ^ xor[y]': '情况 2（y 在上）：`x` 子树自成一块 `{a}`；`y` 子树去掉 `x` 子树 `{b}`；剩下的 `{c}`',
        'a, b, c = xor[x], xor[y], xor[0] ^ xor[x] ^ xor[y]': '情况 3（互不相交）：两棵子树各自 `{a}`、`{b}`；剩下的 `{c}`（总异或去掉两块）',
        'ans = min': '分数 = 最大 `{max(a, b, c)}` − 最小 `{min(a, b, c)}` = `{max(a, b, c) - min(a, b, c)}`，`ans = min({B.ans}, ·) = {ans}`；只要 `ans` 降到 0 就可提前返回',
        'return ans': '所有两条边的组合枚举完，最小分数 `{ans}`',
    },
    cards=dict(
        one_liner='用 DFS 时间戳判断两条边的位置关系，分三种情况算异或',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['无向树，点权 `nums`，删掉==两条不同的边==得到三个连通块',
                 '每块算点权异或，分数 = 最大异或 − 最小异或',
                 '求所有删法里的最小分数。本视频：`nums=[1,5,5,4,11]`，边 `[[0,2],[2,1],[2,4],[1,3]]` → `10`'],
        quote='对于时间戳区间，要么不相交，要么一个完全包含另一个。所以只要区间 A 有一个点在区间 B 内，那么区间 B 就包含区间 A。',
        quote_src='—— 灵茶山艾府题解',
        idea=['以 0 为根，`xor[x]` = 子树 x 的异或和；枚举删掉 `x`、`y` 各自与父亲的边（x、y 都不是 0）',
              '两条边的关系：==上下==（谁是谁的祖先）或==互不相交==，分别对应三种异或公式',
              '怎么判断祖先：递归时记下进入、离开的时间戳，`in_[x] < in_[y] <= out[x]` 就说明 x 是 y 的祖先'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错点：把「异或」当「减法」：子树异或和去掉一块，就是再异或那一块的值',
                 '易错点：枚举的是「点」（删它与父亲的边），所以 x、y 都从 1 起，不含根 0',
                 '`out[x]` 取的是离开时的 `clock`，所以判断用 `<= out[x]`，可以相等',
                 '最小分数是 0，所以 `ans == 0` 时可以提前返回'],
    ),
)
