CONFIG = dict(
    num=4010, title='数对的最大强度', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举数对 + 最优性剪枝',
    tags=['灵神题单', '数学算法', '难度分 1216'],
    code='''
class Solution:
    def maxPairStrength(self, nums: list[int]) -> int:
        nums.sort(reverse=True)
        all_gcd2 = gcd(*nums) ** 2

        ans = 0
        for i, x in enumerate(nums):
            for j in range(i):
                y = nums[j]
                mul = x * y
                if mul // all_gcd2 <= ans:  # 最优性优化
                    break
                g = gcd(x, y)
                ans = max(ans, mul // (g * g))
        return ans
''',
    call='Solution().maxPairStrength([4,6,8,9,12])',
    expect=72,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=260),
        dict(type='text', fn=lambda S: (f"`{S['x']} × {S['y']} = {S['mul']}`，`gcd = {S['g']}`，强度 = =={S['mul'] // (S['g']*S['g'])}==" if 'g' in S and 'mul' in S and 'y' in S and S.get('_line', 0) >= 11 else (f"上界：`mul // all_gcd2 = {S['mul'] // S['all_gcd2']}`" if 'mul' in S and 'all_gcd2' in S else '')), size=32),
    ],
    watch=['all_gcd2', 'x', 'y', 'mul', ('ans', 'ans', 'green')],
    captions={
        'nums.sort': '从大到小排序：越靠前乘积越大，后面才能提前停',
        'all_gcd2 =': '全体 GCD 的平方 `all_gcd2 = {all_gcd2}`：任何数对的 `gcd` 至少是 `allGcd`，所以强度 ≤ `mul // all_gcd2`',
        'for i, x': '外层取 `x = nums[{i}]`',
        'for j in range': '内层 `j` 从 0 到 `i-1`，只枚举排在 `x` 前面的数',
        'y = nums[j]': '`y = nums[{j}] = {y}`',
        'mul = x * y': '乘积 `mul = {x} × {y} = {mul}`',
        'if mul // all_gcd2': lambda S, B, r: (f'强度上界 `{S.mul} // {S.all_gcd2} = {S.mul // S.all_gcd2}` ≤ `ans = {S.ans}` → ==再往后只会更小，直接 break==' if S.mul // S.all_gcd2 <= S.ans else f'强度上界 `{S.mul // S.all_gcd2}` > `ans = {S.ans}` → 还可能更优，继续算'),
        'g = gcd': '`g = gcd({x}, {y}) = {g}`',
        'ans = max': '强度 `{mul} // {g}² = {mul // (g*g)}`，`ans = max({B.ans}, {mul // (g*g)}) = {ans}`',
        'return ans': '最大强度 `{ans}`',
    },
    cards=dict(
        one_liner='枚举数对算强度；从大到小排序，上界不超过 ans 就停',
        complexity='时间 `O(n² log U)`，空间 `O(1)`',
        problem=['选一对下标 `i != j`，强度 = `nums[i] * nums[j] / gcd(...)²`，求最大强度',
                 '示例：`[4,6,8]` → 选 6 和 8，`48 / 4 = 12`',
                 '本视频：`[4,6,8,9,12]` → `72`（8 和 9 互质，`72 / 1`）'],
        quote='从大到小枚举数对，如果 nums[i]·nums[j] / allGcd² ≤ ans，则继续枚举不可能让答案变大，跳出循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先排序，乘积随着往后枚举越来越小',
              '任何数对的 `gcd` 都不小于全体 GCD，所以强度 ≤ `mul // allGcd²`',
              '这个上界都不超过 `ans`，后面更小的数对就不用看了'],
        summary=['时间最坏 `O(n² log U)`，剪枝后通常快很多，空间 `O(1)`',
                 '优化前的写法是直接枚举所有数对，不排序不剪枝',
                 '`gcd(*nums)` 一次求出多个数的 GCD；`all_gcd2` 要平方',
                 '剪枝用 `<=`：上界等于 `ans` 也不可能更大'],
    ),
)
