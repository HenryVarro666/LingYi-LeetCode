CONFIG = dict(
    num=3353, title='最小总操作数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计相邻不同的位置数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        res = 0
        for index in range(1, len(nums)):
            if nums[index] != nums[index - 1]:
                res += 1
        return res
''',
    call='Solution().minOperations([3,3,5,2,2,7])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=300, cell=110, pointers={'index': 'blue'},
             color=lambda S, i, v: ('orange' if S.get('index') is not None and i == S['index'] - 1 and S['_line'] >= 7 and S['nums'][i] != S['nums'][S['index']] else None)),
        dict(type='text', size=34, fn=lambda S: (f"`nums[{S['index']-1}] = {S['nums'][S['index']-1]}`，`nums[{S['index']}] = {S['nums'][S['index']]}`" if S.get('index') else '')),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计需要操作的次数',
        'for index in range': lambda S, B, r: ('所有相邻对都看完了' if B.get('index') == S.index else f'看相邻的一对：`nums[{S.index-1}]` 和 `nums[{S.index}]`'),
        'if nums[index] != ': lambda S, B, r: (f'`{S.nums[S.index]} ≠ {S.nums[S.index-1]}` → 必须对前缀 `[0..{S.index-1}]` 操作一次，把它拉到和右边一样'
                                              if S.nums[S.index] != S.nums[S.index-1] else f'`{S.nums[S.index]} = {S.nums[S.index-1]}` 已经相等 → 不需要新操作'),
        'res += 1': '多一次前缀操作：`res = {res}`',
        'return res': '最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='相邻两数不同，就必须多一次前缀操作',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作选一个前缀，给前缀所有元素加上整数 `k`（`k` 可为负）',
                 '求让数组所有元素相等的最少操作次数',
                 '示例：`[3,3,5,2,2,7]` → `3`'],
        quote='若其与nums[index - 1]不同，那么无论怎么修改，都至少需要对前缀nums[0]到nums[index - 1]执行一次操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一前缀操作多次可以合并成一次，所以每个前缀最多操作一次',
              '只有改前缀 `[0..index-1]`，才能改变 `nums[index-1]` 与 `nums[index]` 的差',
              '每个不同的相邻对至少要一次，且一次操作恰好能消掉它，答案就是相邻不同的对数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一次前缀操作只改变一处相邻差，所以下界就是答案',
                 '数组长度为 1 或全相等时答案为 0',
                 '题面库里缺失，题意据 yiduobo 文章整理'],
    ),
)
