N = 6
EDGES = [[1, 2], [1, 3], [2, 4], [3, 5], [3, 6]]
PRIMES = {2, 3, 5}
POS = {1: (0.5, 0.1), 2: (0.2, 0.5), 3: (0.75, 0.5), 4: (0.2, 0.92), 5: (0.58, 0.92), 6: (0.92, 0.92)}
SETUP = '''
from math import isqrt
# 标记 10**5 以内的质数
MX = 10 ** 5 + 1
is_prime = [True] * MX
is_prime[1] = False
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = False
'''


def is_prime_(v):
    return v in PRIMES


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（粉 = 质数，灰 = 非质数；绿框 = 已算出所在连通块大小，黄 = 正在 DFS）', 22, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 130
    P = {k: (x0 + 60 + v[0] * w, y0 + 75 + v[1] * h) for k, v in POS.items()}
    inn = S.get('_inner', {})
    indfs = 'fa' in inn
    size = S.get('size') or []
    nodes = S.get('nodes') or []
    center = S.get('x') if not indfs and 'ans' in S else None
    cur = inn.get('x') if indfs else None
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    for k, (px, py) in P.items():
        r = 30
        isp = k in PRIMES
        fill = T['pink'] if isp else T['panel2']
        tc = T['bg'] if isp else T['text']
        if k in nodes and not (k < len(size) and size[k] > 0):
            fill, tc = T['yellow'], T['bg']
        if k < len(size) and size[k] > 0 and not isp:
            cv.d.ellipse((px - r - 6, py - r - 6, px + r + 6, py + r + 6), outline=T['green'], width=4)
            cv.text((px, py + r + 12), '块大小 %d' % size[k], 20, T['green'], anchor='mt', bold=True)
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline=T['border'])
        if k == center:
            cv.d.ellipse((px - r - 12, py - r - 12, px + r + 12, py + r + 12), outline=T['blue'], width=5)
        if k == cur:
            cv.d.ellipse((px - r - 12, py - r - 12, px + r + 12, py + r + 12), outline=T['cyan'], width=5)
        cv.text((px, py), k, 30, tc, anchor='mm', bold=True)


def _t(S):
    inn = S.get('_inner', {})
    if 'ans' in S and 's' in S and 'fa' not in inn:
        return f"质数 ==%d==：前面各块非质数共 `s = %d` 个；已累计 ans = ==%d==" % (S['x'], S['s'], S['ans'])
    return ''


