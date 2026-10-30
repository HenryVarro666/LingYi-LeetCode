from math import gcd

CONFIG = dict(
    num=2183, title='统计可以被 K 整除的下标对数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='gcd 约分 · 统计 k 的因子',
    tags=['灵神题单', '数学算法', '难度分 2246'],
    code='''
class Solution:
    def countPairs(self, nums: List[int], k: int) -> int:
        divisors = []  
        d = 1
        while d * d <= k:  # 预处理 k 的所有因子
            if k % d == 0:
                divisors.append(d)
                if d * d < k:
                    divisors.append(k // d)
            d += 1
        ans = 0
        cnt = Counter()
        for v in nums:
            ans += cnt[k // gcd(v, k)]
            for d in divisors:
                if v % d == 0:
                    cnt[d] += 1
        return ans
''',
    call='Solution().countPairs([1,2,3,4,5], 4)',
    expect=4,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"当前 `v = {S['v']}`：左边需要是 `k // gcd(v, k) = {S['k'] // gcd(S['v'], S['k'])}` 的倍数" if 'v' in S and S['_line'] >= 13 else f"`k = {S['k']}` 的因子表 `divisors = {S['divisors']}`")),
        dict(type='array', var='nums', h=190, label='nums',
             color=lambda S, i, v: ('blue' if v == S['v'] and S['_line'] >= 13 else None) if 'v' in S else None),
        dict(type='map', var='cnt', h=300, fmt=lambda k, v: f'因子 {k} 的倍数个数 : {v}', font=26),
    ],
    watch=[('v', 'v', 'blue'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'while d * d <= k': lambda S, B, r: (f'`{S.d}² = {S.d * S.d} ≤ {S.k}`，继续枚举因子' if S.d * S.d <= S.k else f'`{S.d}² > {S.k}`：因子枚举完，`divisors = {S.divisors}`'),
        'divisors.append(d)': '`{d}` 整除 `{k}`，是 k 的因子',
        'divisors.append(k // d)': '配对的另一个因子 `{k} // {d} = {k // d}`',
        'if k % d == 0': '`{k} % {d} == 0`？{"是，d 是因子" if k % d == 0 else "不是"}',
        'ans += cnt': lambda S, B, r: f'`gcd({S.v}, {S.k}) = {gcd(S.v, S.k)}`，左边的数要是 `k // gcd = {S.k // gcd(S.v, S.k)}` 的倍数，已有 `{S.cnt[S.k // gcd(S.v, S.k)]}` 个 → `ans` = =={S.ans}==',
        'if v % d == 0': '`{v} % {d} == 0`？{"是：v 是 d 的倍数" if v % d == 0 else "不是"}',
        'cnt[d] += 1': '`{v}` 是 `{d}` 的倍数，`cnt[{d}]` → {cnt[d]}',
        'return ans': '共 `{ans}` 对',
    },
    skip=['divisors = []', 'd = 1', 'd += 1', 'ans = 0', 'cnt = Counter'],
    max_steps=80,
    cards=dict(
        one_liner='枚举 nums[j]，约掉 gcd 后，左边只需是 k/gcd 的倍数',
        complexity='时间 `O(n·d(k))`，空间 `O(d(k))`，`d(k)` 为 k 的因子个数',
        problem=['求满足 `i < j` 且 `nums[i] × nums[j]` 能被 `k` 整除的下标对个数',
                 '`n` 最大 `10⁵`，`O(n²)` 会超时',
                 '示例：`nums = [1,2,3,4,5]`，`k = 4` → `4`'],
        quote='nums[i] 必须是 x = k / GCD(nums[j], k) 的倍数。……统计 v 是 k 的哪些因子的倍数，这可以通过枚举 k 的所有因子来判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `nums[j]`，从 `k` 里约掉 `gcd(nums[j], k)`，剩下的 `x` 必须由左边的数提供',
              '所以 `x` 是 `k` 的因子，只需统计「左边有多少数是 `x` 的倍数」',
              '预处理 `k` 的全部因子，每个 `v` 检查它是哪些因子的倍数，计入 `cnt`'],
        summary=['先查询 `cnt[k // gcd(v, k)]`，再把当前 `v` 计入，保证只数左边',
                 '原文 `k / gcd` 与 `k / d` 在 Python 3 中得到小数，已改为 `//`，字典键才是整数',
                 '灵神另有方法一：预处理 10⁵ 内每个数的因子，这里演示方法二（只枚举 k 的因子）'],
    ),
)
