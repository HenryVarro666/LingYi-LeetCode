ORIG = [[1, 3, 2], [4, 5, 1]]


def _heap_cells(S):
    return {(x[1], x[2]) for x in (S.get('h') or [])}


def _color(S, i, j, v):
    if 'h' not in S:
        return None
    if (i, j) in _heap_cells(S):
        return 'yellow'
    if S['grid'][i][j] == 0:
        return 'green'
    return None


CONFIG = dict(
    num=2503, title='矩阵查询可获得的最大分数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线询问 + 最小堆（Prim 式向外扩张）',
    tags=['灵神题单', '堆', '难度分 2196'],
    code='''
class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        m, n = len(grid), len(grid[0])
        ans = [0] * len(queries)
        h = [(grid[0][0], 0, 0)]
        grid[0][0] = 0  # 充当 vis 数组的作用
        cnt = 0
        # 查询的下标按照查询值从小到大排序，方便离线
        for qi, q in sorted(enumerate(queries), key=lambda p: p[1]):
            while h and h[0][0] < q:
                cnt += 1
                _, i, j = heappop(h)
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):  # 枚举周围四个格子
                    if 0 <= x < m and 0 <= y < n and grid[x][y]:
                        heappush(h, (grid[x][y], x, y))
                        grid[x][y] = 0  # 充当 vis 数组的作用
            ans[qi] = cnt
        return ans
''',
    call='Solution().maxPoints([[1,3,2],[4,5,1]], [4,2,6])',
    expect=[4, 1, 6],
    views=[
        dict(type='grid', var=lambda S: ORIG, label='grid 原值（黄 = 在堆里等待，绿 = 已弹出得分，蓝框 = 刚弹出的格子）', cell=100, h=240,
             color=_color, cursors=[('i', 'j', 'blue')]),
        dict(type='heap', var='h', fmt=lambda x: f'{x[0]}@({x[1]},{x[2]})', label='h：最小堆（值@坐标）', top_color='pink', h=120),
        dict(type='array', var='queries', label='queries（按值从小到大处理；蓝 = 当前）', cell=80, h=210, pointers={'qi': 'blue'}),
        dict(type='array', var='ans', label='ans', cell=80, h=150),
    ],
    watch=[('q', 'q', 'orange'), ('cnt', 'cnt', 'green'), ('i', 'i', 'blue'), ('j', 'j', 'blue')],
    skip=['cnt += 1', 'grid[x][y] = 0'],
    max_steps=80,
    captions={
        'ans = [0]': '`ans[qi]` 存第 `qi` 个询问的答案',
        'h = [(grid': '最小堆 `h` 装「待探索」的格子（值，坐标），先放左上角',
        'grid[0][0] = 0': '`grid` 兼做 `vis`：值改成 0 表示已入堆，不会重复入堆（原值 ≥ 1，所以 0 一定不会和原值混）',
        'cnt = 0': '`cnt`：已弹出的格子数 = 已得分数。==询问从小到大，上一次的结果可以接着用==',
        'for qi, q in sorted': '按询问值从小到大处理第 `{qi}` 个询问 `q = {q}`（离线：打乱顺序，答案按 `qi` 放回）',
        'while h and': lambda S, B, r: ('堆空了，无处可扩' if not S.h else (f'堆顶最小值 `{S.h[0][0]}` < q `{S.q}` → 这格能走，弹出' if S.h[0][0] < S.q
                                       else f'堆顶最小值 `{S.h[0][0]}` ≥ q `{S.q}`：最容易走的格子都走不了 → 此询问扩张结束')),
        '_, i, j = heappop': '弹出 `({i}, {j})`，==得 1 分==（`cnt` = {cnt}），从它向四周扩张',
        'for x, y in': lambda S, B, r: (f'看邻居 `({S.x}, {S.y})`' if (B.get('x'), B.get('y')) != (S.x, S.y) or S.get('i') != B.get('i') else '四个邻居看完了'),
        'if 0 <= x < m': lambda S, B, r: ('邻居在界内且未入堆（`grid` 非 0）→ 入堆' if (0 <= S.x < S.m and 0 <= S.y < S.n and S.grid[S.x][S.y])
                                          else '越界或已入堆过 → 跳过'),
        'heappush(h': '`({x}, {y})` 入堆并把 `grid` 置 0 当作已访问，等 q 够大再走',
        'ans[qi] = cnt': '这个询问弹出的格子总数就是答案：`ans[{qi}] = {cnt}`',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='询问排序后从小到大做，堆里永远先取最小的格子',
        complexity='时间 `O(mn log mn + k log k)`，空间 `O(mn + k)`',
        problem=['矩阵 `grid`，每个询问 `q`：从左上角出发，只能走==值严格小于 q== 的格子（四方向）',
                 '答案 = 能走到的格子数；示例：`[[1,2,3],[2,5,7],[3,5,1]]`，`[5,6,2]` → `[5,8,1]`',
                 '本视频：`[[1,3,2],[4,5,1]]`，`[4,2,6]` → `[4,1,6]`'],
        quote='仍然是离线询问，还可以从左上角出发向外搜索，用最小堆，初始把左上角的元素值及其坐标入堆。对每个询问，不断循环，如果堆顶元素值小于询问值，则弹出堆顶，继续搜索。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['询问从小到大排序（离线）：`q` 越大，能走的区域越大',
              '堆里放已探到、还没走的边界格子；堆顶 < q 就走，并把新邻居入堆',
              '堆顶 ≥ q 说明边界上最小的都走不了，弹出的个数 `cnt` 就是答案'],
        summary=['时间 `O(mn log mn + k log k)`，空间 `O(mn + k)`',
                 '用 `grid` 当 vis：入堆时就置 0，所以不会重复入堆；会改写输入',
                 '弹出条件是 `h[0][0] < q`，==严格小于==',
                 '方法一是离线 + 并查集：格子按值从小到大合并，答案是左上角连通块大小（本视频未演示）'],
    ),
)
