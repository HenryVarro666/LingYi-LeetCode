CONFIG = dict(
    num=2551, title='将珠子放入背包中', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='相邻和 · 两个堆求 top k',
    tags=['灵神题单', '贪心与思维', '难度分 2042'],
    code='''
class Solution(object):
    def putMarbles(self, weights, k):

        ma_heap = []
        ma = 0
        mi_heap = []
        mi = 0
        for index in range(1, len(weights)):
            s = weights[index] + weights[index - 1]

            heapq.heappush(ma_heap, s)
            ma += s
            if len(ma_heap) >= k:
                ma -= ma_heap[0]
                heapq.heappop(ma_heap)
            
            heapq.heappush(mi_heap, -s)
            mi += s
            if len(mi_heap) >= k:
                mi -= -mi_heap[0]
                heapq.heappop(mi_heap)
        
        return ma - mi
''',
    call='Solution().putMarbles([3,1,5,2,4,1], 3)',
    expect=4,
    views=[
        dict(type='array', var='weights', pointers={'index - 1': 'pink', 'index': 'blue'}, h=200, label='weights（粉 + 蓝 = 当前相邻和 s）'),
        dict(type='heap', var='ma_heap', fmt=lambda x: str(x), h=150, label='ma_heap：小根堆，留下最大的 k-1 个 s'),
        dict(type='heap', var='mi_heap', fmt=lambda x: str(-x), h=150, label='mi_heap：存 -s，堆顶是最大的 s，留下最小的 k-1 个'),
    ],
    watch=['index', 's', ('ma', 'ma', 'orange'), ('mi', 'mi', 'cyan'), ('ma - mi', 'ma - mi', 'green')],
    captions={
        'for index in range': '依次看每一对相邻珠子，切在它们中间',
        's = weights[index]': '相邻和 `s = {weights[index]} + {weights[index-1]}` = =={s}==，切在这里就会同时算上这两个数',
        'heapq.heappush(ma_heap, s)': '`s={s}` 先放进 `ma_heap`（小根堆），堆里现在 `{ma_heap}`',
        'ma += s': '`ma` 先累加 `s`：`ma` → {ma}',
        'if len(ma_heap) >= k': '堆里有 `{len(ma_heap)}` 个，`>= k={k}` 吗？只保留最大的 `k-1` 个，多了就要踢掉最小的',
        'ma -= ma_heap[0]': '堆顶 `{ma_heap[0]}` 是堆里最小的，不在最大的 k-1 个之列 → `ma` 减去它 → {ma}',
        'heapq.heappop(ma_heap)': '把堆顶弹出，`ma_heap` 只剩最大的 `k-1` 个：`{ma_heap}`',
        'heapq.heappush(mi_heap, -s)': '取负号放入 `mi_heap`，这样小根堆的堆顶就是最大的 `s`：`{mi_heap}`',
        'mi += s': '`mi` 先累加 `s`：`mi` → {mi}',
        'if len(mi_heap) >= k': '`{len(mi_heap)}` 个，`>= k={k}` 吗？只保留最小的 `k-1` 个，多了就踢掉最大的',
        'mi -= -mi_heap[0]': '堆顶是 `-{-mi_heap[0]}`，即当前最大的 `s={-mi_heap[0]}` → `mi` 减去它 → {mi}',
        'heapq.heappop(mi_heap)': '弹出最大的 s，`mi_heap` 剩最小的 `k-1` 个（取负）：`{mi_heap}`',
        'return ma - mi': '最大的 k-1 项之和 `{ma}` 减去最小的 k-1 项之和 `{mi}` = =={ret}==',
    },
    cards=dict(
        one_liner='相邻和选最大 k-1 个减最小 k-1 个，用两个堆各维护一边',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['把 `weights` 切成 `k` 个连续的背包，背包价格 = 首 + 尾',
                 '分数 = 所有背包价格之和，求最大分数 − 最小分数',
                 '本视频：`[3,1,5,2,4,1], k=3` → `4`'],
        quote='weights[0]和weights[n - 1]是固定的，而其余的(k - 1) * 2项则是由k - 1组连续下标构成的，那么在这里就可以将原数组weights进行变形，计算相邻项之和形成新的数组s。',
        quote_src='—— yiduobo 题解原文',
        idea=['分数 = 固定的首尾 + 每个切点处的相邻和，首尾在最大最小分数里抵消',
              '最大分数要在 s 里选最大的 `k-1` 项，最小分数选最小的 `k-1` 项',
              '用两个大小为 `k-1` 的堆做 top k：一个小根堆留大的，一个存负数的堆留小的'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '堆大小一到 `k` 就弹出堆顶，所以只保留 `k-1` 个；`ma`、`mi` 同步加减，不必最后再求和',
                 '`mi_heap` 里存的是 `-s`，减回去时写成 `-mi_heap[0]`',
                 '原文在 Python 3 下可直接运行，没有改动；对比灵神：灵神直接排序，yiduobo 用堆做 top k'],
    ),
)
