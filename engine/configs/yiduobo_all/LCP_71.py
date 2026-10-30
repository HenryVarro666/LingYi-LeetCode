SHAPE = ["rlrr", "llrl", "llr."]


def _ref(shape):
    """按 yiduobo 的算法离线重放一遍，得到「被统计进 cnt 的区域」按行的先后集合（只用于画图）。"""
    m, n = len(shape), len(shape[0])
    fa = list(range(m * n * 4 + 1))
    linked = set()
    for i in range(m):
        linked.add(i * n * 4 + 4)
        linked.add((i * n + n - 1) * 4 + 2)
    for j in range(n):
        linked.add(((m - 1) * n + j) * 4 + 3)

    def find(x):
        while fa[x] != x:
            x = fa[x]
        return x

    def union(x, y):
        a, b = find(x), find(y)
        if a != b:
            fa[a] = b
            if a in linked:
                linked.add(b)

    counted = {}
    for i in range(m - 1, -1, -1):
        for j in range(n):
            base = (i * n + j) * 4
            if shape[i][j] == '.':
                union(base + 1, base + 2); union(base + 1, base + 3); union(base + 1, base + 4)
            elif shape[i][j] == 'r':
                union(base + 1, base + 4); union(base + 2, base + 3)
            else:
                union(base + 1, base + 2); union(base + 3, base + 4)
        for j in range(n - 1):
            union((i * n + j + 1) * 4 + 4, (i * n + j) * 4 + 2)
        if i != m - 1:
            for j in range(n):
                union(((i + 1) * n + j) * 4 + 1, (i * n + j) * 4 + 3)
        for j in range(n):
            base = (i * n + j) * 4
            for o in range(1, 5):
                if find(base + o) not in linked:
                    counted[base + o] = True
    return counted


def _info(S):
    if 'cnt' not in S or 'linked_water' not in S:
        return None
    shape = S['shape']
    return _ref(tuple(shape)), len(shape), len(shape[0])


def _root(S, x):
    fa = S['fa']
    while fa[x] != x:
        x = fa[x]
    return x


def _regions(S, i, j):
    n = len(S['shape'][0])
    base = (i * n + j) * 4
    return [base + o for o in range(1, 5)]


def _color(S, i, j, v):
    inf = _info(S)
    if inf is None:
        return None
    counted, m, n = inf
    cur = S.get('i')
    done = 'res' in S
    if not done and isinstance(cur, int):
        if i < cur:
            return None
        if i == cur and S.get('_line', 0) < 59:   # 本行的统计循环还没跑
            return 'blue' if i == cur else None
    mine = [x for x in _regions(S, i, j) if x in counted]
    if not mine:
        return 'blue' if (not done and i == cur) else None
    if done:
        return 'green' if all(_root(S, x) in S['linked_water'] for x in mine) else 'orange'
    return 'yellow'


def _cells(S):
    inf = _info(S)
    if inf is None:
        return [list(r) for r in S['shape']]
    return [list(r) for r in S['shape']]


def _text(S):
    if 'res' in S:
        return f"绿 = 与顶行/边界相连的蓄水区，累计 `res = {S['res']}`（区域数），再 `// 2`"
    if 'cnt' not in S:
        return '每格切成 1上 2右 3下 4左 四块；左右下三边的块先放进 `linked_water`'
    return '黄 = 此刻与左右下边界不通的块（可能蓄水），逐行从下往上统计'


