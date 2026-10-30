_P = [[1, 3], [2, 0], [3, 6], [5, 10], [6, -10]]


def _row(S, i, j, v):
    if 'x' not in S:
        return None
    return 'pink' if _P[i][0] == S['x'] else None


def _eq(S):
    if 'x' not in S:
        return ''
    live = S['q'][S['l']:S['r']]
    if not live:
        return f"当前 `x[j] + y[j] = {S['x'] + S['y']}`，窗口里没有 i 可配"
    h = live[0]
    return f"`x[j] + y[j] + y[i] − x[i]` = `{S['x'] + S['y']}` + (`{h[1]} − {h[0]}`) = =={S['x'] + S['y'] + h[1] - h[0]}=="


CONFIG = dict(
    num=1499, title='满足不等式的最大值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='单调双端队列（数组 + 头尾下标）',
    tags=['单调队列', '难度分 2456'],
    code='''
class Solution(object):
    def findMaxValueOfEquation(self, points, k):

        q = []
        l = r = 0
        res = None

        for x, y in points:
            while l < r and x - q[l][0] > k:
                l += 1
            
            if l < r and (res is None or res < x + y + q[l][1] - q[l][0]):
                res = x + y + q[l][1] - q[l][0]
            
            while r > l and y - x >= q[-1][1] - q[-1][0]:
                q.pop()
                r -= 1
            
            q.append([x, y])
            r += 1

        return res
''',
    call='Solution().findMaxValueOfEquation([[1,3],[2,0],[3,6],[5,10],[6,-10]], 1)',
    expect=7,
    views=[
        dict(type='table', var='points', label='points（粉 = 当前点 j）', rows=['p0', 'p1', 'p2', 'p3', 'p4'], cols=['x', 'y'],
             color=_row, cell=70, h=300),
        dict(type='queue', var='q[l:r]', label='队列里有效的 [x, y]（下标 l 到 r−1，队首 y−x 最大）', fmt=lambda t: f'[{t[0]},{t[1]}] y−x={t[1] - t[0]}', h=130),
        dict(type='text', fn=_eq, h=70),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'pink'), ('l', 'l', 'blue'), ('r', 'r', 'orange'), ('res', 'res', 'green')],
    captions={
        'q = []': '`q` 用数组当双端队列：`l` 是队首下标，`r` 是队尾后一格，有效元素在 `q[l:r]`',
        'res = None': '`res = None`：还没有答案',
        'for x, y in points': '固定右端点 j：`(x, y) = ({x}, {y})`，`x[j] + y[j]` 随之固定，只要 `y[i] − x[i]` 最大',
        'while l < r and x - q[l][0] > k': lambda S, B, ret: (
            f'队首 `{S.x} − {S.q[S.l][0]} = {S.x - S.q[S.l][0]} > {S.k}`：越界，后面更远，用不上了' if S.l < S.r and S.x - S.q[S.l][0] > S.k
            else ('队列空了，停止' if S.l >= S.r else f'队首 `{S.x} − {S.q[S.l][0]} = {S.x - S.q[S.l][0]} ≤ {S.k}`：在范围内，停止')),
        'l += 1': '队头出队：`l += 1` → {l}',
        'if l < r and (res is None': lambda S, B, ret: (
            f'队首就是最优的 i：候选值 `{S.x + S.y} + ({S.q[S.l][1]} − {S.q[S.l][0]})` = {S.x + S.y + S.q[S.l][1] - S.q[S.l][0]}，比 `res` 大吗？ → '
            + ('==是，要更新==' if S.res is None or S.res < S.x + S.y + S.q[S.l][1] - S.q[S.l][0] else '不是，不更新')
            if S.l < S.r else '队列空，没有 i 可配，跳过'),
        'res = x + y + q[l][1] - q[l][0]': '`res` 更新为 =={res}==',
        'while r > l and y - x >= q[-1][1] - q[-1][0]': lambda S, B, ret: (
            f'队尾 `y−x = {S.q[-1][1] - S.q[-1][0]} ≤ {S.y - S.x}`：新来的更大，队尾==没有机会==了' if S.r > S.l and S.y - S.x >= S.q[-1][1] - S.q[-1][0]
            else '队尾比新来的大（或队列空）→ 保留，停止'),
        'q.pop()': '队尾弹出',
        'r -= 1': '`r -= 1` → {r}',
        'q.append([x, y])': '新点 `[{x}, {y}]` 加入队尾，队列里 y−x 保持==严格递减==',
        'r += 1': '`r += 1` → {r}',
        'return res': '最大值 =={ret}==',
    },
    max_steps=110,
    skip=['l = r = 0'],
    cards=dict(
        one_liner='y−x 小的点永远排在大的点后面，留不下来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['点已按 x 排好序，求 `y[i] + y[j] + |x[i] − x[j]|` 的最大值',
                 '限制：`i < j` 且 `x[j] − x[i] ≤ k`',
                 '本视频：5 个点，`k = 1` → `7`'],
        quote='若满足p < q且y[p] - x[p] <= y[q] - x[q]，那么此时对于后续的所有q右侧所有的位置j而言，都不可能选择p作为其配对的位置i了',
        quote_src='—— yiduobo 题解原文',
        idea=['`i < j` 时 `x[i] < x[j]`，绝对值直接去掉：`x[j] + y[j] + y[i] − x[i]`',
              '固定 j，只需最大化 `y[i] − x[i]`，i 在 j 前面的一段连续区间里',
              '双端队列：头部清掉越界的，尾部清掉不如新点的，头部就是最优 i'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '头部用 `x - q[l][0] > k` 判越界；尾部用 `>=` 把相等的也弹掉',
                 '`res` 用 `None` 起步，题目保证至少有一对，最后不会返回 None',
                 '用数组 + `l`、`r` 模拟双端队列：头部只动 `l`，所以 `q` 前面会留着已出队的旧数据',
                 '原文本身可直接在 Python 3 运行，未做修改。对比灵神：灵神直接用 `deque` 存 `(x, y−x)`'],
    ),
)
