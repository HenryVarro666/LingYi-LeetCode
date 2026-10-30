GRID = [[1, 2, 0, 1], [1, 3, 3, 1], [0, 2, 5, 1]]


def _color(S, i, j, v):
    if 'used' not in S:
        return None
    n = S['n']
    if 'step' in S and 'l' in S and 'r' in S and i * n + j in S['used']:
        return 'cyan'
    return None


def _cand(S):
    return [f"{a},{b},{c},{d}" for a, b, c, d in S['candidate']] if 'candidate' in S else None


def _qv(S):
    return [f'{a},{b}' for a, b in S['q']] if 'q' in S else None


CONFIG = dict(
    num=2146, title='价格范围内最高排名的 K 样物品', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 收集候选 + 四关键字排序',
    tags=['灵神题单', '网格图', '难度分 1837'],
    code='''
class Solution(object):
    def highestRankedKItems(self, grid, pricing, start, k):

        m = len(grid)
        n = len(grid[0])

        q = [start]
        used = set([start[0] * n + start[1]])
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        step = 0
        candidate = []

        l = 0
        r = 1
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                if grid[nowx][nowy] >= pricing[0] and grid[nowx][nowy] <= pricing[1]:
                    candidate.append([step, grid[nowx][nowy], nowx, nowy])
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] > 0 and x * n + y not in used:
                        q.append([x, y])
                        used.add(x * n + y)
            
            l, r = r, len(q)
        
        return [[x, y] for _, _, x, y in sorted(candidate)[:k]]
''',
    call=f'Solution().highestRankedKItems({GRID}, [2, 3], [2, 3], 2)',
    expect=[[2, 1], [1, 2]],
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'step = 0', 'candidate = []', 'l = 0', 'r = 1',
          'for index in range(4)', 'x = nowx', 'y = nowy', 'q.append', 'used.add'],
    views=[
        dict(type='grid', var='grid', label='grid（0 = 墙；青 = 已访问；蓝框 = 当前处理的格子；粉框 = 邻居）', cell=100, h=330,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x if _line == 24 else None', 'y', 'pink')]),
        dict(type='array', var=_qv, label='q（暗 = 已处理；l..r 是当前这一层）', cell=76, h=150,
             dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='array', var=_cand, label='candidate（距离,价格,行,列）', cell=118, h=150),
    ],
    watch=[('step', 'step', 'orange'), ('l', 'l', 'blue'), ('r', 'r'),
           ('价格范围', 'pricing')],
    captions={
        'q = [start]': '队列从起点 `{start}` 出发',
        'used = set': '`used` 记录访问过的格子，格子 `(x, y)` 编码成 `x * n + y`：起点的编码是 `{list(used)[0]}`',
        'while l < r': lambda S, B, r: (f'队列里 `[{B.l}, {B.r})` 是当前这一层，非空 → 继续' if B.l < B.r
                                        else '没有新的格子了 → BFS 结束，开始排序取 top k'),
        'step += 1': '这一层的距离 `step = {step}`（起点记作 1，整体 +1 不影响排名）',
        'for nowx, nowy in': lambda S, B, r: ('这一层的格子都处理完了' if B.get('nowx') == S.get('nowx') and B.get('nowy') == S.get('nowy') else f'处理这一层的 `({S.nowx},{S.nowy})`'),
        'if grid[nowx][nowy] >= pricing[0]': lambda S, B, r: (
            f'价格 `{S.grid[S.nowx][S.nowy]}` 在 `[{S.pricing[0]}, {S.pricing[1]}]` 内 → ==打包 `[距离, 价格, 行, 列]` 入候选=='
            if S.pricing[0] <= S.grid[S.nowx][S.nowy] <= S.pricing[1]
            else f'价格 `{S.grid[S.nowx][S.nowy]}` 不在 `[{S.pricing[0]}, {S.pricing[1]}]` 内 → 不是候选，但仍要往外扩'),
        'candidate.append': '候选加入 `{candidate[-1]}`：顺序正好是距离、价格、行、列',
        'if x >= 0 and x < m': lambda S, B, r: (f'邻居 `({S.x},{S.y})` 越界' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
                                                else f'邻居 `({S.x},{S.y})` 是墙 → 不能走' if S.grid[S.x][S.y] == 0
                                                else f'邻居 `({S.x},{S.y})` 已访问过 → 跳过' if S.x * S.n + S.y in S.used
                                                else f'邻居 `({S.x},{S.y})` 可走且没访问过 → ==入队并标记=='),
        'l, r = r, len(q)': '这一层处理完：下一层是 `[{l}, {r})`，也就是刚入队的这些格子',
        'return [[x, y]': '`sorted(candidate)` 按四个关键字从小到大排，取前 `k = {k}` 个的坐标：`{ret}`',
    },
    cards=dict(
        one_liner='先 BFS 求出每件物品的距离，再把四个关键字打包排序',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格 `grid`：`0` 是墙，`1` 是空格，其他正整数是物品价格',
                 '从 `start` 出发，找价格在 `[low, high]` 内排名最高的 `k` 件',
                 '排名依次比：==距离、价格、行坐标、列坐标==，越小越靠前',
                 '本视频：`pricing=[2,3]`，`start=[2,3]`，`k=2` → `[[2,1],[1,2]]`'],
        quote='为了得到距离，就需要从start开始进行一次bfs，找出从start开始到达每样物品的距离。在bfs的过程中，每接触到一样价格在范围内的物品，就将其按距离、价格、行坐标、列坐标的顺序打包加入到候选答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['后三个关键字直接能拿到，只缺距离 → 从 `start` 做一次 BFS',
              '每个价格合格的格子打包成 `[距离, 价格, 行, 列]` 放进 `candidate`',
              'Python 列表直接 `sorted` 就是按四个关键字依次比较，取前 `k` 个'],
        summary=['时间 `O(mn log(mn))`：BFS 是 `O(mn)`，排序是主要开销',
                 '`step` 起点这层记 1，所有距离整体 +1，不影响排名',
                 '易错：只有 `grid > 0` 才能走；价格合格不代表不能继续扩展',
                 '队列用数组加 `l`、`r` 下标分层，格子用 `x * n + y` 编码进集合',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
