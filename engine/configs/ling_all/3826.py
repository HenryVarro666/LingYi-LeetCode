def _pop_front(S, B, r):
    if len(S.q) < 2:
        return '队列里只有一个点，没得比，保留它'
    a, b = S.p.dot(S.q[0]), S.p.dot(S.q[1])
    if a >= b:
        return f'`p·q[0] = {a}` ≥ `p·q[1] = {b}`：队首不比第二个好 → ==弹出==（p 只会越来越往左转，它再也用不上）'
    return f'`p·q[0] = {a}` < `p·q[1] = {b}`：队首已经最优，停止'


def _pop_back(S, B, r):
    if len(S.q) < 2:
        return '队列里不到两个点，不用检查凸性'
    d = (S.q[-1] - S.q[-2]).det(S.v - S.q[-1])
    if d != d or abs(d) == float('inf'):
        return '新点的 y 还是 ∞（上一层没算出来的状态）：叉积无法成立 → 直接保留'
    if d <= 0:
        return f'叉积 `{d}` ≤ 0：队尾点落在凸包内部 → ==弹出=='
    return f'叉积 `{d}` > 0：向上凸出，保留队尾'


def _t(S):
    if 'p' not in S or 's' not in S or '_inner' not in S:
        return '`f[i]`：把前 i 个数分成 K 段的最小分数（×2）；转移 = 在凸包上找 `p·v` 最小的点'
    return (f"`s = pre[i] = {S['s']}`，`p = (−2s, 1) = ({S['p'].x}, {S['p'].y})`；"
            f"队首 `v = ({S['q'][0].x}, {S['q'][0].y})`，点积 `p·v` = =={S['p'].dot(S['q'][0])}==")


CONFIG = dict(
    num=3826, title='最小分割分数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 斜率优化（点积 + 单调队列）',
    tags=['动态规划', '难度分 2345'],
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
    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pre = list(accumulate(nums, initial=0))
        f = [0] + [inf] * n

        for K in range(1, k + 1):
            s = pre[K - 1]
            q = deque([Vec(s, f[K - 1] + s * s - s)])
            for i in range(K, n - (k - K) + 1):  # 其他子数组的长度至少是 1
                s = pre[i]
                p = Vec(-2 * s, 1)
                while len(q) > 1 and p.dot(q[0]) >= p.dot(q[1]):
                    q.popleft()

                v = Vec(s, f[i] + s * s - s)
                f[i] = p.dot(q[0]) + s * s + s

                while len(q) > 1 and (q[-1] - q[-2]).det(v - q[-1]) <= 0:
                    q.pop()
                q.append(v)

        return f[n] // 2
''',
    call='Solution().minPartitionScore([5,1,2,1], 2)',
    expect=25,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80, pointers={'i': 'pink'}),
        dict(type='array', var='pre', label='pre（前缀和）', h=150, cell=80, pointers={'i': 'pink', 'K': 'blue'}),
        dict(type='array', var='f', label='f（分成 K 段的最小分数 ×2）', h=150, cell=80, pointers={'i': 'pink'}),
        dict(type='queue', var='q', label='q 凸包 (x, y)', h=130, fmt=lambda v: f'({v.x},{v.y})'),
        dict(type='text', fn=_t, size=24, h=70),
    ],
    watch=[('K', 'K', 'blue'), ('i', 'i', 'pink'), 's'],
    skip=['n = len', 'pre = list', 'for K in range', 'for i in range', 'self.x = x', 'self.y = y', 'return Vec(self.x', 'return self.x'],
    captions={
        'f = [0]': '`f[i]`：把前 `i` 个数分成 `K` 段的分数（所有值先 ×2）。`f[0]=0`，其余先设为无穷',
        's = pre[K - 1]': '第 `K` 层：最后一段左端点 `j` 至少是 `K-1`。把 `j={K-1}` 对应的点 `v_j = (s_j, f_j + s_j² − s_j)` 放进队列',
        's = pre[i]': '枚举右端点 `i = {i}`，前缀和 `s = {s}`',
        'p = Vec': '把 `f[j] − 2·s_i·s_j + s_j² − s_j` 看成点积：`p = (−2s, 1) = (−2×{s}, 1)`，要让 `p·v_j` ==最小==',
        'p.dot(q[0]) >= p.dot(q[1])': _pop_front,
        'v = Vec': '用 `f[{i}]`（上一层的值）和 `s = {s}` 造出新点 `v = (s, f[i] + s² − s)`，留给之后的 `i` 当转移点',
        'f[i] = p.dot': lambda S, B, r: f"`f[{S.i}] = p·q[0] + s² + s = {S.p.dot(S.q[0])} + {S.s * S.s + S.s}` = =={S.p.dot(S.q[0]) + S.s * S.s + S.s}==（第 `{S.K}` 层的最小分数 ×2）",
        '.det(v - q[-1]) <= 0': _pop_back,
        'q.append(v)': '新点入队，保持下凸包',
        'return f[n]': '答案：`f[n] // 2` = =={ret}==（前面把每段的值乘了 2）',
    },
    cards=dict(
        one_liner='划分型 DP：把「最小化」写成点积，用凸包 + 单调队列找最优决策点',
        complexity='时间 `O((n−k)k)`，空间 `O(n)`',
        problem=['把 `nums` 分成恰好 `k` 段，每段的值是 `sum·(sum+1)/2`，求总分最小',
                 '示例：`nums=[5,1,2,1]`，`k=2` → `25`（`[5]` 和 `[1,2,1]`）',
                 '本视频即示例 1'],
        quote='设向量 v_j = (s_j, f_{K-1,j} + s_j²−s_j)，设向量 p = (−2s_i, 1)，那么我们求的是 min p·v_j。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把值乘 2，避免分数：`f[K][i] = min f[K-1][j] + (s_i − s_j)(s_i − s_j + 1)`',
              '展开后只有一项同时含 `i` 和 `j`：写成点积，`min` 只需看下凸包的点',
              '`−2s_i` 单调递减 → `p` 一路左转，最优点在凸包上右移，用单调队列代替二分'],
        summary=['时间 `O((n−k)k)`，空间 `O(n)`；朴素划分型 DP 是 `O(n²k)`',
                 '每层 `K` 复用同一个 `f`：循环里先用旧的 `f[i]` 造点，再覆盖成新值',
                 '`i` 的范围 `K..n-(k-K)`：前面至少 K 个数，后面至少给剩下的段各 1 个',
                 '答案是 `f[n] // 2`；灵神也把这题归到 §11.8 WQS 二分，本视频演示斜率优化'],
    ),
)
