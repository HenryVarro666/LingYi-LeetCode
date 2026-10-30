import math as _m


def _tgraph(cv, T, box, pos, edges, ncol, nsub, ecol, title, R=30, bottom=62, side=None):
    """通用树/图：pos 为 0..1 的相对坐标；nsub 返回 str 或 [str]（画在节点下方）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 52 + R + (50 if 'a' in (side or {}).values() else 0), y1 - R - bottom
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v in edges:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is None:
            continue
        sd = (side or {}).get(u, 'b')
        for k, line in enumerate([s] if isinstance(s, str) else s):
            if sd == 'b':
                cv.text((px, py + R + 4 + k * 23), line, 20, T['yellow'], anchor='mt', bold=True, mono=True)
            elif sd == 'a':
                cv.text((px, py - R - 4 - (len(s) - 1 - k) * 23 if not isinstance(s, str) else py - R - 4), line, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            elif sd == 'r':
                cv.text((px + R + 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='lm', bold=True, mono=True)
            else:
                cv.text((px - R - 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='rm', bold=True, mono=True)
N = 6
EDGES = [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)]
SIDE = {0: 'a', 2: 'r'}
POS = {0: (0.5, 0.0), 1: (0.2, 0.45), 2: (0.7, 0.45), 3: (0.42, 1.0), 4: (0.7, 1.0), 5: (0.98, 1.0)}


def _phase(S):
    inn = S['_inner']
    if 'depth' in inn:
        return 'dfs'
    if 'x' in inn:
        return 'reroot'
    return None


def _draw(cv, S, B, box, T):
    ph = _phase(S)
    inn = S['_inner']
    ans, size = S.get('ans'), S.get('size')
    x = inn.get('x') if ph else None
    y = inn.get('y') if ph == 'reroot' else None

    def ncol(u):
        if ans is None or ph is None:
            return T['panel2']
        if u == x:
            return T['blue']
        if u == y and ph == 'reroot':
            return T['yellow']
        if ph == 'reroot' and ans[u] != 0:
            return T['green']
        return T['panel2']

    def nsub(u):
        if size is None:
            return None
        s = [f'size={size[u]}']
        if ans[u] != 0 or (u == 0 and ph == 'dfs'):
            s.append(f'ans={ans[u]}')
        return s

    def ecol(u, v):
        if ph == 'reroot' and x is not None and y is not None and {u, v} == {x, y}:
            return T['yellow'], 6
        if ph == 'dfs' and inn.get('fa', -1) >= 0 and {u, v} == {x, inn['fa']}:
            return T['blue'], 6
        return T['border'], 3

    _tgraph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
            side=SIDE, title='树（蓝 = 当前 x，黄 = 正在换到的儿子 y，绿 = ans 已确定）')


def _txt(S):
    ph = _phase(S)
    inn = S['_inner']
    ans, size, n = S.get('ans'), S.get('size'), S.get('n')
    if ph == 'dfs':
        return f"`ans[0]` 累加每个点到 0 的距离：节点 `{inn['x']}` 深度 `{inn['depth']}` → 目前 `ans[0] = {ans[0]}`"
    if ph == 'reroot':
        x, y = inn['x'], inn.get('y')
        if y is not None and ans[y] != 0 and y != 0:
            return (f"`ans[{y}] = ans[{x}] + {n} − 2×size[{y}] = {ans[x]} + {n} − {2 * size[y]}` = =={ans[y]}==")
        return f'换根：已知 `ans[{x}] = {ans[x]}`，推它的儿子'
    return '第一次 DFS 求 `ans[0]` 和 `size`；第二次 DFS 换根求其余'


CONFIG = dict(
    num=834, title='树中距离之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='换根 DP',
    tags=['灵神题单·动态规划', '难度分 2197'],
    code='''
class Solution:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]  # g[x] 表示 x 的所有邻居
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        ans = [0] * n
        size = [1] * n  # 注意这里初始化成 1 了，下面只需要累加儿子的子树大小
        def dfs(x: int, fa: int, depth: int) -> None:
            ans[0] += depth  # depth 为 0 到 x 的距离
            for y in g[x]:  # 遍历 x 的邻居 y
                if y != fa:  # 避免访问父节点
                    dfs(y, x, depth + 1)  # x 是 y 的父节点
                    size[x] += size[y]  # 累加 x 的儿子 y 的子树大小
        dfs(0, -1, 0)  # 0 没有父节点

        def reroot(x: int, fa: int) -> None:
            for y in g[x]:  # 遍历 x 的邻居 y
                if y != fa:  # 避免访问父节点
                    ans[y] = ans[x] + n - 2 * size[y]
                    reroot(y, x)  # x 是 y 的父节点
        reroot(0, -1)  # 0 没有父节点
        return ans
''',
    call='Solution().sumOfDistancesInTree(6, [[0,1],[0,2],[2,3],[2,4],[2,5]])',
    expect=[8, 12, 6, 10, 10, 10],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='calls', h=170),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('depth', lambda S: S['_inner'].get('depth'), 'cyan'),
           ('ans', 'ans', 'green'), ('size', 'size', 'yellow')],
    skip=['g[x].append(y)', 'g[y].append(x)', 'for x, y in edges', 'if y != fa', 'for y in g[x]'],
    max_steps=80,
    captions={
        'g = [[]': '先建邻接表 `g`：`g[x]` 是 x 的所有邻居',
        'ans = [0]': '`ans[i]` 是答案；这一步先只求 `ans[0]`',
        'size = [1]': '`size[x]` = 以 x 为根的子树大小，先记成 1（只有自己）',
        'ans[0] += depth': '节点 `{x}` 到 0 的距离是 `depth = {depth}` → `ans[0]` += {depth} = =={ans[0]}==',
        'dfs(y, x, depth + 1)': '往下走到儿子 `{B.y}`：父亲是 `{B.x}`，深度 `{B.depth + 1}`',
        'size[x] += size[y]': '儿子 `{y}` 的子树 `{size[y]}` 个点都算进 `{x}`：`size[{x}] = {size[x]}`',
        'dfs(0, -1, 0)': '从 0 出发：`0` 没有父节点，传 `-1`',
        'ans[y] = ans[x]': ('换根 `{x} → {y}`：`size[{y}] = {size[y]}` 个点离 y 近了 1，其余 `{n - size[y]}` 个点远了 1\n'
                            '`ans[{y}] = ans[{x}] + {n} − 2×{size[y]}` = =={ans[y]}=='),
        'reroot(y, x)': '`{B.y}` 的答案有了，继续往下换根：以它为 x，推它的儿子',
        'reroot(0, -1)': '`ans[0]` 已知，从 0 开始换根，把答案传给所有儿子',
        'return ans': '每个点的答案都算出来了：`{ans}`',
    },
    cards=dict(
        one_liner='先算一个根的答案，再用「变化量」把答案传给邻居',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树有 `n` 个点、`n-1` 条边，求每个点到其余所有点的距离之和',
                 '`answer[i]` 就是第 `i` 个点的距离和',
                 '示例：`n=6, edges=[[0,1],[0,2],[2,3],[2,4],[2,5]]`',
                 '→ `[8,12,6,10,10,10]`'],
        quote='从「以 0 为根」换到「以 2 为根」时，==唯一改变的是 0 和 2 的父子关系==。由此可见，一对节点的距离的「变化量」应该是很小的。',
        quote_src='—— 灵茶山艾府题解「答疑」',
        idea=['暴力：每个点当根各 DFS 一次，`O(n^2)` 会超时',
              '第一次 DFS：以 0 为根，累加深度得 `ans[0]`，同时算每棵子树大小 `size`',
              '换根 `x → y`：y 子树里 `size[y]` 个点近 1，其余 `n-size[y]` 个点远 1',
              '所以 `ans[y] = ans[x] + n - 2*size[y]`'],
        summary=['两次 DFS，每次每个点恰好访问一次：时间 `O(n)`',
                 '`size` 初始化成 1，DFS 里只需累加儿子的 size',
                 '无向树要传 `fa`，避免走回父节点；顺序是==先 dfs 再 reroot==',
                 '思考题：改成距离的平方和，还要多维护子树内的深度和'],
    ),
)
