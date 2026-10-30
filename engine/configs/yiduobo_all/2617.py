GRID = [[2, 2, 1], [1, 1, 0]]


def _heaps(S):
    hh, vh = S.get('h_heap'), S.get('v_heap')
    if hh is None or vh is None:
        return ''
    fmt = lambda h: '空' if not h else '  '.join(f'({a}步,最远到{b})' for a, b in sorted(h))
    return ('行堆 h_heap：' + '   |   '.join(f'第{i}行: {fmt(h)}' for i, h in enumerate(hh)) + '\n'
            + '列堆 v_heap：' + '   |   '.join(f'第{j}列: {fmt(h)}' for j, h in enumerate(vh)))


def _cell(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None:
        return None
    if (i, j) == (ci, cj):
        return 'yellow'
    if v != -1:
        return 'green'
    return None


def _hq(S, B, r):
    h = S.h_heap[S.i]
    if h:
        return f'行堆不空，堆顶 `({h[0][0]}步, 最远到{h[0][1]})`：从左边的那一格能走到这里'
    return f'第 {S.i} 行的堆空了：左边没有格子能跳到第 {S.j} 列，保持 `-1`'


def _vq(S, B, r):
    h = S.v_heap[S.j]
    if h:
        return f'列堆不空，堆顶 `({h[0][0]}步, 最远到{h[0][1]})`：上边的那一格能走到这里，和左边的结果比一比'
    return f'第 {S.j} 列的堆空了：上边没有格子能跳到第 {S.i} 行'


CONFIG = dict(
    num=2617, title='网格图中最少访问的格子数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='每行每列一个最小堆 + 惰性弹出',
    tags=['网格图', '动态规划', '难度分 2582'],
    code='''
class Solution(object):
    def minimumVisitedCells(self, grid):

        m = len(grid)
        n = len(grid[0])

        h_heap = [[] for _ in range(m)]
        v_heap = [[] for _ in range(n)]
        f = [[-1] * n for _ in range(m)]
        f[0][0] = 1

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    heapq.heappush(h_heap[0], [1, grid[0][0]])
                    heapq.heappush(v_heap[0], [1, grid[0][0]])
                else:
                    while h_heap[i] and h_heap[i][0][1] < j:
                        heapq.heappop(h_heap[i])
                    
                    if h_heap[i]:
                        f[i][j] = h_heap[i][0][0] + 1
                    
                    while v_heap[j] and v_heap[j][0][1] < i:
                        heapq.heappop(v_heap[j])
                    
                    if v_heap[j]:
                        if f[i][j] == -1 or f[i][j] > v_heap[j][0][0] + 1:
                            f[i][j] = v_heap[j][0][0] + 1
                    
                    if f[i][j] != -1 and grid[i][j] > 0:
                        heapq.heappush(h_heap[i], [f[i][j], j + grid[i][j]])
                        heapq.heappush(v_heap[j], [f[i][j], i + grid[i][j]])

        return f[-1][-1]
''',
    call=f'Solution().minimumVisitedCells({GRID})',
    expect=3,
    skip=['m = len', 'n = len', 'h_heap = [[]', 'v_heap = [[]', 'f = [[-1]', 'for j in range(n)'],
    views=[
        dict(type='grid', var='f', label='f[i][j]：走到 (i,j) 的最少格子数（-1 = 到不了；黄 = 当前格，绿 = 已算出）', cell=110, h=260,
             color=_cell, cursors=[('i', 'j', 'yellow')]),
        dict(type='grid', var='grid', label='grid（每格最多能跳几步）', cell=70, h=190),
        dict(type='text', fn=_heaps, size=21, h=110),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'f[0][0] = 1': '起点算 1 个格子：`f[0][0] = 1`；其余先标 -1（到不了）',
        'if i == 0 and j == 0': lambda S, B, r: ('起点：把它的 `(1, 最远到达位置)` 放进本行堆和本列堆' if S.i == 0 and S.j == 0
                                                 else f'处理 `({S.i},{S.j})`：先从左边找，再从上边找'),
        'heapq.heappush(h_heap[0]': '行堆放入 `[1, {grid[0][0]}]`：步数 1，向右最远到第 {grid[0][0]} 列',
        'heapq.heappush(v_heap[0]': '列堆放入 `[1, {grid[0][0]}]`：步数 1，向下最远到第 {grid[0][0]} 行',
        'while h_heap[i] and': lambda S, B, r: (f'堆顶 `最远到 {S.h_heap[S.i][0][1]} < 列 {S.j}`：够不到第 {S.j} 列，也就够不到更右边 → ==永久弹出=='
                                                if S.h_heap[S.i] and S.h_heap[S.i][0][1] < S.j else '堆顶还够得到当前列（或堆已空），不用再弹'),
        'heapq.heappop(h_heap[i])': '弹出堆顶后继续检查新的堆顶',
        'if h_heap[i]:': _hq,
        'while v_heap[j] and': lambda S, B, r: (f'堆顶 `最远到 {S.v_heap[S.j][0][1]} < 行 {S.i}`：够不到第 {S.i} 行 → ==永久弹出=='
                                                if S.v_heap[S.j] and S.v_heap[S.j][0][1] < S.i else '列堆顶还够得到当前行（或已空），不用再弹'),
        'heapq.heappop(v_heap[j])': '弹出列堆顶后继续检查',
        'if v_heap[j]:': _vq,
        'if f[i][j] == -1 or': lambda S, B, r: (f'左边没走到（`-1`），直接用上边的 `{S.v_heap[S.j][0][0] + 1}`' if S.f[S.i][S.j] == -1
                                                else f'左边得到 `{S.f[S.i][S.j]}`，上边是 `{S.v_heap[S.j][0][0] + 1}`：谁小用谁'),
        'f[i][j] = v_heap[j][0][0] + 1': '上边更好：`f[{i}][{j}] = {v_heap[j][0][0]} + 1 = =={f[i][j]}==`',
        'f[i][j] = h_heap[i][0][0] + 1': '从左边来：`f[{i}][{j}] = {h_heap[i][0][0]} + 1 = =={f[i][j]}==`',
        'if f[i][j] != -1 and grid': lambda S, B, r: (f'`f = {S.f[S.i][S.j]}`，`grid = {S.grid[S.i][S.j]}` > 0：能继续跳，把它加入行堆和列堆'
                                                      if S.f[S.i][S.j] != -1 and S.grid[S.i][S.j] > 0
                                                      else '到不了这格或跳不动（`grid = 0`），不入堆'),
        'heapq.heappush(h_heap[i]': '行堆加入 `[{f[i][j]}, {j + grid[i][j]}]`：步数，向右最远到的列',
        'heapq.heappush(v_heap[j]': '列堆加入 `[{f[i][j]}, {i + grid[i][j]}]`：步数，向下最远到的行',
        'return f[-1][-1]': lambda S, B, r: (f'右下角 `f[-1][-1] = {r}`' if r != -1 else '右下角是 -1：到不了'),
    },
    cards=dict(
        one_liner='每行每列各养一个最小堆：堆里是「能从这里跳过来」的候选',
        complexity='时间 `O(mn(log m + log n))`，空间 `O(mn)`',
        problem=['`grid[i][j]` 是在 `(i,j)` 最多能向右或向下走的步数',
                 '从左上角出发，求到右下角==最少经过的格子数==，到不了返回 `-1`',
                 '示例：`[[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]]` → `4`；本视频用 2×3 小例子'],
        quote='若(i, k)由于步长的限制无法到达(i, j)，那么自然也不可能到达(i, j + 1)以及更右侧的位置……因此没必要再将这些位置留在==堆==中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 只可能从同一行左边或同一列上边走来，要对候选取最小步数',
              '每行一个堆、每列一个堆，存 `(步数, 最远能到哪)`',
              '堆顶够不到当前列就弹出：以后更右边的列更够不到，所以==弹了不会错=='],
        summary=['时间 `O(mn(log m + log n))`：每个格子最多入堆、出堆各一次',
                 '`f` 初值是 -1 表示到不了，比较时要先判断 `== -1`',
                 '起点单独处理；`grid = 0` 的格子到得了也不能入堆',
                 '原文为 Python 2 风格，代码未做改动（直接是 Python 3 可运行）',
                 '对比灵神：灵神用单调栈 + 二分，yiduobo 用堆 + 惰性弹出，思路更直观'],
    ),
)
