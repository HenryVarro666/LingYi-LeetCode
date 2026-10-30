import math as _m


def _layout(edges, n):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    pos, depth, nxt = {}, {}, [0]

    def go(x, fa, d):
        kids = [y for y in g[x] if y != fa]
        if not kids:
            pos[x] = nxt[0]
            nxt[0] += 1
        else:
            for y in kids:
                go(y, x, d + 1)
            pos[x] = sum(pos[y] for y in kids) / len(kids)
        depth[x] = d

    go(0, -1, 0)
    return pos, depth, max(depth.values()), max(nxt[0] - 1, 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    edges, price = S['edges'], S['price']
    n = len(price)
    pos, depth, md, mw = _layout(edges, n)
    cv.text((x0 + 18, y0 + 4), '树（以 0 为根 DFS）：黄 = 当前 x，绿 = 刚算完的儿子 y，蓝 = 父节点 fa', 22, T['muted'], bold=True)
    R = 34
    w, h = x1 - x0 - 2 * R - 80, y1 - y0 - 2 * R - 90
    P = {i: (x0 + 40 + R + pos[i] / mw * w, y0 + 56 + R + depth[i] / max(md, 1) * h) for i in range(n)}
    for a, b in edges:
        cv.line([P[a], P[b]], T['dim'], 4)
    cur, fa, ch = S.get('x'), S.get('fa'), S.get('y')
    if 'ans' not in S or cur is None:
        cur = fa = ch = None
    for i in range(n):
        cx, cy = P[i]
        c = None
        if i == cur:
            c = 'yellow'
        elif i == ch:
            c = 'green'
        elif i == fa:
            c = 'blue'
        fill = T[c] if c else T['panel2']
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=fill, outline=T['border'], width=3)
        cv.text((cx, cy - 10), i, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + 14), f'价{price[i]}', 20, T['bg'] if c else T['muted'], anchor='mm', bold=True)


def _info(S):
    if 'max_s1' not in S or 'x' not in S:
        return ''
    return (f"节点 `{S['x']}`：带叶子最大 `max_s1 = {S['max_s1']}`，不带叶子最大 `max_s2 = {S['max_s2'] if 'max_s2' in S else 0}`，"
            f"全局 `ans = {S['ans']}`")


CONFIG = dict(
    num=2538, title='最大价值和与最小价值和的差值', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 带叶子 / 不带叶子的最大路径和',
    tags=['动态规划', '链表树与回溯', '难度分 2398'],
    code='''
class Solution:
    def maxOutput(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建树

        ans = 0
        def dfs(x: int, fa: int) -> (int, int):
            nonlocal ans
            max_s1 = p = price[x]
            max_s2 = 0
            for y in g[x]:
                if y == fa: continue
                s1, s2 = dfs(y, x)
                # 前面最大带叶子的路径和 + 当前不带叶子的路径和
                # 前面最大不带叶子的路径和 + 当前带叶子的路径和
                ans = max(ans, max_s1 + s2, max_s2 + s1)
                max_s1 = max(max_s1, s1 + p)
                max_s2 = max(max_s2, s2 + p)  # 这里加上 p 是因为 x 必然不是叶子
            return max_s1, max_s2
        dfs(0, -1)
        return ans
''',
    call='Solution().maxOutput(6, [[0,1],[1,2],[1,3],[3,4],[3,5]], [9,8,7,6,10,5])',
    expect=24,
    skip=['g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'nonlocal ans', 'ans = 0', 'def dfs'],
    max_steps=80,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_info, h=60, size=24),
        dict(type='calls', h=200),
    ],
    watch=[('x', 'x', 'yellow'), ('max_s1', 'max_s1', 'blue'), ('max_s2', 'max_s2', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'max_s1 = p = price[x]': '先只算 `x` 自己：带叶子路径 `max_s1 = {max_s1}`（单点，x 若是叶子就是它）',
        'max_s2 = 0': '不带叶子的路径：还没往下走，是空路径 `max_s2 = 0`',
        'for y in g[x]': lambda S, B, r: ((f'`x={S.x}` 的下一个邻居 `y = {S.y}`' if S.y != B._inner.get('y') else f'`x={S.x}` 的邻居都处理完了 → 返回')
                                           if 'y' in S else '枚举 `x` 的邻居'),
        'if y == fa': lambda S, B, r: (f'`y = {S.y}` 是父节点 → 不往回走' if S.y == S.fa else f'`y = {S.y}` 是儿子 → 递归'),
        's1, s2 = dfs': '儿子 `{y}` 返回：带叶子 `s1 = {s1}`，不带叶子 `s2 = {s2}`',
        'ans = max': '两条往下的路径在 `x` 拼起来：`max({max_s1}+{s2}, {max_s2}+{s1})`，一条带叶子、一条去掉叶子 → `ans = {ans}`',
        'max_s1 = max(max_s1, s1': '儿子的带叶子路径接上 `x`（价 {p}）：`max_s1 = {max_s1}`',
        'max_s2 = max(max_s2': '不带叶子的也接上 `x`：`max_s2 = {max_s2}`（x 一定不是叶子，所以要加 p）',
        'return max_s1, max_s2': '把 `({max_s1}, {max_s2})` 交给父节点去拼接',
        'dfs(0, -1)': '从 0 开始 DFS，父节点填 -1',
        'return ans': '最大开销 `{ans}`',
    },
    cards=dict(
        one_liner='价值都为正：最小路径是单点，最大路径延伸到叶子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无根树，每个点有价值 `price`，选一个根，求「以根出发的最大路径和 − 最小路径和」',
                 '要在所有根里取最大的开销',
                 '示例：`n=6`，`price=[9,8,7,6,10,5]` → `24`'],
        quote='由于价值都是正数，因此价值和最小的一条路径一定==只有一个点==。……问题转换成==去掉一个叶子==后的最大路径和。',
        quote_src='—— 灵茶山艾府题解 提示 1、3',
        idea=['最小路径是根自己，所以开销 = 最长路径和 − 一个端点（叶子）的价值',
              '类似树的直径：DFS 时同时维护「带叶子」`max_s1` 和「不带叶子」`max_s2`',
              '新儿子的 s1 + 之前的 max_s2、或 s2 + 之前的 max_s1，两条路径不重叠，拼起来更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈 + 邻接表）',
                 '==max_s2 加 p 是因为 x 必然不是叶子==',
                 '这里的叶子指度为 1 的点，根也可能是叶子',
                 '同类题：543 二叉树的直径、124 最大路径和、2246'],
    ),
)