CONFIG = dict(
    num=2867, title='统计树中的合法路径数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举质数 · 非质数连通块 · 乘法原理', tags=['数学算法', '链表树与回溯', '难度分 2428'],
    setup=SETUP,
    code='''
class Solution:
    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        nodes = []
        def dfs(x: int, fa: int) -> None:
            nodes.append(x)
            for y in g[x]:
                if y != fa and not is_prime[y]:
                    dfs(y, x)

        ans = 0
        size = [0] * (n + 1)
        for x in range(1, n + 1):
            if not is_prime[x]:  # 跳过非质数
                continue
            s = 0
            for y in g[x]:  # 质数 x 把这棵树分成了若干个连通块
                if is_prime[y]:
                    continue
                if size[y] == 0:  # 尚未计算过
                    nodes.clear()
                    dfs(y, -1)  # 遍历 y 所在连通块，在不经过质数的前提下，统计有多少个非质数
                    for z in nodes:
                        size[z] = len(nodes)
                # 这 size[y] 个非质数与之前遍历到的 s 个非质数，两两之间的路径只包含质数 x
                ans += size[y] * s
                s += size[y]
            ans += s  # 从 x 出发的路径
        return ans
''',
    call='Solution().countPaths(%d, %r)' % (N, EDGES),
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='size', h=190, label='size（非质数所在连通块的大小，0 = 还没算）', pointers={'y': 'blue'}, cell=70),
        dict(type='text', fn=_t, h=110),
    ],
    watch=[('x', 'x', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    skip=['g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'nodes = []', 'ans = 0', 'size = [0]', 'nodes.clear()', 'continue'],
    max_steps=80,
    captions={
        'for x in range(1, n + 1)': lambda S, B, r: ('枚举完所有点' if getattr(B, 'x', None) == S.x and S.x == S.n else f'枚举点 `x = {S.x}`'),
        'if not is_prime[x]': lambda S, B, r: (f'`{S.x}` 不是质数 → 跳过（只枚举质数当“中间点”）' if not is_prime_(S.x) else f'`{S.x}` 是质数：路径恰好经过它一个质数'),
        's = 0': '`s`：前面已处理的几块里，非质数的个数',
        '质数 x 把这棵树分成': lambda S, B, r: ('质数 `%d` 的邻居都看完了' % S.x if getattr(B, 'y', None) == S.y and S.y == S.g[S.x][-1] else f'质数 `{S.x}` 把树拆成若干块，看邻居 `y = {S.y}`'),
        11: lambda S, B, r: ('这个点的邻居都看完了，返回' if getattr(B, 'y', None) == S.y and S.y == S.g[S.x][-1] else f'DFS 在 `{S.x}`，看邻居 `y = {S.y}`'),
        'if is_prime[y]': lambda S, B, r: (f'邻居 `{S.y}` 是质数，不能经过 → 跳过' if is_prime_(S.y) else f'邻居 `{S.y}` 是非质数，属于一个连通块'),
        'if size[y] == 0': lambda S, B, r: (f'`size[{S.y}] = 0`：这块还没算过，DFS 数一数' if S.size[S.y] == 0 else f'`size[{S.y}] = {S.size[S.y]}`：之前算过，直接用'),
        'dfs(y, -1)': '从 `y` 出发 DFS，只走非质数（遇到质数就停），数出连通块',
        'nodes.append(x)': '`{x}` 属于这个连通块 → `nodes = {nodes}`',
        'if y != fa and not is_prime[y]': lambda S, B, r: (f'邻居 `{S.y}`：' + ('不是父节点且不是质数 → 继续往里走' if (S.y != S.fa and not is_prime_(S.y)) else ('是父节点，不回头' if S.y == S.fa else '是质数，到边界了，不进'))),
        'dfs(y, x)': '进入 `{y}`',
        'size[z] = len(nodes)': '块里每个点都记下大小 `{len(nodes)}`，以后同块不用再 DFS',
        'ans += size[y] * s': '乘法原理：这块 `{size[y]}` 个非质数 × 之前块的 `{s}` 个，两两路径只经过质数 `{x}` → `ans` = =={ans}==',
        's += size[y]': '这块并入 `s` = =={s}==',
        'ans += s  #': '质数 `{x}` 与 `s = {s}` 个非质数的路径（从 x 出发），`ans` = =={ans}==',
        'return ans': '合法路径共 `{ans}` 条',
    },
    cards=dict(
        one_liner='路径恰有一个质数 ⇔ 枚举这个质数，两侧各取非质数连通块里的点',
        complexity='时间 `O(n)`，空间 `O(n)`（预处理不计）',
        problem=['树上节点编号 `1..n`，路径 `(a, b)` 恰好含一个质数编号才算合法',
                 '`(a, b)` 与 `(b, a)` 算同一条，求合法路径条数',
                 '示例：`n = 6`，`edges = [[1,2],[1,3],[2,4],[3,5],[3,6]]` → `6`'],
        quote='代码实现时，为避免反复 DFS 同一个非质数连通块，可以把每个非质数所处的连通块的大小记录下来（类似记忆化搜索）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['“枚举中间”：枚举路径上唯一的质数 `x`，它把树分成几块，只走非质数的连通块',
              '块内任意点到 `x` 的路径只含质数 `x`：这是从 `x` 出发的路径，共 `s` 条',
              '不同块之间的点，路径必经过 `x`：`size[y] * s` 条，再并入 `s`',
              '块大小用 `size` 缓存，同一块只 DFS 一次，所以总时间 `O(n)`'],
        summary=['时间 `O(n)`：每个非质数只 DFS 一次；空间 `O(n)`',
                 '质数表是 `10^5` 以内的预处理，演示里放在 `setup` 中先算好（原文在类外）',
                 '易错：先 `ans += size[y] * s` 再 `s += size[y]`，最后别忘了 `ans += s`（x 作为端点）',
                 '同类题：2242 节点序列的最大得分，同样是“枚举中间”'],
    ),
)
