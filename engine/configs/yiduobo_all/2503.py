def _color(S, i, j, v):
    if 'vis' not in S:
        return None
    if S['vis'][i][j]:
        return 'green'
    if any(x[1] == i and x[2] == j for x in S['heap']):
        return 'yellow'
    return None


CONFIG = dict(
    num=2503, title='矩阵查询可获得的最大分数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='询问排序 + 堆维护边界，逐轮向外扩展',
    tags=['灵神题单', '堆', '难度分 2196'],
    code='''
class Solution(object):
    def maxPoints(self, grid, queries):

        heap = [[grid[0][0], 0, 0]]
        cnt = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        m = len(grid)
        n = len(grid[0])
        vis = [[False] * n for _ in range(m)]
        res = [0] * len(queries)

        for threshold, index in sorted(zip(queries, range(len(queries)))):
            while heap and heap[0][0] < threshold:
                v, nowx, nowy = heapq.heappop(heap)
                if not vis[nowx][nowy]:
                    vis[nowx][nowy] = True
                    cnt += 1
                    for d in range(4):
                        x = nowx + dx[d]
                        y = nowy + dy[d]
                        if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                            heapq.heappush(heap, [grid[x][y], x, y])
            
            res[index] = cnt

        
        return res
''',
    call='Solution().maxPoints([[1,3,2],[4,5,1]], [4,2,6])',
    expect=[4, 1, 6],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已访问 vis，黄 = 在堆里，蓝框 = 当前弹出的格子）', cell=100, h=240,
             color=_color, cursors=[('nowx', 'nowy', 'blue')]),
        dict(type='heap', var='heap', fmt=lambda x: f'{x[0]}@({x[1]},{x[2]})', label='heap：边界格子（值@坐标）', top_color='pink', h=120),
        dict(type='array', var=lambda S: [str(q) for q in sorted(S['queries'])],
             label='queries 从小到大', cell=80, h=130),
        dict(type='array', var='res', label='res（按原下标放回）', cell=80, h=150),
    ],
    watch=[('threshold', 'threshold', 'orange'), ('cnt', 'cnt', 'green'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue')],
    skip=['x = nowx + dx[d]', 'y = nowy + dy[d]', 'dx = [', 'dy = [', 'm = len', 'n = len', 'vis[nowx][nowy] = True'],
    max_steps=85,
    captions={
        'heap = [[grid': '`heap`：待扩展位置的最小堆（值，x，y），先放起点 `(0, 0)`',
        'cnt = 0': '`cnt`：目前已到达的格子数，==跨询问累计==',
        'vis = ': '`vis[x][y]`：这个位置是否已经到达过',
        'res = [0]': '`res[index]` 放第 `index` 个询问的答案',
        'for threshold, index': '处理阈值 `{threshold}`（原下标 `{index}`）：比它小的询问能到的位置，它也都能到 → 接着上一轮扩',
        'while heap and heap[0][0] < threshold': lambda S, B, r: ('堆空了，没有可扩展的位置' if not S.heap else (
            f'堆顶最小值 `{S.heap[0][0]}` < 阈值 `{S.threshold}` → 这个位置能走' if S.heap[0][0] < S.threshold
            else f'堆顶最小值 `{S.heap[0][0]}` ≥ 阈值 `{S.threshold}`：边界上最小的都走不了 → 本轮结束')),
        'heappop(heap)': '弹出 `({nowx}, {nowy})`，值 `{v}`',
        'if not vis[nowx][nowy]': lambda S, B, r: ('第一次到达 → 处理' if not S.vis[S.nowx][S.nowy] else '这个位置之前已到达（堆里有重复项）→ 跳过'),
        'cnt += 1': '标记 `({nowx}, {nowy})` 已访问，`cnt` = =={cnt}==',
        'for d in range(4)': lambda S, B, r: (f'第 `{S.d}` 个方向，看邻居' if B.get('d') != S.d or S.get('nowx') != B.get('nowx') else '四个方向看完了'),
        'if x >= 0 and': lambda S, B, r: (f'邻居 `({S.x}, {S.y})` 在界内且没到过 → 入堆' if (0 <= S.x < S.m and 0 <= S.y < S.n and not S.vis[S.x][S.y]) else f'邻居 `({S.x}, {S.y})` 越界或已到达 → 跳过'),
        'heappush(heap': '`({x}, {y})` 值 `{grid[x][y]}` 入堆（可能被重复推入，弹出时再用 `vis` 去重）',
        'res[index] = cnt': '这一轮结束：`res[{index}] = {cnt}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='询问从小到大排，每一轮在上一轮的基础上继续往外扩',
        complexity='时间 `O(mn log mn + k log k)`，空间 `O(mn + k)`',
        problem=['矩阵 `grid`，每个询问 `q`：从 `(0,0)` 出发，只经过==值小于 q== 的位置（四方向）',
                 '答案 = 能到达的位置数；本视频：`[[1,3,2],[4,5,1]]`，`[4,2,6]` → `[4,1,6]`'],
        quote='对于两个询问queries[i]以及queries[j]，不妨设queries[i] < queries[j]，那么对于前一个询问，其可到达的位置必然就是对于后一个询问的子集。',
        quote_src='—— yiduobo 题解原文',
        idea=['小询问能到的位置是大询问的子集 → 把询问升序，逐个在上一轮的基础上扩',
              '每轮要找边界上值 < 阈值的位置：用最小堆维护还没到的边界位置',
              '位置可能被多次推入堆，所以弹出时用 `vis` 去重'],
        summary=['时间 `O(mn log mn + k log k)`，空间 `O(mn + k)`',
                 '弹出条件 `heap[0][0] < threshold`，==严格小于==',
                 '`vis` 在弹出时才置 True（入堆时不置），所以要在弹出处判重',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神入堆时就标记，不会重复入堆；yiduobo 弹出时判重，另开 `vis` 数组'],
    ),
)
