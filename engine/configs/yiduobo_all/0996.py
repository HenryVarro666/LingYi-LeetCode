A0 = [1, 8, 1]
N = len(A0)
POS = [(0.2, 0.6), (0.5, 0.2), (0.8, 0.6)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图：和为完全平方数的下标连边（蓝 = 当前点 x，粉 = 要扩展到的 next）', 22, T['muted'], bold=True)
    g = S.get('g') or {}
    w, h = x1 - x0, y1 - y0 - 50
    pts = [(x0 + px * w, y0 + 60 + py * h) for px, py in POS]
    line = S.get('_line', 0)
    x, nx = S.get('x'), S.get('next')
    in_bfs = line >= 24 and x is not None
    for i in range(N):
        for j in g.get(i, ()):
            if i < j:
                hot = in_bfs and nx is not None and {i, j} == {x, nx} and line >= 25
                cv.line([pts[i], pts[j]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    state = S.get('state') if in_bfs else None
    for i, (px, py) in enumerate(pts):
        used = state is not None and state >> i & 1
        fill = T['panel2']
        if in_bfs and i == x:
            fill = T['blue']
        elif in_bfs and nx is not None and i == nx and line >= 25:
            fill = T['pink']
        elif used:
            fill = T['green']
        r = 44
        cv.rect((px - r, py - r, px + r, py + r), fill=fill, r=r, outline=T['border'])
        light = fill != T['panel2']
        cv.text((px, py - 6), A0[i], 34, T['bg'] if light else T['text'], anchor='mm', bold=True)
        cv.text((px, py + r + 14), f'下标 {i}', 18, T['dim'], anchor='mt')


def _formula(S):
    line = S.get('_line', 0)
    if line >= 24 and S.get('x') is not None and S.get('state') is not None and line <= 31:
        st = S['state']
        return f'当前 `state = {st:0{N}b}`（绿 = 已经走过的点），路径终点 `x = {S["x"]}`'
    if line >= 38:
        return f'`res = {S.get("res")}`：按下标排列数，相同数字互换被算成不同排列'
    return '`f[state][x]` = 走过 `state` 里的点、终点是 `x` 的合法路径数'


CONFIG = dict(
    num=996, title='平方数组的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='汉密尔顿路径计数（状压 BFS）+ 去重',
    tags=['灵神题单·动态规划'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def numSquarefulPerms(self, A):

        g = {}

        n = len(A)
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i == j:
                    continue
                if int(sqrt(A[i] + A[j])) ** 2 == A[i] + A[j]:
                    g[i].add(j)

        f = [[0] * n for _ in range(1 << n)]
        q = []
        for i in range(n):
            q.append([1 << i, i])
            f[1 << i][i] = 1

        l, r = 0, len(q)
        while l < r:
            for state, x in q[l : r]:
                for next in g[x]:
                    if state & (1 << next) == 0:
                        next_state = state | (1 << next)
                        if f[next_state][next] == 0:
                            q.append([next_state, next])
                        f[next_state][next] += f[state][x]

            l, r = r, len(q)

        res = sum(f[(1 << n) - 1])
        cnt_dict = {}
        for num in A:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1

        for cnt in cnt_dict.values():
            for i in range(cnt, 1, -1):
                res //= i

        return res
''',
    call=f'Solution().numSquarefulPerms({A0})',
    expect=1,
    skip=['g = {}', 'n = len(A)', 'g[i] = set()', 'for j in range(n)', 'continue', 'f = [[0] * n', 'q = []', 'for i in range(n)', 'cnt_dict = {}',
          'for num in A', 'cnt_dict[num]', 'for next in g[x]', 'for state, x in', 'l, r = r', 'l, r = 0', 'if i == j', 'for i in range(cnt', 'for cnt in'],
    max_steps=64,
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='table', var='f', label='f[state][x]：state（二进制）× 终点 x', h=300, cell=56,
             rows=lambda S: [f'{k:0{N}b}' for k in range(2 ** N)], cols=lambda S: [f'{k}' for k in range(N)],
             color=lambda S, r, c, v: ('yellow' if S.get('_line', 0) in (24, 25, 26, 27, 28, 29) and S.get('state') is not None and S.get('next') is not None
                                       and (r, c) == (S['state'] | (1 << S['next']), S['next']) and S.get('_line', 0) >= 26 else None)),
    ],
    watch=[('state', 'state', 'yellow'), ('x', 'x', 'blue'), ('next', 'next', 'pink'), ('res', 'res', 'green')],
    captions={
        'if int(sqrt': lambda S, B, r: (f'`{S.A[S.i]} + {S.A[S.j]} = {S.A[S.i] + S.A[S.j]}` ' + ('是完全平方数 → 连边' if int((S.A[S.i] + S.A[S.j]) ** 0.5) ** 2 == S.A[S.i] + S.A[S.j] else '不是完全平方数 → 不连')),
        'g[i].add(j)': '下标 `{i}` 和 `{j}` 可以相邻放置，建边：`g[{i}] = {g[i]}`',
        'q.append([1 << i, i])': '初始状态：只选下标 `{i}`（`state = {(1 << i):0{n}b}`），当起点',
        'f[1 << i][i] = 1': '单个点的路径只有 1 条：`f[{(1 << i):0{n}b}][{i}] = 1`',
        'while l < r': lambda S, B, r: (f'按层 BFS：这一层有 `{S.r - S.l}` 个状态要扩展' if S.l < S.r else '队列空了，所有状态都扩展完'),
        'if state & (1 << next) == 0': lambda S, B, r: (f'`next = {S.next}` 没在 `state = {S.state:0{S.n}b}` 里 → 可以走过去' if S.state >> S.next & 1 == 0
                                                        else f'`next = {S.next}` 已经走过了，跳过'),
        'next_state = state': '新状态 `{next_state:0{n}b}`：把点 `{next}` 加进路径，终点变成 `{next}`',
        'if f[next_state][next] == 0': lambda S, B, r: ('这个状态第一次出现 → 加入队列' if S.f[S.next_state][S.next] == 0 else '这个状态已经在队列里，只累加方案数'),
        'q.append([next_state, next])': '新状态入队，下一层再从它继续扩展',
        'f[next_state][next] += f[state][x]': '`f[{next_state:0{n}b}][{next}] += f[{state:0{n}b}][{x}]` → =={f[next_state][next]}==',
        'res = sum(f': '全集那一行求和：`res = sum(f[{(1 << n) - 1:0{n}b}])` = =={res}==（按下标算的排列数）',
        'res //= i': '去重：数字出现 `{cnt}` 次，除以 `{cnt}!`：这一步 `res //= {i}` → =={res}==',
        'return res': '去重后的答案 = =={ret}==',
    },
    cards=dict(
        one_liner='建边后数汉密尔顿路径，再除以重复数阶乘',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(n · 2^n)`',
        problem=['相邻两数之和都是==完全平方数==的数组叫平方数组',
                 '给定 `A`，返回其中有多少种不同的排列是平方数组',
                 '示例：`[1,17,8]` → `2`；本视频用 `[1,8,1]` 演示去重'],
        quote='将每个数视为无向图中的一个点，那么对于 A[i] 和 A[j]，若二者之和为完全平方数，那么二者是可以相邻放置的，于是在图中建立一条连接 i 和 j 的边。那么现在问题就又变成了图中存在多少条汉密尔顿路径。',
        quote_src='—— yiduobo 题解',
        idea=['先建图：和是完全平方数的两个下标连边',
              '`f[state][x]`：用了 `state` 里的点、最后一个是 `x` 的方案数；按层 BFS，往后==扩展 next==',
              '`res = sum(f[全集])`；相同数字可互换，每种数出现 `k` 次就除以 `k!`'],
        summary=['时间 `O(n^2 2^n)`；建图 `O(n^2)`',
                 '原文为 Python 2 写法，去重处的 `res /= i` 已改为 `res //= i`（整数除法）；`sqrt` 来自 `math`',
                 '易错：重复数字要除 `k!`，先全部枚举完再除，保证整除',
                 '这里是==往后推==（从旧状态扩展到新状态），灵神是往前看的 `dfs`/递推'],
    ),
)
