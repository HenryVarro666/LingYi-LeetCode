CONFIG = dict(
    num=2656, title='K 个元素的最大和', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='贪心取最大 · 求和公式', tags=[],
    code='''
class Solution(object):
    def maximizeSum(self, nums, k):

        return max(nums) * k + (k - 1) * k // 2
''',
    call='Solution().maximizeSum([5,5,5], 2)',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums', h=200,
             color=lambda S, i, v: 'pink' if v == max(S['nums']) and i == S['nums'].index(v) else None),
        dict(type='text', size=34, fn=lambda S: f"`ma × k` = `{max(S['nums'])} × {S['k']}` = {max(S['nums']) * S['k']}" if 'nums' in S else ''),
        dict(type='text', size=34, fn=lambda S: f"`(k − 1) × k // 2` = `{S['k'] - 1} × {S['k']} // 2` = {(S['k'] - 1) * S['k'] // 2}，合计 =={max(S['nums']) * S['k'] + (S['k'] - 1) * S['k'] // 2}==" if 'nums' in S else ''),
    ],
    watch=['k'],
    captions={
        'return': '操作的数是 `ma, ma+1, …, ma+k-1`：`ma × k` = {max(nums) * k}，再加 `1+2+…+(k-1)` = {(k - 1) * k // 2}，答案 =={ret}==',
    },
    cards=dict(
        one_liner='每次都操作最大的数，答案是 ma 乘 k 加上 1 到 k−1 的和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选一个数 `m` 得 `m` 分，并把它换成 `m+1`',
                 '恰好做 `k` 次，求最大得分',
                 '示例：`[5,5,5], k=2` → `11`（5+6）'],
        quote='题目中的每次操作都会使得被操作的元素变得更大，那么为了使得和最大，就应该不断操作数组中最大的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作会让元素变大，所以一直盯着最大的元素',
              '设最大值 `ma`，操作的数依次是 `ma, ma+1, …, ma+k-1`',
              '求和得 `ma × k + (k−1)·k / 2`'],
        after=[dict(heading='拆成两部分', lines=['每一次选的数比 `ma` 多出 `0, 1, 2, …, k−1`','所以总和 = `ma × k`（基础部分）+ `0+1+…+(k−1)`（增量部分）','增量部分用等差数列求和 `(k−1)·k / 2`','示例 `[5,5,5], k=2`：`5×2 + 1 = 11`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`',
                 '易错点：额外部分是 `1+…+(k−1)`，不是到 `k`'],
    ),
)
