
CONFIG = dict(
    num=2601, title='质数减法运算', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='贪心 + 筛质数 + 二分',
    tags=['灵神题单', '数学算法', '难度分 1779'],
    code='''
MX = 1000
P = [0]  # 哨兵，避免二分越界
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        P.append(i)  # 预处理质数列表
        for j in range(i * i, MX, i):
            is_prime[j] = False

class Solution:
    def primeSubOperation(self, nums: List[int]) -> bool:
        pre = 0
        for x in nums:
            if x <= pre: return False
            pre = x - P[bisect_left(P, x - pre) - 1]  # 减去 < x-pre 的最大质数
        return True
''',
    call='Solution().primeSubOperation([4,9,6,10])',
    expect=True,
    views=[
        dict(type='text', h=70, fn=lambda S, B: (f"上一个减完的数 `pre = {B['pre'] if S.get('_line') == 15 else S['pre']}`，当前 `x = {S['x']}`，要减去 `< {S['x'] - (B['pre'] if S.get('_line') == 15 else S['pre'])}` 的最大质数" if 'x' in S and 'pre' in S else '质数表 `P`（1000 以内，含哨兵 0）已预处理好')),
        dict(type='array', var='nums', h=200, label='nums',
             color=lambda S, i, v: 'blue' if 'x' in S and S['nums'].index(S['x']) == i else None),
    ],
    watch=[('pre', 'pre', 'green'), ('x', 'x', 'blue')],
    captions={
        'pre = 0': '`pre` 是上一个减完后的数，开头设为 0（正整数都比它大）',
        'if x <= pre': '`x = {x}` 与 `pre = {pre}`：{"x 不超过 pre，再怎么减也无法严格递增 → 返回 false" if x <= pre else "x 比 pre 大，还有操作空间"}',
        'pre = x - P[': '在质数表里二分，找 `< {x - B.pre}` 的最大质数 `{x - pre}`（0 表示没有可减的）：==尽量减大==让 `pre` 尽量小 → `pre = {x} − {x - pre} = {pre}`',
        'return True': '全部处理完，严格递增 → ==true==',
    },
    skip=['for j in range', 'is_prime[j] = False'],
    cards=dict(
        one_liner='每个数都尽量减大，让减完的值尽量小，给后面留空间',
        complexity='时间 `O(n log U)`，空间 `O(1)`（不计预处理）',
        problem=['每个下标至多减一次，减去一个 ==严格小于 nums[i]== 的质数',
                 '问能否让 `nums` 变成严格递增数组',
                 '示例：`[4,9,6,10]` → `true`'],
        quote='设 pre 是上一个减完后的数字，x=nums[i] 为当前数字。设 p 是满足 x−p>pre 的最大质数，换言之，p 是小于 x−pre 的最大质数，这可以预处理质数列表后，用二分查找得到。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：当前数减得越小，后面的数越容易比它大',
              '约束 `x - p > pre`，所以 `p < x - pre`，取最大质数',
              '质数表用筛法预处理，查询用 `bisect_left` 二分；表头放哨兵 0 防越界'],
        summary=['预处理筛质数 `O(U log log U)`，之后每个数二分 `O(log U)`',
                 '易错点：`x <= pre` 时直接返回 false；找不到质数时哨兵 0 表示不减',
                 '`bisect_left(P, x-pre)` 得到第一个 ≥ x−pre 的位置，再 −1 才是严格小于的最大质数'],
    ),
)
