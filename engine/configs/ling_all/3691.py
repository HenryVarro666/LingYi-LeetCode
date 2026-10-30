SETUP = '''
def heappush_max(h, item):
    h.append(item)
    i = len(h) - 1
    while i > 0:
        p = (i - 1) // 2
        if h[p] < h[i]:
            h[p], h[i] = h[i], h[p]
            i = p
        else:
            break


def heapreplace_max(h, item):
    ret = h[0]
    h[0] = item
    n = len(h)
    i = 0
    while True:
        c = 2 * i + 1
        if c >= n:
            break
        if c + 1 < n and h[c + 1] > h[c]:
            c += 1
        if h[c] > h[i]:
            h[c], h[i] = h[i], h[c]
            i = c
        else:
            break
    return ret
'''


def _M(S):
    a = S.get('nums')
    if not a:
        return [[]]
    n = len(a)
    return [[(max(a[l:r + 1]) - min(a[l:r + 1])) if r >= l else 0 for r in range(n)] for l in range(n)]


def _cell(S, l, r, v):
    h = S.get('h')
    if not h or r < l:
        return None
    n = len(S['nums'])
    rows = {e[1]: e[2] for e in h}
    if l in rows:
        if r == rows[l] - 1:
            return 'yellow' if S.get('_line', 0) in (33, 34, 36) and (S.get('l'), S.get('r')) == (l, rows[l]) else 'blue'
        if r >= rows[l]:
            return 'green'
    return None


def _info(S):
    if 'h' not in S:
        return '矩阵 M[l][r] = 子数组 nums[l..r] 的极差；每行向右递增，不用算出整个矩阵'
    return f"堆里每一行只放「当前最大的没取走的格子」（蓝）；绿 = 已取走；`ans = {S.get('ans', 0)}`，已选 {S.get('_', -1) + 1 if '_' in S else 0}/{S['k']} 个"


