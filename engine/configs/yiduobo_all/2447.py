CONFIG = dict(
    num=2447, title='最大公因数等于 K 的子数组数目', difficulty='Medium', category='位运算',
    author='yiduobo', technique='枚举左端点 + 向右累计 GCD（暴力）',
    tags=['GCD'],
    code='''
class Solution(object):
    def subarrayGCD(self, nums, k):

        res = 0
        n = len(nums)

        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        for i in range(n):
            now = nums[i]
            if now % k != 0:
                continue
            
            if now == k:
                res += 1

            for j in range(i + 1, n):
                now = gcd(now, nums[j])
                if now == k:
                    res += 1
                elif now < k:
                    break
        
        return res
''',
    call='Solution().subarrayGCD([9,3,1,6,3], 3)',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=230,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None),
        dict(type='text', fn=lambda S: (
            f"`now = {S['now']}` 是 `[{S['i']}..{S['j']-1}]` 的 GCD，即将并入 `nums[{S['j']}] = {S['nums'][S['j']]}`" if S.get('_line') == 21 and 'j' in S and 'now' in S and S['_line'] == 21 else
            f"窗口 `[{S['i']}..{S['j']}]` 的 GCD = ==`{S['now']}`==，目标 `k = {S['k']}`" if 'j' in S and 'now' in S and S['j'] > S['i'] else
            f"以 `i={S['i']}` 为左端点：`now = {S['now']}`" if 'i' in S and 'now' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计 GCD 等于 `k` 的子数组个数',
        'n = len': '数据规模小，直接 `O(n^2)` 暴力',
        'def gcd': '自己写的辗转相除求 GCD',
        'for i in range(n)': '枚举左端点 `i = {i}`',
        'now = nums[i]': '`now` = 子数组 `[{i}..{i}]` 的 GCD = `{now}`',
        'if now % k': lambda S, B, r: (f'`{S.now} % {S.k} ≠ 0` → 不是 k 的倍数，GCD 不可能是 k → ==整个左端点作废==，换下一个'
                                       if S.now % S.k else f'`{S.now} % {S.k} = 0`，是 k 的倍数，继续'),
        'if now == k:\n': '',
        'res += 1': '`res` = =={res}==',
        'for j in range(i + 1, n)': '右端点 `j = {j}`',
        'now = gcd(now, nums[j])': '调用 `gcd({now}, {nums[j]})`，求子数组 `[{i}..{j}]` 的 GCD（见下面辗转相除）',
        'elif now < k': lambda S, B, r: (f'`{S.now} < {S.k}` → GCD 只会越来越小，不可能再回到 k → ==break==' if S.now < S.k
                                         else f'`{S.now}` 还大于 `{S.k}`，继续往右扩'),
        'break': '提前结束这个左端点',
        'return x': 'GCD 求出：==`{ret}`==',
        'return res': '一共 =={res}== 个子数组',
    },
    cards=dict(
        one_liner='GCD 越算越小：降到 k 以下就提前停',
        complexity='时间 `O(n^2 log U)`（`n` 很小），空间 `O(1)`',
        problem=['数出 `nums` 中有多少个子数组，元素的最大公约数恰好等于 `k`',
                 '示例：`[9,3,1,2,6,3], k=3` → `4`',
                 '本视频：`[9,3,1,6,3], k=3` → `4`'],
        quote='由于数据规模比较小，我在这里采用的是O(n^2)的暴力算法。枚举数组的左边界i，然后从i开始向后枚举右边界j并判断当前子数组的最大公约数是否等于k。',
        quote_src='—— yiduobo 题解原文',
        idea=['滑动窗口行不通：窗口左端右移时，GCD 没法「删掉」一个数',
              '分解质因数再维护质因子个数也行，但实现麻烦，所以直接枚举',
              '`now` 向右每并入一个数就 `gcd`，等于 `k` 记一个；小于 `k` 就 break'],
        summary=['时间 `O(n^2)`（再乘 GCD 的对数），因为 `n ≤ 1000` 能过',
                 '左端点自己要先判断：`nums[i] % k != 0` 跳过、`== k` 先记 1 个',
                 '`now < k` 才能 break；`now` 一定始终是 k 的倍数，所以不会出现不整除的情况',
                 '对比灵神：灵神用 LogTrick 做到 `O(n log U)`，这里是朴素枚举'],
    ),
)
