CONFIG = dict(
    num=1920, title='基于排列构建数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 按题意填充',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def buildArray(self, nums):

        res = []
        for index in range(len(nums)):
            res.append(nums[nums[index]])

        return res
''',
    call='Solution().buildArray([0,2,1,5,3,4])',
    expect=[0, 1, 2, 4, 5, 3],
    views=[
        dict(type='text', fn=lambda S: (f"`res[{S['index']}] = nums[nums[{S['index']}]] = nums[{S['nums'][S['index']]}] = =={S['nums'][S['nums'][S['index']]]}==`" if 'index' in S else '')),
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums', h=240),
        dict(type='array', var='res', label='res（答案）', h=240,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('index', 'index', 'blue')],
    captions={
        'res = []': '`res` 保存答案',
        'for index': '遍历下标：`index = {index}`',
        'res.append': '先取 `nums[{index}] = {nums[index]}`，再取 `nums[{nums[index]}] = {nums[nums[index]]}`，追加到 `res`',
        'return res': '`res = {res}`',
    },
    cards=dict(
        one_liner='题目怎么说就怎么做：ans[i] = nums[nums[i]]',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是 `0..n-1` 的排列，构造 `ans[i] = nums[nums[i]]`',
                 '示例：`[0,2,1,5,3,4]` → `[0,1,2,4,5,3]`'],
        quote='比较基础的题目，直接一趟遍历，根据题目要求填充答案数组即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个下标 `index`', '两次取下标：`nums[nums[index]]`，加入答案数组'],
        summary=['时间 `O(n)`，空间 `O(n)`（答案数组）',
                 '这是直接模拟，进阶 `O(1)` 空间需要原地编码',
                 '对比灵神：灵神沿环搬家 + 取反标记，不开新数组'],
    ),
)
