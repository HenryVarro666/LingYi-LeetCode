def _idx(S):
    return S['nums'].index(S['num']) if 'num' in S else None


CONFIG = dict(
    num=1827, title='最少操作使数组递增', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='一趟扫描 · 维护上一个数的最终值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        last = nums[0]
        res = 0
        for num in nums[1:]:
            if num < last + 1:
                res += last + 1 - num
                last += 1
            else:
                last = num
        
        return res
''',
    call='Solution().minOperations([1,5,2,4,0])',
    expect=15,
    views=[
        dict(type='text', fn=lambda S: (f"上一个数最终值 `last = {S['last']}`，当前数 `{S['num']}`，至少要到 `{S['last'] + 1}`" if 'num' in S else f"`last = {S['last']}`（第一个数不用动）") if 'last' in S else '', size=30),
        dict(type='array', var='nums', label='nums（蓝箭头 = 当前数）', h=300,
             color=lambda S, i, v: 'blue' if 'num' in S and S['nums'].index(S['num']) == i else None),
    ],
    watch=[('last', 'last', 'cyan'), ('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'last = nums[0]': '第一个数不需要比较，它的最终值就是 `last = {last}`',
        'res = 0': '`res` 累计操作次数',
        'for num in': '取下一个数 `num = {num}`，和上一个数的最终值 `last = {last}` 比',
        'if num < last + 1': '`num < last + 1`（{num} < {last + 1}）→ ==没有严格大于 last，要加高==' ,
        'res += last + 1 - num': '把 `{num}` 加到 `{B.last} + 1`，要 `{B.last} + 1 − {num}` 次 → `res` = =={res}==',
        'last += 1': '它的最终值就是 `last + 1`：能小则小，后面的数压力最小 → `last` = {last}',
        'last = num': '`num` 已经比 last 大，不用操作，它自己成为新的 `last = {last}`',
        'return res': '全部扫完，总操作次数 `{res}`',
    },
    cards=dict(
        one_liner='每个数都只加到刚好比前一个大 1，一趟扫描搞定',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可以让 `nums` 里某个数加 1',
                 '求让数组==严格递增==的最少操作次数',
                 '示例：`[1,5,2,4,0]` → `15`'],
        quote='对于一个数而言，操作次数越少答案越小，同时越有利于后面的数字递增',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数的最少操作次数只取决于前一个数的最终值 `last`',
              '`num <= last`：加到 `last + 1`，花 `last + 1 - num` 次',
              '`num > last`：不用动，`last` 更新为 `num`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '条件写成 `num < last + 1` 等价于 `num <= last`',
                 '易错点：`last` 要用==最终值==，不是原数组里的前一个数',
                 '同类题：灵神题单「贪心与思维」中的从左到右贪心'],
    ),
)
