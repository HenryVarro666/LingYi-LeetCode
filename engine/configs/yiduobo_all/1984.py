CONFIG = dict(
    num=1984, title='学生分数的最小差值', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='排序 + 滑动窗口',
    tags=['灵神题单', '难度分 1306'],
    code='''
class Solution(object):
    def minimumDifference(self, nums, k):

        nums = sorted(nums)
        res = nums[k - 1] - nums[0]
        for index in range(k, len(nums)):
            res = min(res, nums[index] - nums[index - k + 1])
        
        return res
''',
    call='Solution().minimumDifference([9,4,1,7,12,5], 3)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"窗口 `[{S['index']-S['k']+1}, {S['index']}]`：`{S['nums'][S['index']]} − {S['nums'][S['index']-S['k']+1]}` = =={S['nums'][S['index']]-S['nums'][S['index']-S['k']+1]}==，当前最小 `{S['res']}`" if 'index' in S and 'res' in S else '')),
        dict(type='array', var='nums', h=300,
             pointers={'index': 'pink'},
             window=('index-k+1', 'index')),
    ],
    watch=['k', ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums = sorted': '从小到大排序：`{nums}`，答案一定出现在连续的 `k` 个分数里',
        'res = nums[k - 1]': '先算第一个窗口 `[0, {k-1}]`：`{nums[k-1]} − {nums[0]}` → `res = {res}`',
        'for index': lambda S, B, r: (f'窗口右端 `index = {S.index}`，窗口向右滑一格' if S.index != B.get('index') else '`index` 已到末尾，循环结束'),
        'res = min': '新窗口差 `{nums[index]} − {nums[index-k+1]}` = {nums[index]-nums[index-k+1]}，`res = min({B.res}, …) = {res}`',
        'return res': '最小差值 `{res}`',
    },
    cards=dict(
        one_liner='排序后用大小为 k 的窗口，比较头尾分数之差',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选出 `k` 名学生，使最高分与最低分的差值最小',
                 '示例：`nums=[9,4,1,7], k=2` → `2`',
                 '本视频：`[9,4,1,7,12,5], k=3` → `3`'],
        quote='答案必然出现在分数连续的k个学生中，于是可以将数组从小到大进行排序，然后使用一个大小为k的滑动窗口从头开始向后移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['要差值小，选的分数得挨在一起', '排序后，连续的 `k` 个就是一个窗口', '窗口从头滑到尾，用头尾之差更新答案'],
        summary=['时间 `O(n log n)`，`sorted` 另开数组，空间 `O(n)`',
                 '先单独算第一个窗口，再从 `index = k` 开始滑动',
                 '窗口左端是 `index - k + 1`，别写成 `index - k`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
