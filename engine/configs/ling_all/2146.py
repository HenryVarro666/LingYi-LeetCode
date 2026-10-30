GRID = [[1, 2, 0, 1], [1, 3, 0, 1], [0, 2, 5, 1]]


def _color(S, i, j, v):
    if 'ans' not in S:
        return None
    if [i, j] in [list(p) for p in S['ans']]:
        return 'green'
    if (i, j) in S['q']:
        return 'orange'
    if (i, j) in S['vis']:
        return 'cyan'
    return None


def _qfmt(S):
    return [f'{a},{b}' for a, b in S['q']] if 'q' in S else None


def _ans(S):
    return [f'{a},{b}' for a, b in S['ans']] if 'ans' in S else None


def _check(S, B, r):
    n = len(S.ans)
    if n >= S.k:
        return f'已收集 `{n}` ≥ `k = {S.k}` → ==够了，直接截取前 k 个返回=='
    return f'已收集 `{n}` < `k = {S.k}` → 还不够，继续向外扩一层'


CONFIG = dict(
    num=2146, title='价格范围内最高排名的 K 样物品', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='分层 BFS + 层内排序',
    tags=['灵神题单', '网格图', '难度分 1837'],
    code='''
class Solution:
    def highestRankedKItems(self, grid: List[List[int]], pricing: List[int], start: List[int], k: int) -> List[List[int]]:
        ans = []
        m, n = len(grid), len(grid[0])
        low, high = pricing
        sx, sy = start
        vis = {(sx, sy)}
        q = [(sx, sy)]
        while q:  # 分层 BFS
            # 此时 q 内所有元素到起点的距离均相同，因此按照题目中的第 2~4 关键字排序后，就可以将价格在 [low,high] 内的位置加入答案
            q.sort(key=lambda p: (grid[p[0]][p[1]], p))
            ans.extend(p for p in q if low <= grid[p[0]][p[1]] <= high)
            if len(ans) >= k: return ans[:k]
            tmp = q
            q = []
            for i, j in tmp:
                for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):
                    if 0 <= x < m and 0 <= y < n and grid[x][y] and (x, y) not in vis:
                        vis.add((x, y))
                        q.append((x, y))
        return ans
''',
    call=f'Solution().highestRankedKItems({GRID}, [2, 5], [0, 0], 3)',
    expect=[(0, 1), (1, 1), (2, 1)],
    result_fn=lambda r: [tuple(p) for p in r],
    skip=['m, n = len', 'low, high = pricing', 'sx, sy = start', 'tmp = q', 'q = []'],
    views=[
        dict(type='grid', var='grid', label='grid（0 墙；青 已访问；橙 当前层；绿 已入答案）',
             cell=100, h=330, color=_color, cursors=[('x if _line == 18 else None', 'y', 'yellow')]),
        dict(type='array', var=_qfmt, label='q（当前这一层，到起点距离相同）', cell=76, h=150),
        dict(type='array', var=_ans, label='ans（按距离、价格、行、列排好）', cell=76, h=150),
    ],
    watch=[('k', 'k'), ('low', 'low'), ('high', 'high'), ('len(ans)', 'len(ans) if "ans" in S else 0', 'green')],
    captions={
        'vis = {': '`vis` 记录访问过的格子，起点先放进去',
        'q = [(sx, sy)]': '队列只放==当前这一层==：此刻只有起点，距离 0',
        'while q': lambda S, B, r: ('当前这一层 `q` 非空 → 处理这一层' if S.q else '没有更远的格子了 → 结束'),
        'q.sort': '这一层距离都相同 → 只需按 ==价格、行、列== 排序：`q = {q}`',
        'ans.extend': '把这一层里价格在 `[{low}, {high}]` 的格子按顺序收入答案 → `ans` 共 `{len(ans)}` 个',
        'if len(ans) >= k': _check,
        'for i, j in tmp': lambda S, B, r: ('这一层的格子都处理完了，进入下一层' if B.get('i') == S.get('i') and B.get('j') == S.get('j') else f'取出这一层的 `({S.i},{S.j})`，看它四周'),
        'if 0 <= x < m': lambda S, B, r: (f'邻居 `({S.x},{S.y})` 越界' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
                                          else f'邻居 `({S.x},{S.y})` 是墙 → 不能走' if S.grid[S.x][S.y] == 0
                                          else f'邻居 `({S.x},{S.y})` 已访问过 → 跳过' if (S.x, S.y) in S.vis
                                          else f'邻居 `({S.x},{S.y})` 可走且没访问过 → ==进入下一层=='),
        'vis.add': '标记 `({x},{y})` 已访问',
        'q.append': '`({x},{y})` 进入下一层队列',
        'return ans[:k]': '取前 `k` 个：`{ret}`',
        'return ans': '全部返回：`{ret}`',
    },
    cards=dict(
        one_liner='分层 BFS：一层距离相同，层内只排价格和坐标',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格 `grid`：`0` 是墙，`1` 是空格，其他正整数是物品价格',
                 '从 `start` 出发，找价格在 `[low, high]` 内、排名最高的 `k` 件',
                 '排名：==距离 → 价格 → 行 → 列==，都是越小越靠前',
                 '本视频：`pricing=[2,5]`，`start=[0,0]`，`k=3` → `[[0,1],[1,1],[2,1]]`'],
        quote='我们可以采用分层 BFS 的做法，即每次 BFS 时向外扩展一层，然后对扩展出的这些位置排序，取将价格在 [low,high] 中的物品位置加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['距离是第一关键字 → 一层一层扩，同一层距离相等',
              '层内只要按 `(价格, (行, 列))` 排序即可',
              '收集够 `k` 个就立刻返回，不用扫完整张图'],
        summary=['时间 `O(mn log(mn))`：每格入队一次，排序总量不超过 mn',
                 '易错：起点本身也可能是符合价格的物品，所以排序收集放在扩展之前',
                 '易错：`grid[x][y]` 为 0 是墙，不能入队',
                 '排序键 `(grid[i][j], p)`，`p` 是 `(行, 列)` 元组，正好是第 3、4 关键字',
                 '前置题：1765. 地图中的最高点（网格图 BFS）'],
    ),
)
