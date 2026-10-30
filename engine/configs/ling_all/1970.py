ROW, COL = 3, 2
CELLS = [[1, 1], [2, 1], [3, 2], [2, 2], [1, 2], [3, 1]]
DAY = [[0] * COL for _ in range(ROW)]
for _d, (_r, _c) in enumerate(CELLS):
    DAY[_r - 1][_c - 1] = _d + 1          # 第 d+1 天变成水（图上显示的数字）
TOP, BOT = ROW * COL, ROW * COL + 1


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _fa(S):
    uf = S.get('uf')
    return list(uf._fa) if uf is not None and hasattr(uf, '_fa') else None


def _gcolor(S, i, j, v):
    land = S.get('land')
    if land is None or 'uf' not in S:
        return None
    if not land[i][j]:
        return None
    fa = S['uf']._fa
    rt = _root(fa, i * COL + j)
    if rt == _root(fa, TOP) and rt == _root(fa, BOT):
        return 'yellow'
    if rt == _root(fa, TOP):
        return 'cyan'
    if rt == _root(fa, BOT):
        return 'orange'
    return 'green'


def _gdim(S, i, j, v):
    land = S.get('land')
    return land is not None and not land[i][j]


def _atcolor(S, i, v):
    uf = S.get('uf')
    if uf is None:
        return None
    fa = uf._fa
    if i == TOP:
        return 'cyan'
    if i == BOT:
        return 'orange'
    return None


def _conn(S):
    uf = S.get('uf')
    land = S.get('land')
    if uf is None or land is None:
        return ''
    fa = uf._fa
    cnt = sum(sum(1 for x in rw if x) for rw in land)
    same = _root(fa, TOP) == _root(fa, BOT)
    st = '==已连通=='  if same else '还没连通'
    return f"已恢复成陆地 `{cnt}` 格；最上边 `top` 与最下边 `bottom`：{st}"


