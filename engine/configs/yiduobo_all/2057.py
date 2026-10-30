NUMS = [4, 3, 2, 1]

CONFIG = dict(
    num=2057, title='值相等的最小索引', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def smallestEqual(self, nums):

        for index in range(len(nums)):
            if index % 10 == nums[index]:
                return index
        
        return -1
''',
    call=f'Solution().smallestEqual({NUMS})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前下标 index）', cell=110, h=210, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i == S['index'] and S['index'] % 10 == v else None),
        dict(type='text', h=100, size=32,
             fn=lambda S: (f"`{S['index']} % 10 = {S['index'] % 10}`，`nums[{S['index']}] = {S['nums'][S['index']]}`"
                           f"  →  {'==相等==' if S['index'] % 10 == S['nums'][S['index']] else '不相等'}") if 'index' in S else ''),
    ],
    watch=[('index', 'index', 'blue')],
    captions={
        'for index in range': '从下标 0 开始，一趟遍历找最小的满足条件的下标',
        'if index % 10 == nums[index]': lambda S, B, r: (
            f'`{S.index} % 10 = {S.index % 10}`，`nums[{S.index}] = {S.nums[S.index]}` → 相等，就是答案'
            if S.index % 10 == S.nums[S.index]
            else f'`{S.index} % 10 = {S.index % 10}` ≠ `nums[{S.index}] = {S.nums[S.index]}` → 不满足，看下一个'),
        'return index': '从小到大第一个满足的下标就是最小的：返回 `{index}`',
        'return -1': '整个数组都没找到 → 返回 `-1`',
    },
    cards=dict(
        one_liner='从小到大扫一遍，第一个满足 i % 10 == nums[i] 的就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回最小的下标 `i`，使得 `i mod 10 == nums[i]`',
                 '不存在则返回 `-1`',
                 '示例：`[4,3,2,1]` → `2`（`2 mod 10 = 2 = nums[2]`）'],
        quote='比较基础的题目，只需一趟遍历，检测当前下标index是否满足index % 10 = nums[index]，若等于，那么答案就是index。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标从小到大枚举，==第一个满足的就是最小的==',
              '找到就立刻返回，不用继续往后看',
              '遍历完都没有，返回 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：返回的是下标 `index`，不是 `nums[index]`',
                 '下标超过 9 之后 `i % 10` 会循环回 0，所以要取模再比',
                 '代码与原文一致，只保留了 Python 3 可运行的写法'],
    ),
)
