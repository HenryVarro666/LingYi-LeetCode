def _row(S):
    x, y = S['x'], S['y']
    s = S.get('s')
    if s is None:
        return '`dp[s]` = 已用 nums2 的下标集合为 `s`（二进制）时，前 `popcount(s)` 个 nums1 的最小异或和'
    k = bin(s).count('1')
    return f'集合 `s = {s:0{len(x)}b}`：已匹配 nums1 前 =={k}== 个 → 下一个是 `x[{k}] = {x[k]}`'


CONFIG = dict(
    num=1879, title='两个数组最小的异或值之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP（Go 原文转写）',
    tags=['图论算法', '动态规划', '难度分 2145'],
    code='''
class Solution:
    def minimumXORSum(self, x: List[int], y: List[int]) -> int:
        m = 1 << len(x)
        dp = [0] * m
        for i in range(len(dp)):
            dp[i] = int(2e9)
        dp[0] = 0
        for s in range(m - 1):
            dv = dp[s]
            v = x[s.bit_count()]
            t, lb = s ^ (m - 1), 0
            while t > 0:
                lb = t & -t
                w = y[lb.bit_length() - 1]
                dp[s | lb] = min(dp[s | lb], (v ^ w) + dv)
                t ^= lb
        return dp[m - 1]
''',
    call='Solution().minimumXORSum([1,0,3], [5,3,4])',
    expect=8, max_steps=44,
    skip=['for i in range(len(dp))', 'dp[i] = int', 'dv = dp[s]', 'w = y[', 't ^= lb', 't, lb =', 'dp = [0]', 'dp[0] = 0'],
    views=[
        dict(type='text', fn=_row, size=24, h=60),
        dict(type='array', var='x', label='x = nums1（按顺序一个个配）', h=150, cell=80,
             pointers={'k': 'blue'},
             color=lambda S, i, v: 'blue' if 's' in S and i == bin(S['s']).count('1') else None,
             dim=lambda S, i, v: 's' in S and i < bin(S['s']).count('1')),
        dict(type='array', var='y', label='y = nums2（t 里的位 = 还没用的）', h=150, cell=80,
             color=lambda S, i, v: ('pink' if 'lb' in S and 'w' in S and i == S['lb'].bit_length() - 1 and S['_line'] >= 14 else None)),
        dict(type='array', var=lambda S: ['∞' if v >= 2000000000 else v for v in S['dp']], label='dp[s]：下标 s 的二进制 = 已选 nums2 的集合', h=190, cell=84,
             pointers={'s': 'blue'},
             color=lambda S, i, v: 'green' if 's' in S and 'lb' in S and i == (S['s'] | S['lb']) and S['lb'] > 0 and S['_line'] >= 15 else None),
    ],
    watch=[('s', 's', 'blue'), 'dv', 'v', 't', 'lb', 'w', ('dp[m-1]', "'∞' if dp[m - 1] >= 2000000000 else dp[m - 1]", 'green')],
    captions={
        'm = 1 <<': '`m = 1 << {len(x)} = {m}`：nums2 的每个子集一个状态',
        'dp = [0]': '`dp` 先开 `{m}` 个格子',
        'dp[0] = 0': '什么都没选，异或和 `dp[0] = 0`',
        'for s in range': '`s = {s}`：这个集合里 nums2 的元素已被用掉',
        'dv = dp[s]': '这个集合当前最小异或和 `dv = {dv}`',
        'v = x[s.bit_count()]': '`dv = dp[s] = {dv}`；集合里有 `{s.bit_count()}` 个数，所以轮到 `x[{s.bit_count()}]` = =={v}==',
        't, lb = ': '`t = s ^ (m-1)` = 没选的 nums2 位置集合 = `{t:b}`',
        'while t > 0': lambda S, B, r: (f'`t = {S.t:b}` 还有没试过的 nums2 元素 → 继续' if S.t > 0 else '没选的都试过了，换下一个 `s`'),
        'lb = t & -t': '`lowbit` 取出 t 最低位 `lb = {lb}` → 要配的是 `y[{lb.bit_length()-1}]` = {y[lb.bit_length()-1]}',
        'w = y[': '这位对应 `y[{lb.bit_length()-1}]` = =={w}==',
        'dp[s | lb] = min': '用 `x[{s.bit_count()}]` 配 `y[{lb.bit_length()-1}]`：`({v} ^ {w}) + {dv}` = {(v ^ w) + dv} → `dp[{s | lb}] = min({B.dp[s | lb]}, {(v ^ w) + dv})` = =={dp[s | lb]}==',
        't ^= lb': '把这一位从 t 里去掉，接着试下一个：`t = {t}`',
        'return dp[m - 1]': '全部配完（全 1 的集合），最小异或和 = =={ret}==',
    },
    cards=dict(
        one_liner='集合 s 的大小，就是 nums1 已经配到第几个',
        complexity='时间 `O(n·2^n)`，空间 `O(2^n)`',
        problem=['把 `nums2` 重新排列，使 `Σ nums1[i] XOR nums2[i]` 最小',
                 '`n ≤ 14`，可以用二进制集合表示 nums2 用掉了哪些',
                 '示例：`[1,0,3]`，`[5,3,4]` → `8`'],
        quote='原文为 Go：`v := x[bits.OnesCount(uint(s))]`，`for t, lb := s^(m-1), 0; t > 0; t ^= lb`，`dp[s|lb] = min(dp[s|lb], v^w+dv)`。',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['`s` 里有几个 1，就已经配了 nums1 的前几个，所以不用再记第一维',
              '枚举没选的位 `lb`，用 `x[popcount(s)]` 去配 `y[lb]`',
              '往 `dp[s|lb]` 刷表，答案是全 1 集合 `dp[m-1]`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n·2^n)`，空间 `O(2^n)`',
                 '易错：Go 里 `v^w+dv` 是从左到右算，Python 要写成 `(v ^ w) + dv`',
                 '易错：`2e9` 在 Python 是浮点，写成 `int(2e9)`；`TrailingZeros(lb)` = `lb.bit_length() - 1`',
                 '题单里也列在网络流：这题还能用 KM / 费用流做'],
    ),
)
