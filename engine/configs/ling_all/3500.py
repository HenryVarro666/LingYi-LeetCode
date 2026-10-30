def _pts(S):
    q = S.get('q')
    pts = [(v.x, v.y) for v in q] if q is not None else []
    return pts


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '凸包点 v_j = (s[j], f[j])：蓝 = 队首（当前最优），粉 = 新点', 22, T['muted'], bold=True)
    pts = _pts(S)
    line = S.get('_line', 0)
    new = None
    if line >= 33 and 'p' in S and hasattr(S['p'], 'x'):
        new = (S['p'].x, S['p'].y)
    allp = pts + ([new] if new and new not in pts else [])
    if not allp:
        return
    px0, px1 = x0 + 90, x1 - 50
    py0, py1 = y0 + 70, y1 - 60
    xs = [a for a, _ in allp] + [TOT]
    ys = [b for _, b in allp]
    xmin, xmax = 0, max(xs)
    ymin, ymax = min(ys + [0]), max(ys)
    if ymax == ymin:
        ymax = ymin + 1

    def X(v):
        return px0 + (v - xmin) / (xmax - xmin) * (px1 - px0)

    def Y(v):
        return py1 - (v - ymin) / (ymax - ymin) * (py1 - py0)

    cv.line([(px0, py1), (px1, py1)], T['border'], 2)
    cv.line([(px0, py0 - 10), (px0, py1)], T['border'], 2)
    cv.text((px1, py1 + 8), 's[j]（cost 前缀和）', 18, T['dim'], anchor='ra')
    cv.text((px0 + 8, py0 - 22), 'f[j]', 18, T['dim'], anchor='la')
    if len(pts) > 1:
        cv.line([(X(a), Y(b)) for a, b in pts], T['cyan'], 3)
    if new and new not in pts:
        a, b = new
        cv.rect((X(a) - 11, Y(b) - 11, X(a) + 11, Y(b) + 11), outline=T['pink'], width=4, r=11)
        cv.text((X(a), Y(b) - 18), f'({a},{b})', 20, T['pink'], anchor='mb', bold=True)
    for k, (a, b) in enumerate(pts):
        c = T['blue'] if k == 0 else T['text']
        cv.rect((X(a) - 9, Y(b) - 9, X(a) + 9, Y(b) + 9), fill=c, r=9)
        cv.text((X(a), Y(b) + 16), f'({a},{b})', 20, c, anchor='mt', bold=True)


def _msg(S):
    line = S.get('_line', 0)
    if 'sum_num' not in S or 'p' not in S or not hasattr(S['p'], 'x'):
        return '`f[i+1] = sumNum·s[i+1] + k·s[n] + min_j ( f[j] − (sumNum + k)·s[j] )`'
    if line <= 31:
        return f'`p = (−sumNum − k, 1) = ({S["p"].x}, 1)`，求 `min p·v_j`'
    return f'新点 `v = (s[i+1], f[i+1]) = ({S["p"].x}, {S["p"].y})`，`f[i+1] = {S["p"].y}`'


NUMS = [4, 8, 5, 1]
COST = [7, 2, 8, 4]
TOT = sum(COST)

