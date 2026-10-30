CONFIG = dict(
    num=3987, title='处理所有元素的成本', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='模拟 · 等差数列求和',
    tags=['灵神题单', '难度分 1550'],
    code='''
class Solution:
    def minimumCost(self, nums: list[int], k: int) -> int:
        MOD = 1_000_000_007
        s = 0  # 总操作次数
        left = k
        for x in nums:
            if left < x:
                op = (x - left - 1) // k + 1  # 把 left 增大到 >= x，至少操作 op 次
                s += op
                left += op * k
            left -= x

        # 1 + 2 + ... + s
        return s * (s + 1) // 2 % MOD
''',
    call='Solution().minimumCost([1,2,7,13], 4)',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在处理的元素）', cell=100, pointers={'nums.index(x)': 'blue'},
             pointer_labels={'nums.index(x)': 'x'},
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='text', size=28, fn=lambda S: (f"剩余资源 `left = {S['left']}`，操作总次数 `s = {S['s']}`" if 'left' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('x', 'x', 'pink'), ('s', 's', 'green')],
    captions={
        's = 0': '`s` 只记==操作次数==，不急着算成本',
        'left = k': '一开始有 `k = {k}` 单位资源',
        'if left < x': lambda S, B, r: (f'`left = {S.left} < x = {S.x}`：资源不够，要补充' if S.left < S.x
                                        else f'`left = {S.left} ≥ x = {S.x}`：够用，直接处理'),
        'op = ': '至少补 `op = ({x} - {B.left} - 1) // {k} + 1` = =={op}== 次，才能让 left ≥ x',
        's += op': '总操作次数 `s` → =={s}==',
        'left += op * k': '补充 `{op} × {k}`，`left` → {left}',
        'left -= x': '处理 `{x}`，剩余 `left` → =={left}==',
        'return': '第 i 次操作成本为 i，共 `s = {s}` 次 → `1+2+…+s = {s}×({s}+1)/2` = ==15==，再取模',
    },
    cards=dict(
        one_liner='先数出总共补几次，再用等差数列求成本',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['按顺序处理 `nums`，资源不够就补 `k` 单位，第 j 次补充成本为 j',
                 '求处理完所有元素的最小总成本（对 `10^9+7` 取模）',
                 '本视频：`nums=[1,2,7,13]`，`k=4` → `15`'],
        quote='累加所有操作次数，得到总操作次数 sum。根据等差数列求和公式，最终答案为 1+2+⋯+sum = sum(sum+1)/2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`left < x` 时，最少补 `ceil((x-left)/k)` 次，写成 `(x-left-1)//k+1` 避开浮点',
              '成本只和==总次数==有关：第 1 次 1，第 2 次 2……所以等差数列求和',
              '补的次数越少越好，所以每个元素只补到刚好够用'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '上取整用 `(a-1)//k+1`，注意 `x-left` 是正数才能用',
                 '`s*(s+1)` 必为偶数，除以 2 不需要逆元；Python 大整数最后再取模即可',
                 '方法二：资源可累积，总次数 `(sum(nums)-1)//k`，一行搞定'],
    ),
)
