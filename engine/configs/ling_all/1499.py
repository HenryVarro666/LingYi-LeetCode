_P = [[1, 3], [2, 0], [3, 6], [5, 10], [6, -10]]


def _row(S, i, j, v):
    if 'x' not in S:
        return None
    return 'pink' if _P[i][0] == S['x'] else None


def _eq(S):
    if 'x' not in S:
        return ''
    best = f"max(yi−xi) = =={S['q'][0][1]}==" if S.get('q') else '队列空，没有 i 可配'
    return f"`yi+yj+|xi−xj|` = `(xj+yj) + (yi−xi)`，当前 `xj+yj = {S['x'] + S['y']}`，{best}"


CONFIG = dict(
    num=1499, title='满足不等式的最大值', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='单调队列（x 递增，y−x 递减）',
    tags=['单调队列', '难度分 2456'],
    code='''
class Solution:
    def findMaxValueOfEquation(self, points: List[List[int]], k: int) -> int:
        ans = -inf
        q = deque()
        for x, y in points:
            while q and q[0][0] < x - k:  # 队首超出范围
                q.popleft()  # 弹它！
            if q:
                ans = max(ans, x + y + q[0][1])  # 加上最大的 yi-xi
            while q and q[-1][1] <= y - x:  # 队尾不如新来的强
                q.pop()  # 弹它！
            q.append((x, y - x))
        return ans
''',
    call='Solution().findMaxValueOfEquation([[1,3],[2,0],[3,6],[5,10],[6,-10]], 1)',
    expect=7,
    views=[
        dict(type='table', var='points', label='points（粉 = 当前点 j）', rows=['p0', 'p1', 'p2', 'p3', 'p4'], cols=['x', 'y'],
             color=_row, cell=70, h=300),
        dict(type='queue', var='q', label='单调队列 q：(x, y−x)，队首 y−x 最大', fmt=lambda t: f'x={t[0]}, {t[1]}', h=130),
        dict(type='text', fn=_eq, h=70),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = -inf': '`ans = -inf`：还没配出任何一对',
        'q = deque()': '队列存 `(x_i, y_i − x_i)`：x 用来判断超出范围，y−x 是要最大化的量',
        'for x, y in points': '枚举 j：`(x, y) = ({x}, {y})`。因为 `x_i < x_j`，绝对值可以直接展开成 `x_j − x_i`',
        'while q and q[0][0] < x - k': lambda S, B, r: (
            f'队首 `x_i = {S.q[0][0]} < {S.x} − {S.k} = {S.x - S.k}`：离得太远，以后更远 → ==超出范围==' if S.q and S.q[0][0] < S.x - S.k
            else ('队列空了，停止' if not S.q else f'队首 `x_i = {S.q[0][0]} ≥ {S.x - S.k}`：还在范围内，停止')),
        'q.popleft()': '队首出队：后面的 `x_j` 只会更大，它永远配不上了',
        'if q:': lambda S, B, r: ('队列里还有候选 i，队首就是 y−x 最大的那个' if S.q else '队列空，没有 i 可以配对，跳过'),
        'ans = max(ans, x + y + q[0][1])': '`(xj+yj) + max(yi−xi)` = `{x + y} + {q[0][1]}` = {x + y + q[0][1]}，`ans` = =={ans}==',
        'while q and q[-1][1] <= y - x': lambda S, B, r: (
            f'队尾 `y−x = {S.q[-1][1]} ≤ {S.y - S.x}`：又老又不强 → ==淘汰==' if S.q and S.q[-1][1] <= S.y - S.x
            else '队尾比新来的强（或队列空）→ 保留，停止'),
        'q.pop()': '队尾出队：新点 x 更大、y−x 不低，以后永远选新点更好',
        'q.append((x, y - x))': '`(x={x}, y−x={y - x})` 入队：队列里 y−x 从队首到队尾==严格递减==',
        'return ans': '最大值 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='老员工的能力必须比新来的强，否则淘汰',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['点按 x 严格递增，求 `yi + yj + |xi − xj|` 的最大值',
                 '限制：`i < j` 且 `|xi − xj| ≤ k`',
                 '本视频：5 个点，`k = 1` → `7`'],
        quote='枚举 j，问题变成计算 y_i − x_i 的最大值，其中 i<j 且 x_i ≥ x_j − k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['化简：`yi + yj + xj − xi = (xj + yj) + (yi − xi)`',
              '枚举 j，只需要范围内 `yi − xi` 的==最大值==',
              '队首 `x_i < x_j − k` 就出队；队尾 `y−x` 不高于新来的也出队，队首即最大值'],
        summary=['时间 `O(n)`：每个点至多入队、出队各一次',
                 '先出队超范围的，再算答案，最后才让自己入队（`i < j`）',
                 '队尾弹出条件用 `<=`：相等时新点 x 更大，更不容易过期',
                 '同类题：239、862、1438'],
    ),
)
