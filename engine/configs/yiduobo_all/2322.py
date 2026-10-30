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
    left, right, xo = S.get('left'), S.get('right'), S.get('f')
    sub = ''
    if left and left[u] > 0:
        sub = f'^{xo[u]}  [{left[u]},{right[u]}]' if right[u] > 0 else f'[{left[u]},…]'
    if 'res' in I and 'x' in I and 'y' in I:
        c = _comp(u, I['x'], I['y'])
        return ('green' if c == 'root' else 'pink' if c == I['x'] else 'cyan'), str(u), sub
    if I.get('now') == u:
        return 'yellow', str(u), sub
    return 'panel2', str(u), sub


def _draw(cv, S, B, box, T):
    I = S['_inner']
    pair = 'res' in I and 'x' in I and 'y' in I
    edges = []
    for a, ks in CH.items():
        for b in ks:
            cut = pair and b in (I['x'], I['y'])
            edges.append((a, b, 'red' if cut else None, bool(cut)))
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='树（右侧：^子树异或 f  [left, right]）' + ('；红虚线 = 断开的边，三色 = 三块' if pair else ''))


def _abc(S):
    I = S['_inner']
    if 'res' in I and 'part3' in I and S['_line'] >= LN_P3:
        p = (I['part1'], I['part2'], I['part3'])
        return f"三块异或：`{p[0]}`、`{p[1]}`、`{p[2]}` → 最大 − 最小 = =={max(p) - min(p)}=="
    if 'res' in I and 'x' in I and 'y' in I:
        return f"删以 `{I['x']}`、`{I['y']}` 为根的两棵新子树与原树的连接边" + ('' if I['res'] is None else f"，当前最小分数 `res = {I['res']}`")
    return ''


CODE = '''
class Solution(object):
    def minimumScore(self, nums, edges):

        n = len(nums)
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        used = set([0])
        f = nums[:]
        left = [0] * n
        right = [0] * n

        self.timestamp = 0
        def dfs(now):
            self.timestamp += 1
            left[now] = self.timestamp

            for next in g.get(now, set()):
                if next not in used:
                    used.add(next)
                    dfs(next)
                    f[now] ^= f[next]
            
            self.timestamp += 1
            right[now] = self.timestamp

        dfs(0)
        
        res = None
        for x in range(1, n - 1):
            for y in range(x + 1, n):
                if left[x] < left[y]:
                    if left[y] < right[x]:
                        part1 = f[y]
                        part2 = f[x] ^ f[y]
                        part3 = f[0] ^ f[x]
                    else:
                        part1 = f[x]
                        part2 = f[y]
                        part3 = f[0] ^ f[x] ^ f[y]
                elif left[x] < right[y]:
                    part1 = f[x]
                    part2 = f[x] ^ f[y]
                    part3 = f[0] ^ f[y]
                else:
                    part1 = f[x]
                    part2 = f[y]
                    part3 = f[0] ^ f[x] ^ f[y]

                diff = max(part1, part2, part3) - min(part1, part2, part3)
                if res is None or res > diff:
                    res = diff
        
        return res
'''
_L = CODE.lstrip('\n').split('\n')
LN_P3 = next(i for i, l in enumerate(_L, 1) if 'part3 =' in l)
_LN = {l.strip(): i for i, l in reversed(list(enumerate(_L, 1)))}
_P3 = [i for i, l in enumerate(_L, 1) if 'part3 =' in l]   # 三个分支各一行：x 在上 / 互不相交 / y 在上
_TS = [i for i, l in enumerate(_L, 1) if 'self.timestamp += 1' in l]