CONFIG = dict(
    num=1970, title='你能穿过矩阵的最后一天', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='时光倒流 · 并查集',
    tags=['七、并查集', '§7.2 进阶', '难度分 2124'],
    code='''
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己
        self._fa = list(range(n))  # 代表元

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        fa = self._fa
        # 如果 fa[x] == x，则表示 x 是代表元
        if fa[x] != x:
            fa[x] = self.find(fa[x])  # fa 改成代表元
        return fa[x]

    # 判断 x 和 y 是否在同一个集合
    def is_same(self, x: int, y: int) -> bool:
        # 如果 x 的代表元和 y 的代表元相同，那么 x 和 y 就在同一个集合
        # 这就是代表元的作用：用来快速判断两个元素是否在同一个集合
        return self.find(x) == self.find(y)

    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, from_: int, to: int) -> None:
        x, y = self.find(from_), self.find(to)
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了

class Solution:
    def latestDayToCross(self, m: int, n: int, cells: List[List[int]]) -> int:
        DIRS = (0, -1), (0, 1), (-1, 0), (1, 0)  # 左右上下

        top = m * n
        bottom = m * n + 1
        uf = UnionFind(m * n + 2)
        land = [[False] * n for _ in range(m)]

        for day in range(len(cells) - 1, -1, -1):
            r, c = cells[day]
            r -= 1  # 改成从 0 开始的下标
            c -= 1
            v = r * n + c
            land[r][c] = True  # 变成陆地

            if r == 0:
                uf.merge(v, top)  # 与最上边相连

            if r == m - 1:
                uf.merge(v, bottom)  # 与最下边相连

            for dx, dy in DIRS:
                x, y = r + dx, c + dy
                if 0 <= x < m and 0 <= y < n and land[x][y]:
                    uf.merge(v, x * n + y)  # 与四周的陆地相连

            if uf.is_same(top, bottom):  # 最上边和最下边连通
                return day
''',
    call=f'Solution().latestDayToCross({ROW}, {COL}, {CELLS})',
    expect=2,
    skip=['DIRS =', 'top =', 'bottom =', 'r -= 1', 'c -= 1', 'v = r * n + c', 'for dx, dy in DIRS', 'x, y = r + dx',
          'fa = self._fa', 'return fa[x]', 'self._fa = list', 'if fa[x] != x',
          'x, y = self.find(from_)', 'land = [[False]', 'uf = UnionFind'],
    max_steps=85,
    views=[
        dict(type='grid', var=lambda S: DAY, cell=96, h=330, color=_gcolor, dim=_gdim, rows=None,
             label='数字=第几天被淹；暗=仍是水；绿=陆地；青=连上边；橙=连下边；黄=上下已通',
             cursors=[('r', 'c', 'pink')]),
        dict(type='array', var=_fa, cell=64, h=170, color=_atcolor,
             label='uf._fa（下标 = r*n+c；6 = top 青，7 = bottom 橙）'),
        dict(type='text', fn=_conn, h=60, size=28),
    ],
    watch=[('day', 'day', 'blue'), ('(r, c)', '(r, c) if "r" in dir() else None', 'pink'), ('v', 'v if "v" in dir() else None')],
    captions={
        'self._fa = list(range(n))': '每个格子一开始自成一个集合：`fa[i] = i`，==代表元就是自己==',
        'fa[x] = self.find(fa[x])': '`fa[{B.x}] = {B.fa[B.x]}` 不是自己 → `{B.x}` 不是代表元：先递归找到代表元，再==路径压缩==，让 `fa[{B.x}]` 直接指向它',
        'self._fa[x] = y': lambda S, B, r_: (f'`{S.x}` 和 `{S.y}` 的代表元相同，本来就在同一个集合，不用动' if S.x == S.y
                                             else f'合并：把代表元 `{S.x}` 挂到代表元 `{S.y}` 下面，`fa[{S.x}] = {S.y}`'),
        'DIRS =': '四个方向：左右上下',
        'top = m * n': '虚拟节点 `top = m*n`：代表“最上边”',
        'bottom = m * n + 1': '虚拟节点 `bottom = m*n+1`：代表“最下边”',
        'uf = UnionFind': '`m*n + 2` 个节点：所有格子再加上 top 和 bottom',
        'land = [[False]': '`land[r][c]` 表示 (r,c) 此刻是不是陆地：==一开始全是水==（倒着看）',
        'for day in range': lambda S, B, r: (f'==时光倒流==：从最后一天开始，每天把一块水变回陆地。现在是 `day = {S.day}`'
                                             if 'day' in S else '循环结束'),
        'r, c = cells[day]': '第 `{day}` 天（下标）被淹的是第 `{r}` 行第 `{c}` 列（从 1 开始）；倒着看，它要==变回陆地==',
        'land[r][c] = True': '`({r},{c})` 变成陆地，编号 `v = {v}`',
        'if r == 0': lambda S, B, r_: (f'`r = 0`：在第一行 → 与 `top` 相连' if B.r == 0 else f'`r = {B.r}`：不在第一行'),
        'uf.merge(v, top)': '在第一行，和虚拟节点 `top` 合并',
        'if r == m - 1': lambda S, B, r_: (f'`r = {B.r} = m-1`：在最后一行 → 与 `bottom` 相连' if B.r == B.m - 1
                                           else f'`r = {B.r}`：不在最后一行'),
        'uf.merge(v, bottom)': '在最后一行，和虚拟节点 `bottom` 合并',
        'if 0 <= x < m': lambda S, B, r_: (f'邻居 `({B.x},{B.y})` 越界' if not (0 <= B.x < B.m and 0 <= B.y < B.n)
                                           else (f'邻居 `({B.x},{B.y})` 是陆地 → ==合并=='
                                                 if B.land[B.x][B.y] else f'邻居 `({B.x},{B.y})` 还是水 → ==不能连==')),
        'uf.merge(v, x * n + y)': '和邻居陆地合并到同一个集合',
        'if uf.is_same(top, bottom)': lambda S, B, r_: ('`top` 和 `bottom` ==连通==：倒着第一次能从上走到下 → 答案就是 `day`'
                                                         if _root(S.uf._fa, S.top) == _root(S.uf._fa, S.bottom)
                                                         else '`top` 和 `bottom` 还没连通，继续把下一块水变回陆地'),
        'return day': '倒着遍历，第一次连通就返回：答案 `day = {day}`（第 `{day}` 天结束时仍能通过）',
        'return self.find(x) == self.find(y)': '`is_same`：两个代表元相同 ↔ 同一个集合 ↔ 连通',
    },
    cards=dict(
        one_liner='并查集只擅长加边：把时间倒过来，淹水就变成了填陆地',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['`row × col` 的矩阵，第 `i` 天 `cells[i]` 这格陆地变成水',
                 '求==最后一天==仍能只走陆地、从最上一行走到最下一行',
                 '本视频：`3×2`，`cells = [[1,1],[2,1],[3,2],[2,2],[1,2],[3,1]]` → `2`'],
        quote='本质是判断最上边和最下边是否连通。并查集加边很好做，但删边不好做。如果时光倒流，删边就成了加边（把水变成陆地）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正着看是不断淹水（删点），并查集不好做；==倒着看就是不断填陆地==',
              '格子 `(r,c)` 编号 `r*n+c`，再加虚拟节点 `top`、`bottom`',
              '第一行的陆地连 `top`，最后一行的连 `bottom`，再和四周陆地合并',
              '倒着遍历，==第一次==发现 `top` 与 `bottom` 连通，就返回 `day`'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '易错：`cells` 的行列从 1 开始，要先减 1；不要把陆地和水连起来',
                 '题目保证第 0 天一定连通，所以倒着一定会返回',
                 '灵神还给了 DFS 感染写法（`O(mn)`），以及正序用八方向水从左流到右的写法，本视频只演示并查集',
                 '同类题：803 打砖块（同样是逆序加边）'],
    ),
)
