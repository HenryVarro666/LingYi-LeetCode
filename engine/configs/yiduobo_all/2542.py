def _cur(S):
    return f"{S['x']}·{S['y']}" if 'x' in S and 'y' in S else None


CONFIG = dict(
    num=2542, title='最大子序列的分数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='nums2 降序扫描 + 小顶堆维护 top k',
    tags=['灵神题单', '堆', '难度分 2056'],
    code='''
class Solution(object):
    def maxScore(self, nums1, nums2, k):

        heap = []
        res = 0
        s = 0
        for x, y in sorted(zip(nums1, nums2), key=lambda d:d[1], reverse=True):
            heapq.heappush(heap, x)
            s += x
            if len(heap) > k:
                s -= heap[0]
                heapq.heappop(heap)
            
            if len(heap) == k:
                res = max(res, y * s)
        
        return res
''',
    call='Solution().maxScore([4,2,3,1,5,2], [1,6,3,5,2,4], 3)',
    expect=21,
    views=[
        dict(type='array', var=lambda S: [f'{a}·{b}' for a, b in sorted(zip(S['nums1'], S['nums2']), key=lambda d: d[1], reverse=True)],
             label='按 nums2 从大到小的 (nums1·nums2)；黄 = 当前员工', cell=100, h=170,
             color=lambda S, i, v: 'yellow' if v == _cur(S) else None),
        dict(type='heap', var='heap', label='heap：小顶堆，候选集里 nums1 的 top k', top_color='pink', h=200),
        dict(type='text', fn=lambda S: (f"候选集 top k 之和 `s = {S['s']}`，乘最小值 `y = {S['y']}` = =={S['s']*S['y']}==" if 'y' in S and len(S['heap']) == S['k'] and S['_line'] == 14 else ''), h=60),
    ],
    watch=[('s', 's', 'blue'), ('x', 'x', 'orange'), ('y', 'y', 'cyan'), ('len(heap)', lambda S: len(S['heap']), 'pink'), ('res', 'res', 'green')],
    captions={
        'heap = []': '`heap`：小顶堆，保存当前候选集里 nums1 最大的 `k` 个',
        5: '`res` 记录目前最大的分数',
        6: '`s` 是堆里所有数之和，边进边出时顺手维护',
        'for x, y in sorted': '扫到 `(nums1 = {x}, nums2 = {y})`：它的 nums2 就是阈值，之前的人 nums2 都 ≥ 它，候选集又多一个 `{x}`',
        'heappush(heap, x)': '把 `{x}` 加进堆，堆大小 `{len(heap)}`',
        's += x': '`s` 加上 `{x}` → {s}',
        'if len(heap) > k': lambda S, B, r: (f'堆里有 `{len(S.heap)}` 个，超过 `k = {S.k}` → 要踢掉最小的' if len(S.heap) > S.k
                                             else f'堆里 `{len(S.heap)}` 个，没超过 `k = {S.k}`'),
        's -= heap[0]': '踢掉堆顶最小的 `{B.heap[0]}`：`s` 减去它 → =={s}==',
        'heappop(heap)': '堆顶弹出，堆里重新只剩 top `k`',
        'if len(heap) == k': lambda S, B, r: (f'凑够 `k = {S.k}` 个了，可以算分数' if len(S.heap) == S.k
                                              else f'才 `{len(S.heap)}` 个，不够 `k = {S.k}`，先不算'),
        'res = max': '`res = max({B.res}, {y} × {s})` = =={res}==',
        'return res': '最大分数 `{res}`',
    },
    cards=dict(
        one_liner='乘号右边决定候选集，加号左边是 top k：降序扫 + 小顶堆',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选 `k` 个下标，分数 = ==nums1 之和 × nums2 最小值==，求最大分数',
                 '示例：`[1,3,3,2]`、`[2,1,3,4]`、`k=3` → `12`',
                 '本视频：`[4,2,3,1,5,2]`、`[1,6,3,5,2,4]`、`k=3`'],
        quote='将nums2中的数从大到小进行排序，然后一趟遍历逐个选取作为最小值的部分中的最小值……候选集就相当于在上一轮候选集的基础上额外添加了nums1[index]',
        quote_src='—— yiduobo 题解原文',
        idea=['加法部分：从 nums1 子集里取 top k，子集只增不减，所以==小顶堆==能一路迭代',
              '乘法部分：min 决定候选集，nums2 降序 → 候选集稳定扩展',
              '每步：入堆、超过 k 就弹堆顶，凑够 k 个再用 `y * s` 更新答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先入堆再弹：新元素可能立刻被弹出，也没关系',
                 '`len(heap) == k` 才能更新答案，否则不足 k 个',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神先放前 k 个再用 heapreplace；这里统一「先入再弹」'],
    ),
)
