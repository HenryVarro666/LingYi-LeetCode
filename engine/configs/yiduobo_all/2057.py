CONFIG = dict(
    num=2057, title='值相等的最小索引', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历', tags=[],
    code='''
class Solution(object):
    def smallestEqual(self, nums):

        for index in range(len(nums)):
            if index % 10 == nums[index]:
                return index
        
        return -1
''',
    call='Solution().smallestEqual([5,4,3,2,9,8,6,7])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（蓝箭头 = 当前 index）', pointers={'index': 'blue'}, cell=96, h=260,
             color=lambda S, i, v: ('green' if 'index' in S and i == S['index'] and S['index'] % 10 == v else None)),
        dict(type='text', h=110, size=32,
             fn=lambda S: f"`index % 10 = {S['index'] % 10}`，`nums[index] = {S['nums'][S['index']]}`" if 'index' in S else ''),
    ],
    watch=[('index', 'index', 'blue')],
    captions={
        'for index': '检测下标 `index = {index}`',
        'if index % 10': '`index % 10 = {index % 10}` 对比 `nums[index] = {nums[index]}` → {"==相等，答案就是它==" if index % 10 == nums[index] else "不相等，看下一个"}',
        'return index': '返回合法的下标 ==`{ret}`==',
        'return -1': '遍历完都没找到合法下标，答案是 `-1`',
    },
    cards=dict(
        one_liner='一趟遍历，检测 index % 10 是否等于 nums[index]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最小下标 `i`，满足 `i mod 10 == nums[i]`，找不到返回 `-1`',
                 '示例：`[2,1,3,5,2]` → `1`',
                 '本视频：`[5,4,3,2,9,8,6,7]` → `6`'],
        quote='比较基础的题目，只需一趟遍历，检测当前下标index是否满足index % 10 = nums[index]，若等于，那么答案就是index。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `index = 0` 开始往后查，第一个满足的就是最小的',
              '遍历完整个数组都没找到，答案是 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`return -1` 要放在 for 循环外面',
                 '`index % 10` 是下标取余，不是数值取余',
                 '代码为 Python 3 可直接运行，原文未改动（`range` 本身就是 Python 3 写法）'],
    ),
)
