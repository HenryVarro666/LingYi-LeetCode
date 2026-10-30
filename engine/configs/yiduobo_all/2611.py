CONFIG = dict(
    num=2611, title='老鼠和奶酪', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='差值 + 大小为 k 的小顶堆',
    tags=['灵神题单', '难度分 1663'],
    code='''
class Solution(object):
    def miceAndCheese(self, reward1, reward2, k):

        heap = []
        res = 0
        for v1, v2 in zip(reward1, reward2):
            res += v2
            heapq.heappush(heap, v1 - v2)
            if len(heap) > k:
                heapq.heappop(heap)
            
        return res + sum(heap)
''',
    call='Solution().miceAndCheese([5,2,7,1,6,3], [3,6,4,4,1,5], 3)',
    expect=33,
    views=[
        dict(type='array', var='reward1', h=130, label='reward1', color=lambda S, i, v: 'blue'),
        dict(type='array', var='reward2', h=130, label='reward2', color=lambda S, i, v: 'pink'),
        dict(type='heap', var='heap', h=330),
    ],
    watch=['v1', 'v2', 'k', ('res', 'res', 'green')],
    captions={
        'heap = []': '准备一个小顶堆，只留下 ==差值最大的 k 个==',
        'res = 0': '`res` 先累加全部 reward2：假设所有奶酪都给老鼠 2',
        'res += v2': '奶酪先给老鼠 2：`res += {v2}` → {res}',
        'heappush': '若改给老鼠 1，价值差 `v1 - v2 = {v1} - {v2} = {v1 - v2}`，放进堆：{heap}',
        'if len(heap) > k': lambda S, B, r: (f'堆里有 `{len(S.heap)}` 个 > k = {S.k}：多了一个' if len(S.heap) > S.k else f'堆里 `{len(S.heap)}` 个，没超过 k = {S.k}，保留'),
        'heappop': '弹出堆顶（最小的差值）：它不在前 k 大里，这块奶酪仍给老鼠 2 → heap = {heap}',
        'return res': '`res + sum(heap)` = `{res}` + `{sum(heap)}`（前 k 大差值之和）→ =={ret}=='
    },
    max_steps=60,
    cards=dict(
        one_liner='先假设全归老鼠 2，改分给老鼠 1 的代价就是差值，选最大的 k 个',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['奶酪 `i` 老鼠 1 吃得 `reward1[i]`，老鼠 2 吃得 `reward2[i]`',
                 '老鼠 1 恰好吃 `k` 块，求最大总得分',
                 '本视频：`[5,2,7,1,6,3]`、`[3,6,4,4,1,5]`、`k=3` → `33`'],
        quote='先假设所有的东西都归其中一人所有，那么在此基础上就某个物品改成分给另一个人的代价就是这两人对于这个物品的价值之差。',
        quote_src='—— yiduobo 题解原文',
        idea=['所有奶酪归老鼠 2：总分是 `sum(reward2)`',
              '第 `index` 块改给老鼠 1，变化量是 `reward1[index] - reward2[index]`',
              '问题变成：求差值数组的 ==top k 大的和==，用大小为 k 的小顶堆一趟遍历'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '堆超过 k 个就弹出堆顶（最小值），剩下的就是最大的 k 个',
                 '差值可以是负数，k 个名额也必须用满',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神直接排序；这里用堆，k 小时更省'],
    ),
)