CONFIG = dict(
    num=3500, title='将数组分割为子数组的最小代价', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='式子变形 + 斜率优化（下凸包 + 双端队列）',
    tags=['灵神题单·动态规划', '难度分 2569'],
    code='''
class Vec:
    __slots__ = 'x', 'y'

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, b: "Vec") -> "Vec":
        return Vec(self.x - b.x, self.y - b.y)

    def det(self, b: "Vec") -> int:
        return self.x * b.y - self.y * b.x

    def dot(self, b: "Vec") -> int:
        return self.x * b.x + self.y * b.y

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        total_cost = sum(cost)

        q = deque([Vec(0, 0)])
        sum_num = sum_cost = 0
        for x, c in zip(nums, cost):
            sum_num += x
            sum_cost += c

            p = Vec(-sum_num - k, 1)
            while len(q) > 1 and p.dot(q[0]) >= p.dot(q[1]):
                q.popleft()

            # 一边算 DP 一边构建下凸包
            p = Vec(sum_cost, p.dot(q[0]) + sum_num * sum_cost + k * total_cost)
            while len(q) > 1 and (q[-1] - q[-2]).det(p - q[-1]) <= 0:
                q.pop()
            q.append(p)

        return q[-1].y
''',
    call='Solution().minimumCost([4,8,5,1], [7,2,8,4], 1)',
    expect=309,
    skip=list(range(1, 16)) + [ 'total_cost = sum', 'q = deque', 'sum_num = sum_cost = 0'],
    views=[
        dict(type='text', fn=_msg, size=24, h=60),
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='nums', label='nums', h=95, cell=70, pointers={}),
        dict(type='array', var='cost', label='cost', h=95, cell=70),
    ],
    watch=[('sum_num', 'sum_num', 'blue'), ('sum_cost', 'sum_cost', 'pink'), ('len(q)', 'len(q)'), ('k', 'k')],
    captions={
        'total_cost = sum': '`s[n]` = cost 总和 = `{total_cost}`',
        'sum_num += x': '`sum_num` 是 nums 前缀和（含 x）：{sum_num}',
        'sum_cost += c': '`sum_cost` 是 cost 前缀和 `s[i+1]` = {sum_cost}',
        'p = Vec(-sum_num - k, 1)': '构造 `p = (−sumNum − k, 1)`：`min_j p·v_j` 就是 `f[j] − (sumNum+k)·s[j]` 的最小值',
        'while len(q) > 1 and p.dot': lambda S, B, r: (f'`p·q[0] = {S.p.dot(S.q[0])}` ≥ `p·q[1] = {S.p.dot(S.q[1])}`：队首不如第二个点 → ==弹出队首==（p 的方向单调，之后更不会用到它）'
                                                      if len(S.q) > 1 and S.p.dot(S.q[0]) >= S.p.dot(S.q[1]) else
                                                      '队首已经是投影最小的点（或只剩一个）→ 最优转移 = `q[0]`'),
        'p = Vec(sum_cost': '`f[i+1] = sumNum·s[i+1] + k·s[n] + p·q[0]` = =={p.dot(q[0]) + sum_num * sum_cost + k * total_cost}==，新点 `(s[i+1], f[i+1]) = ({sum_cost}, {p.dot(q[0]) + sum_num * sum_cost + k * total_cost})`',
        'while len(q) > 1 and (q[-1]': lambda S, B, r: ('`det((q[-1]−q[-2]), (p−q[-1])) ≤ 0`：新点让队尾不再是下凸 → ==弹出队尾=='
                                                       if len(S.q) > 1 and (S.q[-1] - S.q[-2]).det(S.p - S.q[-1]) <= 0 else
                                                       '拐弯方向是逆时针（det > 0）→ 仍是下凸，停止弹出'),
        'q.popleft()': '队首出队，下一个点成为新的最优候选',
        'q.pop()': '队尾出队：它在新点和前一个点连线的上方，不可能是最小',
        'q.append(p)': '新点加入凸包队尾：`len(q) = {len(q)}`',
        'return q[-1].y': '最后一个点的 `f` 就是 `f[n]` = =={ret}==',
    },
    cards=dict(
        one_liner='把 k·i 的系数拆成后缀和，转移变成点积，用下凸包 + 队列 O(n)',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干子数组，第 `i` 个子数组 `[l, r]` 代价 `(sum(nums[0..r]) + k·i) × sum(cost[l..r])`',
                 '求最小总代价',
                 '示例：`nums=[3,1,4], cost=[4,6,6], k=1` → `110`；本视频用 `[4,8,5,1]`、`cost=[7,2,8,4]`、`k=1`'],
        quote='换句话说，我们可以跨越时空，把未来要计算的内容，放到现在计算！式子中的 i·(s[r+1]−s[l]) 可以替换成 s[n]−s[l]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `A+2B+3C` 拆成 `(A+B+C)+(B+C)+C`，去掉序号 `i`：转移 `f[i+1] = min f[j] + sumNum·(s[i+1]−s[j]) + k·(s[n]−s[j])`',
              '提出与 `j` 无关的量，剩 `f[j] − (sumNum+k)·s[j]` = 点积 `p·v_j`，`v_j = (s[j], f[j])`',
              '只有下凸包上的点有用；`s[j]` 递增免排序，`p` 方向单调 → 双端队列'],
        summary=['时间 `O(n)`，空间 `O(n)`（`O(n^2)` 的方法一是直接枚举 `j`）',
                 '易错：`det ≤ 0` 才弹队尾；先弹队首求出 `f`，再用新点维护凸包',
                 '题解还给了 `O(n^2)` 划分型 DP（方法一）和 Abel 求和公式的证明',
                 '同类题：3494. 酿造药水需要的最少总时间（同样的凸包优化）'],
    ),
)