CONFIG = dict(
    num=3691, title='最大子数组总值 II', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='最大堆求前 k 大 + ST 表查极差',
    tags=['常用数据结构', '难度分 2469'],
    setup=SETUP,
    code='''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

def op(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return min(a[0], b[0]), max(a[1], b[1])

class ST:
    def __init__(self, a: List[int]):
        n = len(a)
        w = n.bit_length()
        st = [[None] * n for _ in range(w)]
        st[0] = [(x, x) for x in a]
        for i in range(1, w):
            for j in range(n - (1 << i) + 1):
                st[i][j] = op(st[i - 1][j], st[i - 1][j + (1 << (i - 1))])
        self.st = st

    # [l, r) 左闭右开
    def query(self, l: int, r: int) -> int:
        k = (r - l).bit_length() - 1
        mn, mx = op(self.st[k][l], self.st[k][r - (1 << k)])
        return mx - mn

class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        st = ST(nums)

        h = [(st.query(0, n), 0, n)]
        ans = 0
        for _ in range(k):
            d, l, r = h[0]
            if d == 0:  # 堆中剩余元素全是 0
                break
            ans += d
            heapreplace_max(h, (st.query(l, r - 1), l, r - 1))
            if r == n and l + 1 < n:
                heappush_max(h, (st.query(l + 1, n), l + 1, n))
        return ans
''',
    call='Solution().maxTotalValue([4, 2, 5, 1], 5)',
    expect=18,
    views=[
        dict(type='array', var='nums', h=120, cell=80, label='nums'),
        dict(type='grid', var=_M, h=330, cell=70, label='M[l][r] 极差', color=_cell),
        dict(type='heap', var='h', h=150, fmt=lambda x: f'{x[0]}:[{x[1]},{x[2] - 1}]'),
        dict(type='text', fn=_info, size=24, h=90),
    ],
    watch=[('ans', 'ans', 'green'), 'k', 'd', ('已选', lambda S: S['_'] + 1 if '_' in S else 0, 'orange')],
    skip=['for i in range(1, w)', 'for j in range(n - (1 << i) + 1)', 'k = (r - l).bit_length() - 1', 'n = len(a)', 'w = n.bit_length()', 'st = [[None]', 'self.st = st', 'for _ in range(k)', 'n = len(nums)', 'return min(a[0], b[0])', 'mn, mx = op(', 'return mx - mn', 'n = len(a)'],
    captions={
        'st[0] = [(x, x) for x in a]': 'ST 表第 0 层：每个元素自己，`(最小, 最大) = (x, x)`',
        'st[i][j] = op(': '第 `{i}` 层：`st[{i}][{j}]` 管 `{1 << i}` 个元素 `[{j}, {j + (1 << i)})`，由前一层两个小块合并（取最小的最小、最大的最大）',
                'h = [(st.query(0, n), 0, n)]': '堆里先放整段 `[0, {n})` 的极差：它是==所有子数组里最大的==（每列往下递减）',
        'd, l, r = h[0]': '看堆顶：子数组 `[{l}, {r})`，极差 `{d}` 是目前最大的',
        'if d == 0': lambda S, B, r: ('`d = 0`：剩下的全是 0，再选也不增加，提前结束' if S.d == 0 else f'`d = {S.d} > 0`，继续选'),
        'ans += d': '选它：`ans = {B.ans} + {d} = =={ans}==`（第 `{_ + 1}` 个）',
        'heapreplace_max(h, (st.query(l, r - 1), l, r - 1))': '用 ST 表 `O(1)` 查极差（两个可重叠的 2 的幂块覆盖）：同一左端点、右端点缩一格（极差只会不变或变小），顶替堆顶',
        'if r == n and l + 1 < n': lambda S, B, r: (f'刚取的是整段（右端到 `n`）→ 下一个左端点 `{S.l + 1}` 的这一行也该入堆了' if S.r == S.n and S.l + 1 < S.n
                                                   else '这一格不是整段的右端 → 下一行还不用入堆'),
        'heappush_max(h, (st.query(l + 1, n), l + 1, n))': '下一个左端点的整段入堆：它是那一行最大的格子',
        'return ans': '选完 `k = {k}` 个：总值 = =={ans}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='极差矩阵每行递增：合并 n 个有序列表，用最大堆取前 k 大',
        complexity='时间 `O(n log n + k log min(n,k))`，空间 `O(n log n)`',
        problem=['从 `nums` 里选恰好 `k` 个不同子数组，值 = 最大值 − 最小值',
                 '求总值最大。示例：`[4,2,5,1], k=3` → `12`；本视频：`k=5` → `18`（4+4+4+3+3）',
                 '子数组数量 `O(n²)`，不能全算出来'],
        quote='当左端点固定时，右端点越大，子数组的最小值越小，最大值越大，所以子数组的极差也就越大。所以矩阵 M 每一行都是递增的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`M[l][r]` 表示 `nums[l..r]` 的极差，每行递增、每列递减',
              '前 k 大 = 合并有序列表：堆里放每行当前最大的，弹一个、补它左边的',
              '极差用 ST 表 `O(1)` 查询；写法二让整段按需入堆，一开始堆更小'],
        after=[dict(heading='k 更大时', lines=['方法一的堆做法依赖 `k`，k 很大会超时', '方法二：二分第 k 大的值 + 滑窗 + 单调栈 + Lazy 线段树，复杂度与 k 无关'])],
        summary=['ST 表 `st[i][j]` 保存 `[j, j+2^i)` 的 (最小, 最大)，查询用两块重叠覆盖',
                 '堆元素 `(极差, l, r)`，`r` 是右开端点；弹出后把 `r-1` 放回',
                 '堆顶为 0 说明剩下全是 0，直接 `break`',
                 '视频里的 `heapreplace_max / heappush_max` 是 LeetCode 之外的最大堆写法，已用等价实现替代'],
    ),
)
