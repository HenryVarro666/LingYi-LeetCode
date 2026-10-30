CONFIG = dict(
    num=3066, title='超过阈值的最少操作数 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='小顶堆，每轮弹两次再压入',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1400'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):

        heapq.heapify(nums)
        res = 0

        while nums[0] < k:
            x = heapq.heappop(nums)
            y = heapq.heappop(nums)
            heapq.heappush(nums, x * 2 + y)
            res += 1

        return res
''',
    call='Solution().minOperations([2,11,10,1,3], 10)',
    expect=2,
    views=[
        dict(type='heap', var='nums', label='nums（小顶堆）', top_color='yellow', h=160),
        dict(type='text', fn=lambda S: f'最小值 `{S["nums"][0]}` {"<" if S["nums"][0] < S["k"] else ">="} `k = {S["k"]}`' if S.get('nums') and S['_line'] in (5, 7) else '', size=28, h=60),
        dict(type='text', fn=lambda S: f'本轮：`x = {S["x"]}`，`y = {S["y"]}`，新数 `x*2 + y` = =={S["x"] * 2 + S["y"]}==' if 'y' in S else '', size=26, h=60),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'blue'), ('res', 'res', 'green')],
    captions={
        'heapq.heapify': '把 `nums` 原地堆化成小顶堆，堆顶 ==`{nums[0]}`== 是最小值',
        'res = 0': '`res` 记录轮数',
        'while nums[0] < k': lambda S, B, ret: (f'堆顶 `{S["nums"][0]}` < `{S.k}`，还有数不够大，再来一轮' if S['nums'][0] < S.k else f'堆顶 `{S["nums"][0]}` >= `{S.k}`，最小的都够大，==全部达标==，结束'),
        'x = heapq.heappop': '第一次弹出：最小值 `x` = ==`{x}`==',
        'y = heapq.heappop': '第二次弹出：次小值 `y` = ==`{y}`==',
        'heapq.heappush': '把 `x*2 + y` = `{x}*2 + {y}` = ==`{x * 2 + y}`== 放回堆',
        'res += 1': '一轮结束：`res` = ==`{res}`==',
        'return res': '堆顶已 >= `k`，共 ==`{ret}`== 轮',
    },
    max_steps=60,
    cards=dict(
        one_liner='每轮弹出最小、次小两个数，合并后放回堆',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次选最小的两个数 `x ≤ y`，删掉并加入 `x*2 + y`',
                 '求让所有数都 `>= k` 的最少操作次数',
                 '本视频：`nums=[2,11,10,1,3], k=10` → ==2=='],
        quote='题目每次要求从数组中选出最小的两个数进行操作，是动态的最小值问题，可以使用堆来处理。',
        quote_src='—— yiduobo 题解',
        idea=['“每次取最小两个数”是动态的最小值问题 → 堆',
              '每轮弹出两次堆顶，得到最小值 `x` 和次小值 `y`',
              '把 `x*2 + y` 放回堆，重复到堆顶 `>= k`，轮数就是答案'],
        summary=['时间 `O(n log n)`：每轮堆里少一个数，最多 `n` 轮',
                 '空间：直接把 `nums` 当堆，额外空间 `O(1)`',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '易错：`x` 是最小、`y` 是次小，公式是 `x*2 + y`，不要写反'],
    ),
)
