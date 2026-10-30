def _text(S):
    if 'pre' not in S:
        return '相邻两个 1 之间有 `x` 个 0，就有 `x + 1` 个位置可以画分割线'
    if S['pre'] < 0:
        return '还没遇到 1：第一个 1 前面的 0 都归它，不用分割'
    return f"上一个 1 在下标 `{S['pre']}`；`ans = {S['ans']}`"


CONFIG = dict(
    num=2750, title='将数组划分成若干好子数组的方式', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='乘法原理 · 相邻 1 的间距',
    tags=['灵神题单', '难度分 1598'],
    code='''
class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        ans, pre = 1, -1
        for i, x in enumerate(nums):
            if x == 0: continue
            if pre >= 0:
                ans = ans * (i - pre) % MOD
            pre = i
        return 0 if pre < 0 else ans
''',
    call='Solution().numberOfGoodSubarraySplits([0,1,0,0,1,0,0,0,1])',
    expect=12,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var='nums', pointers={'pre': 'pink', 'i': 'blue'}, h=300,
             color=lambda S, i, v: 'green' if v == 1 else None,
             dim=lambda S, i, v: 'i' in S and v == 0 and i < S['i']),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans, pre = 1, -1': '`ans = 1` 是乘法的单位元；`pre = -1` 表示还没见过 1',
        'if x == 0': lambda S, B, r: (f'`nums[{S.i}] = 0`：不是 1，跳过' if S.x == 0 else f'`nums[{S.i}] = 1`：遇到一个 1'),
        'if pre >= 0': lambda S, B, r: ('`pre >= 0`：前面有 1，这两个 1 之间要画一条分割线' if S.pre >= 0
                                        else '`pre = -1`：这是第一个 1，前面的 0 全归它，不用画线'),
        'ans = ans *': '两个 1 在 `{pre}` 和 `{i}`，中间 `{i - pre - 1}` 个 0，有 `{i - pre}` 个位置可画线 → `ans = {B.ans} × {i - pre} = {ans}`',
        'pre = i': '记下这个 1 的位置：`pre = {pre}`',
        'return 0 if': lambda S, B, r: ('数组里没有 1，不能划分，返回 0' if S.pre < 0 else f'每对相邻 1 的方案数相乘（乘法原理），答案 `{r}`'),
    },
    cards=dict(
        one_liner='每两个 1 之间画一条分割线，有 x 个 0 就有 x+1 种画法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二元数组，恰好含一个 `1` 的子数组叫好子数组',
                 '求把 `nums` 划分成若干好子数组的方法数，对 `10^9 + 7` 取余',
                 '示例：`[0,1,0,0,1]` → `3`'],
        quote='根据题意，需要在每两个 1 之间画一条分割线，有 x 个 0 就可以画 x+1 条分割线。根据乘法原理，答案为所有分割线的方案数的乘积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个好子数组恰有一个 1 → 相邻两个 1 之间必须断开一次',
              '断开的位置在这两个 1 之间 `x` 个 0 的 `x + 1` 个空隙里任选',
              '各对 1 之间互不影响 → 把每对的 `i - pre` 连乘'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '特判：没有 1 返回 `0`；只有一个 1 时乘法一次也没做，答案 `1`',
                 '乘完立刻 `% MOD`，避免数字过大（Python 不会溢出，但变慢）',
                 '相似题：2147 分隔长廊的方案数'],
    ),
)
