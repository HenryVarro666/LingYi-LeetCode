CONFIG = dict(
    num=3478, title='选出和最大的 K 个元素', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 最小堆维护前 k 大',
    tags=['堆（优先队列）', '难度分 1753'],
    code='''
class Solution:
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        a = sorted((x, y, i) for i, (x, y) in enumerate(zip(nums1, nums2)))
        n = len(a)
        ans = [0] * n
        h = []
        s = 0
        for i, (x, y, idx) in enumerate(a):
            ans[idx] = ans[a[i - 1][2]] if i and x == a[i - 1][0] else s
            s += y
            heappush(h, y)
            if len(h) > k:
                s -= heappop(h)
        return ans
''',
    call='Solution().findMaxSum([4,2,2,5,3], [10,20,30,40,50], 2)',
    expect=[80, 0, 0, 80, 50],
    views=[
        dict(type='text', fn=lambda S: (f"排序后第 {S['i']} 项：nums1 = {S['x']}，nums2 = {S['y']}，原下标 {S['idx']}；堆内和 `s` = =={S['s']}==" if 'idx' in S else '先按 nums1 排序成三元组 (x, y, 下标)')),
        dict(type='array', var='[f"{x},{y},{j}" for x, y, j in a]', pointers={'i': 'blue'}, cell=130, h=220, label='a = 排序后的 (nums1, nums2, 原下标)'),
        dict(type='heap', var='h', fmt=lambda x: str(x), h=150, label='h：最小堆，只留前 k 大的 nums2'),
        dict(type='array', var='ans', h=150, label='ans（按原下标）'),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'yellow'), ('k', 'k', 'purple')],
    captions={
        'a = sorted': '按 `nums1` 排序：比 `nums1[i]` 小的数都排在它左边，==前缀即候选集==',
        'ans[idx] =': lambda S, B, r: (f'`nums1 = {S.x}` 与上一项相同 → 答案同上一项：`ans[{S.idx}] = {S.ans[S.idx]}`' if S.i and S.x == S.a[S.i-1][0]
                                       else f'前面都是更小的数，堆里前 k 大之和 `s = {S.s}` 就是答案：`ans[{S.idx}] = {S.ans[S.idx]}`'),
        's += y': '先把 `{y}` 计入和：`s = {B.s} + {y} = {s}`',
        'heappush': '`{y}` 入堆（最小堆，堆顶是最小的）',
        'if len(h) > k': lambda S, B, r: (f'堆大小 `{len(S.h)}` > k = {S.k} → 成立，要弹出最小值' if len(S.h) > S.k else f'堆大小 `{len(S.h)}` ≤ k = {S.k}，不用弹'),
        's -= heappop': '弹出堆顶（这 k+1 个数的最小值）并从和里减掉：`s = {s}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后做前缀，最小堆维护前 k 大之和',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对每个 `i`，在所有 `nums1[j] < nums1[i]` 的 `j` 里，选至多 `k` 个最大的 `nums2[j]` 求和',
                 '示例：`nums1=[4,2,1,5,3]`，`nums2=[10,20,30,40,50]`，`k=2` → `[80,30,0,80,50]`',
                 '本视频：`[4,2,2,5,3]`，同样的 nums2，`k=2`，含相同的 nums1'],
        quote='排序后，小于 nums1[i] 的数，都在 nums1[i] 左边，这样方便我们增量地处理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先排序，把「小于」变成「左边的前缀」',
              '遍历时用最小堆维护 nums2 的前 `k` 大，变量 `s` 记堆内之和',
              '堆超过 `k` 个就弹出堆顶（这 `k+1` 个数的最小值）'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：`nums1` 相同的元素互不「小于」，答案必须相同，所以先取答案、再入堆',
                 '本视频用写法二（判断与前一项是否相等）；写法一是分组循环，通用；还有 heappushpop 的更快写法',
                 '前置题：703. 数据流中的第 K 大元素'],
    ),
)
