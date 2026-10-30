CONFIG = dict(
    num=2089, title='找出数组排序后的目标下标', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序 + 一趟遍历',
    code='''
class Solution(object):
    def targetIndices(self, nums, target):

        res = []
        for index, num in enumerate(sorted(nums)):
            if num == target:
                res.append(index)
        
        return res
''',
    call='Solution().targetIndices([1,2,5,2,3,2], 2)',
    expect=[1, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums（原数组）', cell=84, h=150,
             color=lambda S, i, v: 'blue' if v == S.get('target') else None),
        dict(type='array', var='sorted(nums)', label='排序后（绿 = 等于 target，下标即答案）', cell=84, h=200,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if v == S.get('target') else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='array', var='res', label='res（目标下标）', cell=84, h=150, color=lambda S, i, v: 'green'),
    ],
    watch=[('target', 'target', 'blue'), ('index', 'index', 'pink'), ('num', 'num', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来收集所有目标下标',
        'for index, num in enumerate(sorted(nums))': lambda S, B, r: (
            f'先排序，再遍历：`index = {S.index}`，`num = {S.num}`' if 'index' in S and S.get('index') != B.get('index')
            else '排序后的数组遍历完了'),
        'if num == target': lambda S, B, r: (
            f'`num = {S.num}` == `target = {S.target}` → ==是目标下标=='
            if S.num == S.target else f'`num = {S.num}` ≠ `target = {S.target}` → 跳过'),
        'res.append(index)': '把下标 `{index}` 加入 `res` → `{res}`；排序后相同的值挨在一起，所以下标连续',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先排序，再扫一遍，等于 target 的下标就是答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 排序后，返回所有满足 `nums[i] == target` 的下标 `i`（递增）',
                 '示例：`nums = [1,2,5,2,3]`，`target = 2` → `[1,2]`',
                 '本视频：`[1,2,5,2,3,2]`，`target = 2` → `[1,2,3]`'],
        quote='比较基础的题目。按题目要求将数组排序，然后一趟遍历找到所有等于target的下标即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sorted(nums)` 得到排序后的数组，原数组不动',
              '`enumerate` 同时拿到下标 `index` 和值 `num`',
              '`num == target` 就记下 `index`，不存在则 `res` 保持为空'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '要的是排序==后==的下标，不是原数组的下标',
                 '不存在目标时返回空列表 `[]`',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
