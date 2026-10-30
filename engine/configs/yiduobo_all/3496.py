CONFIG = dict(
    num=3496, title='最大化配对删除后的得分', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='总和减去最小的剩余部分',
    tags=[],
    code='''
class Solution(object):
    def maxScore(self, nums):

        n = len(nums)
        if n % 2 == 1:
            mi = min(nums)
        else:
            mi = nums[0] + nums[1]
            for index in range(2, n):
                mi = min(mi, nums[index - 1] + nums[index])
        
        return sum(nums) - mi
''',
    call='Solution().maxScore([3,1,4,1,5,9])',
    expect=19,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前相邻对 index-1, index）', cell=100, h=240,
             pointers={'index': 'pink'},
             window=('index - 1', 'index')),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"剩下的部分和 `mi = {S['mi']}`，得分 = 总和 `{sum(S['nums'])}` − `{S['mi']}` = =={sum(S['nums']) - S['mi']}==" if 'mi' in S else f"总和 `{sum(S['nums'])}`")),
    ],
    watch=['n', ('mi', 'mi', 'orange'), ('index', 'index', 'pink')],
    captions={
        'n % 2 == 1': '`n = {n}`：=={"奇数" if n % 2 == 1 else "偶数"}== 个元素，最后{"剩 1 个" if n % 2 == 1 else "剩相邻的 2 个"}',
        'mi = min(nums)': '奇数个：最后只剩 1 个，让它最小 → `mi = {mi}`',
        'mi = nums[0] + nums[1]': '偶数个：最后剩相邻两个，先取头两个当候选 `mi = {mi}`',
        'for index in range': '从 `index = 2` 起，看每一对相邻元素',
        'mi = min': '相邻对 `{nums[index-1]} + {nums[index]} = {nums[index-1] + nums[index]}`，和之前的 `{B.mi}` 比较，`mi` → =={mi}==',
        'return': '总分 = 全部元素之和 − 剩下的最小部分 = `{sum(nums)} − {mi}` = =={ret}==',
    },
    cards=dict(
        one_liner='删掉的总和最大 = 全部之和 − 剩下的部分最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['整数数组 `nums`，元素多于两个时，可重复选一种操作：删前两个、删后两个、或删首尾各一个',
                 '每次得分是删掉的两个数之和，求最大总得分',
                 '示例：`[3,1,4,1,5,9]` → `19`'],
        quote='当nums中有奇数个元素时，无论怎样执行删除操作，最后nums中都只会剩下唯一一个元素。为了使得删除的元素之和最大，就应该让剩下的元素最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次删 2 个，奇偶性不变：奇数个最后剩 1 个，偶数个最后剩 2 个',
              '剩下的 ==越小==，删掉的和越大：奇数取 `min(nums)`',
              '偶数时剩下的一定是==相邻的两个==，扫一遍找最小相邻和'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：偶数个时剩下的是相邻两个，不是任意两个最小值',
                 '循环从 `index = 2` 开始，`mi` 初值已含第一对',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
