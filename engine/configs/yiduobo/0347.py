CONFIG = dict(
    num=347, title='前 K 个高频元素', difficulty='Medium', category='堆',
    author='yiduobo', technique='哈希表计数 + 大小为 k 的小根堆',
    code='''
import heapq

class Solution(object):
    def topKFrequent(self, nums, k):

        weight_dict = {}
        for num in nums:
            weight_dict[num] = weight_dict.get(num, 0) + 1

        if k == len(weight_dict):
            return list(weight_dict.keys())

        heap = []
        for value, weight in weight_dict.items():
            if len(heap) == k:
                min_weight, min_value = heapq.heappop(heap)
                if min_weight > weight:
                    weight = min_weight
                    value = min_value
            heapq.heappush(heap, [weight, value])

        return [x[1] for x in heap]
''',
    call='Solution().topKFrequent([1, 2, 2, 3, 3, 3, 4], 2)',
    result_fn=sorted,
    expect=[2, 3],
    skip=['for num in nums', 'value = min_value'],
    views=[
        dict(type='array', var='nums', cell=80, index=False),
        dict(type='map', var='weight_dict', label='weight_dict（元素 → 频率）', fmt=lambda k, v: f'{k}: {v}次', h=110),
        dict(type='heap', var='heap', label='heap（小根堆，元素是 [频率, 值]，最多 k 个）',
             fmt=lambda x: f'[{x[0]},{x[1]}]', h=130),
        dict(type='text', fn=lambda S: (f"当前元素 `{S['value']}`，频率 `{S['weight']}`" +
                                        (f"　　弹出的堆顶：`[{S['min_weight']},{S['min_value']}]`" if 'min_weight' in S else ''))
             if 'value' in S else '', size=26),
    ],
    watch=[('k', 'k', 'orange'), ('len(heap)', lambda S: len(S['heap']), 'green'), 'value', 'weight'],
    captions={
        'weight_dict = {}': '第一步：一趟扫描，用 `dict` 统计每个元素出现的频率',
        'weight_dict[num] = weight_dict.get': '`{num}` 的频率 → {weight_dict[num]}',
        'if k == len(weight_dict)': lambda S, B, ret: (f'不同元素有 `{len(S.weight_dict)}` 个 == `k`：全部返回' if S.k == len(S.weight_dict)
                                                       else f'不同元素有 `{len(S.weight_dict)}` 个 ≠ `k = {S.k}`，需要用堆来挑'),
        'heap = []': '第二步：维护一个大小为 `k` 的==小根堆==，key 是频率，==堆顶就是 k 个里频率最小的==',
        'for value, weight in weight_dict.items()': lambda S, B, ret: (
            f'下一个元素 `{S.value}`，频率 `{S.weight}`'
            if 'value' not in B or (B.value, B.weight) != (S.value, S.weight) else '所有元素都处理完了'),
        'if len(heap) == k': lambda S, B, ret: (f'堆里已有 `k = {S.k}` 个：要先拿出堆顶比一比' if len(S.heap) == S.k
                                                 else f'堆里只有 `{len(S.heap)}` 个，不满 `k`，直接放'),
        'min_weight, min_value = heapq.heappop': '弹出堆顶 `[{min_weight}, {min_value}]`：当前 k 个里频率最小的',
        'if min_weight > weight': lambda S, B, ret: (
            f'堆顶频率 `{S.min_weight} > {S.weight}`：当前元素更不常见 → ==把堆顶放回去==' if S.min_weight > S.weight
            else f'堆顶频率 `{S.min_weight} ≤ {S.weight}`：==当前元素替换掉堆顶=='),
        'weight = min_weight': '`weight, value` 换成堆顶的 `[{weight}, {min_value}]`，下面 push 回去',
        'heapq.heappush(heap, [weight, value])': 'push `[{weight}, {value}]`，堆重新调整，堆顶仍是最小频率',
        'return [x[1] for x in heap]': '堆里剩下的 `k` 个就是答案：`{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='只留 k 个：小根堆的堆顶是“守门员”，频率更高的才能挤进来',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['返回数组中出现频率前 `k` 高的元素，可以按任意顺序返回',
                 '进阶：时间复杂度必须优于 `O(n log n)`',
                 '本视频示例：`[1,2,2,3,3,3,4], k = 2` → ==[3,2]==（顺序任意）'],
        quote='由于这里只需要求前k个高频元素，于是很自然就想到了使用堆来解决问题……维护一个大小为k的小根堆，key为元素出现的频率。',
        quote_src='—— yiduobo 题解',
        idea=['一趟扫描统计频率；若不同元素正好 `k` 个，直接全部返回',
              '堆满 `k` 个后，每来一个元素先弹出堆顶：==频率比堆顶大才替换==，否则把堆顶放回',
              '每个元素 `O(log k)`，总共 `O(n log k)`；`k = n` 已在第二步返回，所以优于 `n log n`'],
        summary=['为什么是==小根堆==：堆顶是 k 个里最弱的，新元素只需和它比',
                 '堆元素存 `[频率, 值]`，按频率比较',
                 '“先 pop 再 push” 也可以用 `heapq.heappushpop` 一步完成',
                 '原文为 Python 2 写法：`.keys()` 已改为 `list(...)`，并删去了文档字符串'],
    ),
)