CONFIG = dict(
    num=2322, title='从树中删除边的最小分数', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='枚举两棵新子树的根 · dfs 序判断包含',
    tags=['灵神题单', '链表树与回溯', '难度分 2392'],
    code=CODE,
    call='Solution().minimumScore([1,5,5,4,11], [[0,2],[2,1],[2,4],[1,3]])',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='f', label='f（子树异或值；一开始是 nums，回溯时逐步异或进孩子）', cell=60, h=110),
        dict(type='calls', h=90),
        dict(type='text', fn=_abc),
    ],
    watch=[('now', "now if 'now' in _inner else '–'", 'yellow'), ('x', "x if 'res' in _inner and 'x' in _inner else '–'", 'pink'),
           ('y', "y if 'res' in _inner and 'y' in _inner else '–'", 'cyan'), ('res', "res if 'res' in _inner else '–'", 'green')],
    skip=[_TS[0], _TS[1], 'for x, y in edges', 'if x not in g', 'g[x] = set()', 'if y not in g', 'g[y] = set()', 'g[x].add(y)', 'g[y].add(x)', 'n = len(nums)', 'g = {}',
          'used = set', 'f = nums[:]', 'left = [0]', 'right = [0]', 'self.timestamp = 0', 'for next in g.get', 'if next not in used', 'used.add(next)',
          'for x in range(1, n - 1)', 'for y in range(x + 1, n)', 'part1 = ', 'part2 = ', 'if res is None or res > diff', 'res = None'],
    max_steps=100,
    captions={
        _TS[0] + 1: '进入 `{now}`：时间戳加一，`left[{now}] = {self.timestamp}`（dfs 序里==第一次==出现的位置）',
        _TS[1] + 1: '离开 `{now}`：时间戳再加一，`right[{now}] = {self.timestamp}`（==最后一次==出现的位置）',
        'dfs(next)': '往孩子 `{next}` 走：先把它整棵子树的异或值 `f[{next}]` 算好',
        'f[now] ^= f[next]': '孩子 `{next}` 的子树异或 `{f[next]}` 并进来：`f[{now}] = {f[now]}`',
        'dfs(0)': '从 0 出发：同时算出子树异或值 `f` 和 dfs 序区间 `[left, right]`',
        'if left[x] < left[y]:': lambda S, B, r: (f'枚举新子树的根 `x = {S.x}`、`y = {S.y}`（删它们与父亲的边）。`left[{S.x}] = {S.left[S.x]}` ' + ('<' if S.left[S.x] < S.left[S.y] else '>') + f' `left[{S.y}] = {S.left[S.y]}`：' + ('`x` 先进入，可能 `y` 在 `x` 子树里' if S.left[S.x] < S.left[S.y] else '`y` 先进入，可能 `x` 在 `y` 子树里')),
        'if left[y] < right[x]:': lambda S, B, r: (f'`left[{S.y}] = {S.left[S.y]}` 在 `x = {S.x}` 的区间 `({S.left[S.x]}, {S.right[S.x]})` 内 → ==' + ('`y` 在 `x` 的子树里' if S.left[S.y] < S.right[S.x] else '不在，两棵子树互不相交') + '=='),
        'elif left[x] < right[y]:': lambda S, B, r: (f'`left[{S.x}] = {S.left[S.x]}` 在 `y = {S.y}` 的区间 `({S.left[S.y]}, {S.right[S.y]})` 内 → ==' + ('`x` 在 `y` 的子树里' if S.left[S.x] < S.right[S.y] else '不在，两棵子树互不相交') + '=='),
        _P3[0]: '情况 1（`y` 在 `x` 子树里）：`y` 子树不变 `{part1}`；`x` 子树去掉 `y` 子树 `{part2}`；剩下 `f[0]^f[x]` = `{part3}`',
        _P3[1]: '情况 3（互不相交）：`x` 子树 `{part1}`、`y` 子树 `{part2}` 都不变；剩下 `f[0]^f[x]^f[y]` = `{part3}`',
        _P3[2]: '情况 2（`x` 在 `y` 子树里）：`x` 子树不变 `{part1}`；`y` 子树去掉 `x` 子树 `{part2}`；剩下 `f[0]^f[y]` = `{part3}`',
        'diff = max': '分数 = 最大 `{max(part1, part2, part3)}` − 最小 `{min(part1, part2, part3)}` = `{diff}`；和当前最小 `{res}` 比，更小才替换',
        'res = diff': '分数 `{diff}` 更小 → `res = {res}`',
        'return res': '所有 `(x, y)` 都试过，最小分数 `{res}`',
    },
    cards=dict(
        one_liner='不枚举边，枚举新长出的两棵子树的根，dfs 序判断包含',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['无向树，点权 `nums`，删掉==两条边==得到三个连通块',
                 '每块算异或，分数 = 最大 − 最小，求最小分数',
                 '本视频：`nums=[1,5,5,4,11]`，边 `[[0,2],[2,1],[2,4],[1,3]]` → `10`'],
        quote='枚举删除的两条边需要对两条边是否具有公共节点进行特殊判断，相对比较麻烦，不妨直接枚举最终新多出来的两棵树的根节点再计算分数。',
        quote_src='—— yiduobo 题解原文',
        idea=['删两条边 = 多出两棵新子树，根设为 `x`、`y`：枚举这对点',
              '三种位置：`y` 在 `x` 里、`x` 在 `y` 里、互不相交，各有一套三块异或的算法',
              '判断包含：dfs 序里每个点进出各记一次，`left[x] < left[y] < right[x]` 说明 `y` 在 `x` 里'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错点：包含了 `x` 的那块要==去掉 `y` 子树==，所以是 `f[x] ^ f[y]`',
                 '易错点：dfs 序里进、出==各占一个时间戳==，判断用 `<` 即可',
                 '原文是 Python 2 风格 `class Solution(object)`，在 Python 3 中可直接运行，未改动',
                 '对比灵神：灵神枚举「删哪个点和父亲的边」，时间戳每个点只记进入/离开时的 `clock`；yiduobo 进出各加一'],
    ),
)
