def _k(S):
    n = S['nums']
    for k in range(1, len(n) + 1):
        if sum(n[:k]) == S['now']:
            return k
    return 1


CONFIG = dict(
    num=2219, title='数组的最大总分', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 总和反推后缀和',
    tags=[],
    code='''
class Solution(object):
    def maximumSumScore(self, nums):

        s = sum(nums)
        res = max(nums[0], s)
        
        now = nums[0]
        for v in nums[1:]:
            res = max(res, now + v, s - now)
            now += v
        
        return res
''',
    call='Solution().maximumSumScore([-3,6,-2,4])',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 前缀和 now 覆盖的范围，黄 = 当前 v）', cell=96, h=190,
             window=(lambda S: 0 if 'now' in S else None, lambda S: _k(S) - 1 if 'now' in S else None),
             color=lambda S, i, v: 'yellow' if 'v' in S and i == _k(S) and S['_line'] != 10 else None),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"前缀和 `now+v` = =={S['now'] + S['v']}==，后缀和 `s−now` = =={S['s'] - S['now']}==" if 'v' in S and S['_line'] == 9 else
            (f"当前前缀和 `now` = =={S['now']}==，总和 `s` = =={S['s']}==" if 'now' in S else ''))),
        dict(type='text', h=80, size=32, fn=lambda S: f"`res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('s', 's', 'blue'), ('v', 'v', 'yellow'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        's = sum(nums)': '先求总和 `s = {s}`：后缀和 = `s − 前缀和 + 当前数`，不用再算一遍',
        'res = max(nums[0], s)': '下标 0 的得分：前缀和 `{nums[0]}`，后缀和就是整个数组 `{s}` → `res = {res}`',
        'now = nums[0]': '`now` = 前缀和（目前是 `nums[0]` 本身）',
        'for v in nums[1:]': '看下一个位置，`v = {v}`',
        'res = max': '这个位置的前缀和 `{now} + ({v})` = {now+v}，后缀和 `{s} − ({now})` = {s-now}，取大的更新 → `res = {res}`',
        'now += v': '前缀和并入 `v` → `now = {now}`',
        'return res': '所有位置都看过了，最大得分 `{res}`',
    },
    cards=dict(
        one_liner='前缀和 + 后缀和 = 总和 + 当前数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['位置 `i` 的得分 = 以 `i` 结尾的前缀和、以 `i` 开头的后缀和，取较大者',
                 '求所有位置得分的最大值',
                 '本视频：`[-3,6,-2,4]` → `10`'],
        quote='这个前缀和与后缀和相加恰好就是数组总和再加上当前位置上的数',
        quote_src='—— yiduobo 题解原文',
        idea=['先求总和 `s`，边遍历边累计前缀和 `now`',
              '后缀和不用另算：新位置 `v` 的前缀和是 `now+v`，后缀和是 `s−now`',
              '每个位置取两者较大，再更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '下标 0 的前缀和是 `nums[0]`，后缀和是 `s`，要单独初始化',
                 '遍历到 `v` 时：前缀和含 `v`，后缀和是 `s − now`（`now` 不含 `v`）',
                 '原文为 Python 2 风格，代码一字未改'],
    ),
)
