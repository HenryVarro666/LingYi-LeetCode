def _num(x):
    return f'{-x:g}'


CONFIG = dict(
    num=2208, title='将数组和减半的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='大顶堆（存相反数）+ 浮点减半',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1550'],
    code='''
class Solution(object):
    def halveArray(self, nums):

        s = sum(nums)
        target = s / 2.0
        
        heap = []
        for num in nums:
            heapq.heappush(heap, -num)
        
        step = 0
        while s > target:
            step += 1
            max_num = -heapq.heappop(heap)
            max_num /= 2.0
            s -= max_num
            heapq.heappush(heap, -max_num)
        
        return step
''',
    call='Solution().halveArray([3, 8, 20, 5])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前总和 `s` = =={S['s']:g}==，目标 `target` = {S['target']:g}：`s` 降到 `target` 以下就停" if 'target' in S else '先算出总和 `s` 和目标 `target`'), size=26, h=60),
        dict(type='heap', var='heap', label='heap：存的是相反数，最左 = 堆顶 = 最小相反数 = 最大的数', top_color='orange', fmt=lambda x: f'{x:g}', h=250),
        dict(type='text', fn=lambda S: (f"本轮：取出最大的数 `{S['max_num'] * 2:g}`，减半成 `{S['max_num']:g}`，总和少了 {S['max_num']:g}" if 'max_num' in S and 'step' in S and S['step'] > 0 else ''), size=24, h=60),
    ],
    watch=[('step', lambda S: S.get('step'), 'green'), ('s', lambda S: S.get('s'), 'orange'), ('target', lambda S: S.get('target'), 'blue')],
    captions={
        's = sum(nums)': '先求原数组总和 `s` = =={s}==',
        'target = s / 2.0': '目标：总和降到 `{target}` 以下，即至少减掉一半',
        'heap = []': '`heapq` 是小顶堆，存==相反数==当大顶堆用',
        'heapq.heappush(heap, -num)': '`{num}` 以 `-{num}` 入堆',
        'step = 0': '`step` 记操作次数',
        'while s > target': lambda S, B, r: (f'`s = {S.s:g} > target = {S.target:g}`：还没减掉一半，继续' if S.s > S.target
                                            else f'`s = {S.s:g} <= target = {S.target:g}`：已经减掉至少一半，结束'),
        'step += 1': '又要操作一次：`step` = =={step}==',
        'max_num = -heapq.heappop(heap)': '堆顶取反 = 当前==最大==的数 `{max_num}`：减它能让总和降得最多',
        'max_num /= 2.0': '把它减半，减掉的量就是 `{max_num}`（减半后剩下的和减掉的一样多）',
        's -= max_num': '总和 `s` 减去 `{max_num}`，变成 =={s}==',
        'heapq.heappush(heap, -max_num)': '减半后的数 `{max_num}` 还可能再被选，放回堆里',
        'return step': '返回 =={ret}==',
    },
    skip=['for num in nums'],
    max_steps=70,
    cards=dict(
        one_liner='总和要降得快，每一轮就把最大的数减半',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选数组里任意一个数，把它==减半==（可以得到小数）',
                 '问总和==至少减少一半==最少要几次操作',
                 '本视频：`nums = [3,8,20,5]`，总和 36，答案 `3`'],
        quote='为了尽快使得总和减下来，因此每一轮都应该将数组中最大的数减半，因此可以维护一个堆，其中堆顶元素为当前数组中的最大值。',
        quote_src='—— yiduobo 题解',
        idea=['贪心：减半能减掉这个数的一半，所以==选最大的数==，总和降得最多',
              '每轮：弹出堆顶、减半、把减半后的数放回堆，直到总和 `s` 不超过 `target`',
              '操作次数不会超过 `n`：把每个数各减半一次，总和就已经减半了，所以复杂度 `O(n log n)`'],
        summary=['最多 `n` 轮，每轮堆操作 `O(log n)`，总 `O(n log n)`',
                 '原文为 Python 2 写法：`s / 2.0`、`/ 2.0` 本来就是浮点除法，Python 3 下无需修改',
                 '易错：`heapq` 是小顶堆，存相反数；弹出后记得取反',
                 '浮点数可以通过本题；想避免误差可以像灵神那样整体乘 `2^20` 用整数做'],
    ),
)