CONFIG = dict(
    num='LCP 71', title='集水器', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='四区域并查集 + 与边界相连标记',
    tags=['并查集'],
    code='''
class Solution(object):
    def reservoir(self, shape):

        m = len(shape)
        n = len(shape[0])

        fa = list(range(m * n * 4 + 1))
        linked_water = set()
        cnt = [0] * (m * n * 4 + 1)

        for i in range(m):
            linked_water.add(i * n * 4 + 4)
            linked_water.add((i * n + n - 1) * 4 + 2)
        
        for j in range(n):
            linked_water.add(((m - 1) * n + j) * 4 + 3)
        
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        def union(x, y):
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                cnt[fa_y] += cnt[fa_x]
                if fa_x in linked_water:
                    linked_water.add(fa_y)

        for i in range(m - 1, -1, -1):
            for j in range(n):
                base = (i * n + j) * 4
                if shape[i][j] == '.':
                    union(base + 1, base + 2)
                    union(base + 1, base + 3)
                    union(base + 1, base + 4)
                elif shape[i][j] == 'r':
                    union(base + 1, base + 4)
                    union(base + 2, base + 3)
                else:
                    union(base + 1, base + 2)
                    union(base + 3, base + 4)

            for j in range(n - 1):
                right = (i * n + j) * 4 + 2
                left = (i * n + j + 1) * 4 + 4
                union(left, right)

            if i != m - 1:
                for j in range(n):
                    bottom = (i * n + j) * 4 + 3
                    top = ((i + 1) * n + j) * 4 + 1
                    union(top, bottom)
            
            for j in range(n):
                base = (i * n + j) * 4
                for offset in range(1, 5):
                    if find(base + offset) not in linked_water:
                        cnt[fa[base + offset]] += 1

        for j in range(n):
            linked_water.add(find(j * 4 + 1))

        res = 0
        for index in range(1, m * n * 4 + 1):
            if find(index) == index and index in linked_water:
                res += cnt[index]
        
        return res // 2
''',
    call=f'Solution().reservoir({SHAPE!r})',
    expect=6,
    skip=['m = len', 'n = len', 'fa = list', 'linked_water = set', 'cnt = [0]', 'def find', 'def union',
          'fa_x = find', 'fa_y = find', 'if fa_x != fa_y', 'fa[fa_x] = fa_y', 'cnt[fa_y] +=', 'if fa_x in linked',
          'linked_water.add(fa_y)', 'if fa[x] != x', 'fa[x] = find(fa[x])', 'return fa[x]',
          'for i in range(m):', 'for j in range(n):', 'for j in range(n - 1):', 'for offset in range',
          'for index in range', 'base = (i', 'right = ', 'left = ', 'bottom = ', 'top = ',
          'union(base', "if shape[i][j]", 'elif shape', 'else:', 'union(left, right)', 'union(top, bottom)',
          'if find(base + offset)', 'linked_water.add(find(j', 'for i in range(m - 1, -1, -1)', 'linked_water.add(i', 'linked_water.add((i', 'linked_water.add(((m',
          'if find(index) == index', 'res += cnt'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, size=24, h=60),
        dict(type='grid', var=_cells, label='shape（蓝 = 当前行；黄 = 可能蓄水的块；绿 = 最终有水；橙 = 通向外面）',
             cell=96, h=420, color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('res', 'res', 'green')],
    captions={
        'if i != m - 1': lambda S, B, r: (f"第 `{S.i}` 行：先按隔板合并格内四块，再合并左右邻格，最后（非底行）接上下一行" if S.i != len(S.shape) - 1 else f"最下面一行 `{S.i}`：格内、左右合并；它的下边就是容器底，不用再向下连"),
        'cnt[fa[base + offset]] += 1': lambda S, B, r: (f"块 `{S.base + S.offset}` 合并完这一行后仍够不到左/右/下边界 → ==可能蓄水==，记到根 `{S.fa[S.base + S.offset]}` 上，`cnt = {S.cnt[S.fa[S.base + S.offset]]}`"),
        'res = 0': '先把顶行的上块（1 号块）所在的连通块也标成「与外界相连」：水面上方的空气腔和外面连通。下面只累加这些连通块里的 cnt',
        'return res': '`res = {res}` 个块，每格 4 块、水量记 2 → `res // 2 = {res // 2}`',
    },
    cards=dict(
        one_liner='先切四块并查集，再从下往上数「够不到边界」的块',
        complexity='时间 `O(mn α)`，空间 `O(mn)`',
        problem=['`shape` 里 `l`/`r` 是斜隔板，`.` 是空；集水器从水里竖直取出',
                 '空气能穿过隔板，水不能；每格水量 `2`',
                 '求取出后集水器里留下的水量',
                 '示例：`["rlrr","llrl","llr."]` → `6`'],
        quote='如果一个块可以仅经过较低的块到达左右边界或者底边，那么这个块就无法蓄水。',
        quote_src='—— yiduobo 题解原文',
        idea=['先照 959 题的办法：每格按对角线切成 4 块，按斜线方向并查集合并',
              '从样例看出：只经过「更低」的块就能到边界的块，水会流走',
              '所以从最下面一行往上合并；每合并完一行，数下哪些块还够不到左右下边界'],
        summary=['时间 `O(mn α)`，空间 `O(mn)`；块总数 `4mn`，最后 `res // 2`',
                 '用 `linked_water` 存与左/右/下边界相连的根，`cnt` 存各连通块里的「可能蓄水」块数',
                 '==合并时要把 cnt 和 linked 标记一起并到新根上==，最后再把顶行块标记为连通',
                 '原文为 Python 2 写法，`fa = range(...)` 已改为 `list(range(...))`，`res / 2` 已改为 `res // 2`'],
    ),
)
