from math import gcd


CONFIG = dict(
    num=2176, title='统计数组中相等且可以被整除的数对', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举 j · gcd 求 k\' · 哈希表记因子',
    tags=['灵神题单', '数学算法', '难度分 2200'],
    code='''
# 预处理每个数的因子
MX = 101
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i, MX, i):
        divisors[j].append(i)

class Solution:
    def countPairs(self, nums: list[int], k: int) -> int:
        ans = 0
        cnt = defaultdict(int)
        for j, x in enumerate(nums):  # 枚举 j，计算左边有多少个符合要求的 i
            if j and x == nums[0]:
                ans += 1  # 单独统计 i=0 的情况
            k2 = k // gcd(k, j)  # i 必须是 k2 的倍数
            ans += cnt[(x, k2)]
            for d in divisors[j]:  # j 是 d 的倍数
                cnt[(x, d)] += 1
        return ans
''',
    call='Solution().countPairs([3,1,2,2,2,1,3], 2)',
    expect=4,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"当前 `j = {S['j']}`，`x = {S['x']}`；左边值为 {S['x']} 且下标是 `k2 = {S['k2']}` 的倍数的数有几个？" if 'k2' in S and 'x' in S and S['_line'] >= 15 else
                                              (f"当前 `j = {S['j']}`，`x = {S['x']}`" if 'x' in S and 'j' in S else '枚举 j，查左边满足条件的 i 的个数'))),
        dict(type='array', var='nums', h=190, label='nums', pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if 'j' in S and 'x' in S and i < S['j'] and v == S['x'] else None),
        dict(type='map', var='cnt', h=330, fmt=lambda k, v: f'(值{k[0]}, 因子{k[1]}) : {v}', font=24),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'cyan'), ('k2', 'k2', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'if j and x == nums[0]': lambda S, B, r: (f'`j = 0`：`i = j` 无意义，跳过' if S.j == 0 else f'`j={S.j} ≠ 0` 且 `x = {S.x}` {"等于" if S.x == S.nums[0] else "不等于"} `nums[0] = {S.nums[0]}`：{"i=0 配对成立（0×j=0 被 k 整除）" if S.x == S.nums[0] else "i=0 不配"}'),
        'ans += 1': '`i = 0` 时乘积为 0，一定被 `k` 整除：`ans` = =={ans}==',
        'k2 = k // gcd': lambda S, B, r: f'`gcd({S.k}, {S.j}) = {gcd(S.k, S.j)}`，所以 `i` 只要是 `k2 = {S.k} // {gcd(S.k, S.j)}` = =={S.k2}== 的倍数',
        'ans += cnt': '左边值为 `{x}`、下标是 `{k2}` 的倍数的个数 `cnt[({x}, {k2})] = {cnt[(x, k2)]}` → `ans` = =={ans}==',
        'cnt[(x, d)] += 1': '`j = {j}` 是 `{d}` 的倍数：记一笔 `({x}, {d})` → {cnt[(x, d)]}',
        'return ans': '共 `{ans}` 对',
    },
    skip=['for d in divisors', 'ans = 0', 'cnt = defaultdict'],
    max_steps=80,
    cards=dict(
        one_liner='枚举 j，i 只需是 k/gcd(k,j) 的倍数',
        complexity='时间 `O(n log n)`，空间 `O(n log n)`',
        problem=['求满足 `i < j`、`nums[i] == nums[j]` 且 `i × j` 能被 `k` 整除的数对个数',
                 '示例：`nums = [3,1,2,2,2,1,3]`，`k = 2` → `4`'],
        quote='枚举 j，那么 i 必须是 k\'=k/GCD(k,j) 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i×j` 被 `k` 整除 ⇔ `i` 是 `k/gcd(k,j)` 的倍数（约掉 j 带来的因子）',
              '哈希表 `cnt[(值, d)]` 记录：左边值为该值、下标是 `d` 的倍数的个数',
              '每个 `j` 把它的所有因子 `d` 都记一笔；`i = 0` 乘积为 0，单独统计'],
        summary=['预处理因子表调和级数 `O(M log M)`，枚举 j 为 `O(n log n)`',
                 '易错点：`i = 0` 不是任何数的因子，必须单独加一',
                 '`k2` 要用整除 `//`；本题数据小，暴力 `O(n²)` 也行，但 `n = 10⁵` 就要这种写法'],
    ),
)
