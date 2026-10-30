NUMS = [1, 3, 2, 4, 9]

CONFIG = dict(
    num=3423, title='循环数组中相邻元素的最大差值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='下标取模 (index+1) % n',
    code='''
class Solution(object):
    def maxAdjacentDistance(self, nums):
        
        res = 0
        for index in range(len(nums)):
            res = max(res, abs(nums[index] - nums[(index + 1) % len(nums)]))
            
        return res
''',
    call=f'Solution().maxAdjacentDistance({NUMS})',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = index，粉 = (index+1) % n，循环相邻）', cell=90, h=240,
             pointers={'index': 'blue', '(index + 1) % len(nums)': 'pink'},
             pointer_labels={'index': 'i', '(index + 1) % len(nums)': 'next'}),
        dict(type='text', fn=lambda S: (f"`|nums[{S['index']}] − nums[{(S['index'] + 1) % len(S['nums'])}]|` = `|{S['nums'][S['index']]} − {S['nums'][(S['index'] + 1) % len(S['nums'])]}|` = =={abs(S['nums'][S['index']] - S['nums'][(S['index'] + 1) % len(S['nums'])])}==") if 'index' in S else '', size=30),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最大绝对差，差值都 ≥ 0，初始 `0` 就够',
        'for index in range': lambda S, B, r: (f'枚举 `index = {S.index}`，它的下一个元素是 `nums[({S.index}+1) % {len(S.nums)}]`' if S.get('index') != B.get('index') or 'index' not in B else '每个下标都算过了'),
        'res = max': lambda S, B, r: (f'`|{S.nums[S.index]} − {S.nums[(S.index + 1) % len(S.nums)]}| = {abs(S.nums[S.index] - S.nums[(S.index + 1) % len(S.nums)])}`，`res = max({B.res}, {abs(S.nums[S.index] - S.nums[(S.index + 1) % len(S.nums)])}) = {S.res}`'
                                       + ('（==最后一个元素的下一个绕回了 `nums[0]`==）' if S.index == len(S.nums) - 1 else '')),
        'return res': '所有相邻对（含首尾）都比较过，返回 `{res}`',
    },
    cards=dict(
        one_liner='下一个元素的下标取模：(index + 1) % n，最后一个自然绕回首项',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['循环数组 `nums`，==第一个和最后一个元素也算相邻==',
                 '求相邻元素绝对差的最大值',
                 '示例：`[1,2,4]` → `3`',
                 '本视频：`[1,3,2,4,9]` → `8`（`|9-1|`，答案出在首尾）'],
        quote='对于下标在index的元素，其下一个元素的下标为(index + 1) % len(nums)，那么只需遍历数组，对于当前遍历到的元素nums[index]，计算其与nums[(index + 1) % len(nums)]的差的绝对值并更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通情况 `index + 1` 就是下一个；到了最后一个，取模变成 `0`',
              '一个循环、一个表达式，不需要特判首尾',
              '每次用 `abs` 算差，再和 `res` 取 `max`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：差要取绝对值；别漏掉最后一个与第一个的比较',
                 '原文为 Python 2 风格，代码无需修改，Python 3 直接可运行',
                 '对比灵神：灵神把首项补到末尾再 `pairwise`；这里用取模下标'],
    ),
)
