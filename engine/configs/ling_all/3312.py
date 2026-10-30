CONFIG = dict(
    num=3312, title='查询排序后的最大公约数', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='倍数统计 · 倒序容斥 + 前缀和二分',
    tags=['灵神题单·数学算法', '难度分 2533'],
    code='''
class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        mx = max(nums)
        cnt_x = [0] * (mx + 1)
        for x in nums:
            cnt_x[x] += 1

        cnt_gcd = [0] * (mx + 1)
        for i in range(mx, 0, -1):
            c = 0
            for j in range(i, mx + 1, i):
                c += cnt_x[j]
                cnt_gcd[i] -= cnt_gcd[j]  # gcd 是 2i,3i,4i,... 的数对不能统计进来
            cnt_gcd[i] += c * (c - 1) // 2  # c 个数选 2 个，组成 c*(c-1)/2 个数对

        s = list(accumulate(cnt_gcd))  # 前缀和
        return [bisect_right(s, q) for q in queries]
''',
    call='Solution().gcdValues([2, 3, 4], [0, 2, 2])',
    expect=[1, 2, 2],
    views=[
        dict(type='array', var='cnt_x', label='cnt_x[v]：数 v 在 nums 中出现几次', cell=84, h=190,
             pointers={'j': 'pink'}, color=lambda S, i, v: 'cyan' if v else None),
        dict(type='array', var='cnt_gcd', label='cnt_gcd[g]：gcd 恰好等于 g 的数对个数', cell=84, h=190,
             pointers={'i': 'blue'}, color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='s', label='s[g]：gcd ≤ g 的数对个数（前缀和）', cell=84, h=190),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('c', 'c', 'cyan')],
    captions={
        'mx = max': '`gcd` 不会超过 `mx = {mx}`，所以按值域 `1..{mx}` 来统计',
        'cnt_x[x] += 1': '`cnt_x[{x}] = {cnt_x[x]}`：数 `{x}` 出现的次数',
        'cnt_gcd = [0]': '`cnt_gcd[g]`：gcd ==恰好==等于 `g` 的数对个数，先全 0',
        'for i in range(mx': '==倒序==枚举 `i`：算 `cnt_gcd[i]` 要用到 `cnt_gcd[2i], cnt_gcd[3i]...`，它们必须先算好',
        'c = 0': '`c` 统计 nums 中有多少个数是 `{i}` 的倍数',
        'for j in range(i, mx': '枚举 `{i}` 的倍数 `j = {j}`',
        'c += cnt_x[j]': '`{j}` 出现 `{cnt_x[j]}` 次 → 倍数个数 `c = {c}`',
        'cnt_gcd[i] -= cnt_gcd[j]': lambda S, B, r: (f'`j = i = {S.i}` 自己：此时 `cnt_gcd[{S.i}]` 还是 0，减 0 不变；真正的扣除从 `2i` 开始' if S.j == S.i else f'`cnt_gcd[{S.i}] -= cnt_gcd[{S.j}]`（= {S.cnt_gcd[S.j]}）：gcd 为 `{S.j}` 的数对也是 `{S.i}` 的倍数，但 gcd 不是 `{S.i}`，要扣掉 → `{S.cnt_gcd[S.i]}`'),
        'cnt_gcd[i] += c': '`c = {c}` 个倍数两两组合：`{c}×({c}−1)/2 = {c*(c-1)//2}` 对，gcd 都是 `{i}` 的倍数；扣掉更大的 → ==`cnt_gcd[{i}] = {cnt_gcd[i]}`==',
        's = list(accumulate': '前缀和 `s[g]` = gcd ≤ g 的数对总数。`gcdPairs` 升序，所以 gcd 等于 g 的数占下标 `[s[g-1], s[g]-1]`',
        'return [bisect_right': lambda S, B, ret: f'对每个 `q`：在 `s` 中二分找==严格大于 q 的第一个位置==，就是 gcdPairs[q] → 答案 `{ret}`',
    },
    cards=dict(
        one_liner='不排序数对：数每个 gcd 出现几次，再前缀和二分',
        complexity='时间 `O(n + (U+q) log U)`，空间 `O(U)`',
        problem=['`gcdPairs`：所有数对 `(nums[i], nums[j])` 的 gcd 升序排列',
                 '对每个 `queries[i]`，返回 `gcdPairs[queries[i]]`',
                 '示例：`nums=[2,3,4], queries=[0,2,2]` → `[1,2,2]`（gcdPairs = `[1,1,2]`）'],
        quote='直接把每个 GCD 分别出现多少次算出来，就方便回答询问了。……cntGcd[i] = c(c-1)/2 − cntGcd[2i] − cntGcd[3i] − ⋯',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 的倍数两两组合，gcd 都是 `i` 的倍数，==不一定恰好是 `i`==',
              '减去 gcd 为 `2i, 3i, ...` 的数对，才是恰好为 `i` 的 → ==倒序枚举 `i`==',
              '`cnt_gcd` 做前缀和 `s`，在 `s` 上二分严格大于 `q` 的第一个位置'],
        summary=['时间：二重循环是调和级数 `O(U log U)`，每个询问二分 `O(log U)`',
                 '易错点：`bisect_right` 找的是严格大于 `q` 的位置，下标直接就是 gcd 值',
                 '`cnt_gcd` 要用 `int`，`c*(c-1)//2` 在 `n=10^5` 时可达 5×10^9',
                 '同类：CF803F（子序列 gcd 恰好为 i）、CF990G（树上路径）'],
    ),
)
