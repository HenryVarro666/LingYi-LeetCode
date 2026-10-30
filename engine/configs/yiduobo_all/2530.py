CONFIG = dict(
    num=2530, title='执行 K 次操作后的最大分数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='大顶堆（取负）逐轮取最大',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1386'],
    code='''
class Solution(object):
    def maxKelements(self, nums, k):

        heap = []
        for x in nums:
            heapq.heappush(heap, -x)
        
        res = 0
        for _ in range(k):
            ma = -heapq.heappop(heap)
            res += ma
            if ma % 3 == 0:
                ma //= 3
            else:
                ma = ma // 3 + 1
            
            heapq.heappush(heap, -ma)

        return res
''',
    call='Solution().maxKelements([1,10,3,3,3], 3)',
    expect=17,
    views=[
        dict(type='heap', var='heap', label='heap（存相反数，堆顶 = 最大的数取负）', top_color='yellow', h=140),
        dict(type='text', fn=lambda S: '真实的数：' + ', '.join(str(-x) for x in sorted(S['heap'])) if S.get('heap') else '', size=26, h=60),
        dict(type='text', fn=lambda S: f'得分 `res` = ==`{S["res"]}`==' if 'res' in S else '', size=28, h=60),
    ],
    watch=[('ma', 'ma', 'yellow'), ('res', 'res', 'green')],
    captions={
        'heap = []': '空堆；Python 的 `heapq` 是小顶堆，所以放进去的都是==负数==',
        'heapq.heappush(heap, -x)': '把 `{x}` 取负放进堆：`{-x}`',
        'res = 0': '堆建好了，得分从 0 开始；最小的负数在堆顶',
        'for _ in': lambda S, B, ret: (f'`k` = {S.k} 轮做完了，循环结束' if (S.get('_') is not None and S.get('_') == B.get('_')) else f'开始第 {S["_"] + 1} 轮（共 {S.k} 轮）'),
        'ma = -heapq.heappop': '弹出堆顶取负：当前最大的数是 ==`{ma}`==',
        'res += ma': '得分加上最大值：`res` = `{B.res} + {ma}` = =={res}==',
        'if ma % 3 == 0': lambda S, B, ret: f'`{S.ma} % 3 = {S.ma % 3}`：' + ('能整除，直接 `ma //= 3`' if S.ma % 3 == 0 else '不能整除，向上取整要在整除结果上再加 1'),
        'ma //= 3': '整除：`ma` = ==`{ma}`==',
        'ma = ma // 3 + 1': '向上取整：`{B.ma} // 3 + 1` = ==`{ma}`==',
        'heapq.heappush(heap, -ma)': '变小后的 `{ma}` 取负放回堆里，下一轮重新比大小',
        'return res': '`k` 轮做完，最大得分 = ==`{ret}`==',
    },
    max_steps=70,
    cards=dict(
        one_liner='每轮弹出最大数加分，向上取整除 3 后放回',
        complexity='时间 `O(n log n + k log n)`，空间 `O(n)`',
        problem=['每次选一个 `nums[i]`：分数加 `nums[i]`，再把它换成 `ceil(nums[i]/3)`',
                 '恰好操作 `k` 次，求最大分数',
                 '本视频：`nums=[1,10,3,3,3], k=3` → ==17=='],
        quote='题目中的各个整数间互不影响，因此只需每一轮都选择当前数组中的最大值进行操作，一共选择k轮就行了。',
        quote_src='—— yiduobo 题解',
        idea=['各个数互不影响，所以每轮都挑当前==最大值==就是最优',
              '需要反复取最大值，用堆；`heapq` 是小顶堆，存相反数',
              '除以 3 要向上取整：能整除就 `//3`，否则 `//3 + 1`'],
        summary=['时间 `O((n+k) log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`ma /= 3` 与 `ma / 3 + 1` 已改为 `//=` 和 `//`',
                 '易错：堆里是负数，取出要再取负；向上取整不能直接 `//3`',
                 '同类题：1962. 移除石子使总数最小'],
    ),
)
