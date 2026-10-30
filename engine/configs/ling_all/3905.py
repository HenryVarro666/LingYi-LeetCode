PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange']


def _color(S, i, j, v):
    return PAL[v % 7] if v else None


def _qv(S):
    return [f'{a},{b}:{c}' for a, b, c in S['q']] if 'q' in S else None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.n and 0 <= y < S.m):
        return f'邻居 `({x},{y})` 越界'
    if S.ans[x][y] != 0:
        return f'邻居 `({x},{y})` 已经是颜色 `{S.ans[x][y]}` → 不覆盖'
    return f'邻居 `({x},{y})` 还没着色 → ==染成 `{S.c}`=='


CONFIG = dict(
    num=3905, title='多源图像渲染', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='多源 BFS · 颜色大的先入队',
    tags=['灵神题单', '网格图', '难度分 1671'],
    code='''
class Solution:
    def colorGrid(self, n: int, m: int, sources: list[list[int]]) -> list[list[int]]:
        ans = [[0] * m for _ in range(n)]
        for x, y, c in sources:
            ans[x][y] = c  # 初始颜色

        sources.sort(key=lambda s: -s[2])
        q = deque(sources)

        while q:
            i, j, c = q.popleft()
            for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 左右上下
                if 0 <= x < n and 0 <= y < m and ans[x][y] == 0:  # (x, y) 未着色
                    ans[x][y] = c  # 着色
                    q.append((x, y, c))  # 继续扩散

        return ans
''',
    call='Solution().colorGrid(3, 3, [[0, 0, 1], [2, 2, 2]])',
    expect=[[1, 1, 2], [1, 2, 2], [2, 2, 2]],
    skip=['for x, y, c in sources', 'q.append((x, y, c))'],
    views=[
        dict(type='grid', var='ans', label='ans（0 = 未着色；颜色 = 数值；蓝框 = 出队扩散的格子，粉框 = 正在看的邻居）', cell=110, h=400,
             color=_color, cursors=[('i', 'j', 'blue'), ('x if _line == 13 else None', 'y', 'pink')]),
        dict(type='array', var=_qv, label='q（行,列:颜色；颜色大的排在前面）', cell=130, h=190),
    ],
    watch=[('c', 'c', 'green')],
    captions={
        'ans = [[0]': '先全部是 `0`（未着色）',
        'ans[x][y] = c  # 初始颜色': '源点 `({x},{y})` 先涂上初始颜色 `{c}`',
        'sources.sort': '==按颜色从大到小排序==：同一时刻到达同一格时，颜色大的先抢到 → `{sources}`',
        'q = deque': '按这个顺序把所有源点一起入队，作为多源 BFS 的第 0 层',
        'while q': lambda S, B, r: ('队列非空 → 继续扩散' if S.q else '队列空了 → 没有格子能再着色'),
        'q.popleft': '出队 `({i},{j})`，颜色 `{c}`：向左右上下扩散',
        'if 0 <= x < n': _nb,
        'ans[x][y] = c': '`ans[{x}][{y}] = {c}`：先着色的就是最终颜色，==后到的不会覆盖==',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='多源 BFS：把颜色大的源点排在队头，平局就自然取最大',
        complexity='时间 `O(k log k + nm)`，空间 `O(nm)`',
        problem=['`n × m` 网格，`sources[i] = [r, c, color]` 是初始着色的格子',
                 '每个单位时间，已着色格子同时向四邻未着色格子扩散自己的颜色',
                 '多种颜色同时到达，取==最大==的颜色',
                 '本视频：`n=3, m=3`，`sources=[[0,0,1],[2,2,2]]` → `[[1,1,2],[1,2,2],[2,2,2]]`'],
        quote='我们可以先把 sources 按照 color 从大到小排序，然后把 sources 中的所有元素入队。这样在 BFS 的过程中，我们会优先扩散颜色大的单元格，这些单元格的邻居会先入队。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一层里，先出队的先着色，后面的看到 `ans != 0` 就不再覆盖',
              '所以只要让大颜色先入队，平局时大颜色就赢',
              '后续层的入队顺序继承前一层，这个优先级一直保持'],
        summary=['时间 `O(k log k + nm)`：排序 `k` 个源点，BFS 每格入队一次',
                 '易错：初始颜色要先全部写进 `ans`，再排序入队',
                 '易错：着色发生在==入队时==，不是出队时，否则会被重复着色',
                 '注意 `sources.sort` 会原地修改输入',
                 '相关：1765. 地图中的最高点（网格图 BFS）'],
    ),
)
