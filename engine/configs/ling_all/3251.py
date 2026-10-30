def _txt(S):
    if 'cur' not in S:
        return '`f[j]` = 下标 0..i 中 `arr1[i] = j` 的单调数组对个数'
    pre, cur, j0 = S['pre'], S['cur'], S.get('j0')
    if j0 is None:
        return f'处理 `nums[i-1] = {pre}` → `nums[i] = {cur}`'
    return f'`j0 = max({cur} − {pre}, 0)` = =={j0}==：`arr1` 至少要涨 `{j0}`，所以 `j < {j0}` 的状态全为 0'


CONFIG = dict(
    num=3251, title='单调数组对的数目 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前缀和优化 DP · 一维滚动',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2323'],
    code='''
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        m = nums[-1]
        f = [0] * (m + 1)
        for j in range(min(nums[0], m) + 1):
            f[j] = 1
        for pre, cur in pairwise(nums):
            j0 = max(cur - pre, 0)
            m2 = min(cur, m)
            if j0 > m2:
                return 0
            for j in range(1, m2 - j0 + 1):
                f[j] = (f[j] + f[j - 1]) % MOD  # 计算前缀和
            f[j0: m2 + 1] = f[:m2 - j0 + 1]
            f[:j0] = [0] * j0
        return sum(f) % MOD
''',
    call='Solution().countOfPairs([2,4,3,3])',
    expect=5,
    skip=['MOD = 1_000_000_007'],
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=80),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='f', label='f[j]：arr1[i] = j 的方案数', h=260, cell=80, pointers={'j': 'yellow'}),
    ],
    watch=[('pre', 'pre', 'blue'), ('cur', 'cur', 'pink'), ('j0', 'j0', 'orange'), ('m2', 'm2', 'cyan')],
    captions={
        'm = nums[-1]': '`m = nums[-1] = {m}`：答案只看 `arr1[n-1] ≤ m` 的状态，所以 `f` 只开 `m+1` 格',
        'f = [0] * (m + 1)': '`f[j]`：当前下标处 `arr1 = j` 的方案数，先全 0',
        'f[j] = 1': '下标 0：`arr1[0]` 取 `0..nums[0]` 都行，各 1 种 → `f[{j}] = 1`',
        'for pre, cur in pairwise': lambda S, B, r: ('相邻两项都处理完了' if B.get('cur') == S.cur and B.get('pre') == S.pre
                                                    else f'看相邻两项：`pre = {S.pre}`，`cur = {S.cur}`；==从 pre 位转移到 cur 位=='),
        'j0 = max': '`arr1` 涨幅至少 `cur − pre`（否则 `arr2` 会变大）：`j0 = max({cur} − {pre}, 0)` = =={j0}==',
        'm2 = min': '`j` 最多到 `min(cur, m) = {m2}`',
        'if j0 > m2': '`j0 = {j0} > m2 = {m2}`？{"是 → 无解，返回 0" if j0 > m2 else "否，继续"}',
        '# 计算前缀和': '`f[{j}] += f[{j-1}]` → {f[j]}：==前缀和==，因为新 `f[j]` 是旧 `f[0..j-j0]` 之和',
        'f[j0: m2 + 1] =': '整体右移 `j0 = {j0}` 格：新 `f[j] = 旧前缀和 s[j − {j0}]`',
        'f[:j0] = ': '`j < {j0}` 的状态不可能，清零',
        'return sum(f)': '`arr1[n-1]` 取 `0..m` 的方案数全加起来 = =={ret}==',
    },
    cards=dict(
        one_liner='f[j] 记 arr1 取 j 的方案数，转移是前缀和再右移',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['`arr1` 非递减，`arr2` 非递增，且 `arr1[i] + arr2[i] = nums[i]`，求数组对个数（模 `10^9+7`）',
                 '示例：`nums = [2,3,2]` → `4`；`[5,5,5,5]` → `126`',
                 '本视频：`nums = [2,4,3,3]` → `5`'],
        quote='考虑枚举 arr1[i-1] = k，那么必须满足 k ≤ j 且 nums[i-1]-k ≥ nums[i] - j。……其中和式可以用前缀和优化。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['只枚举 `arr1`，`arr2 = nums − arr1` 自动确定',
              '`f[i][j]` = 前 `i` 个位置、`arr1[i] = j` 的方案数；转移是 `f[i-1][0..maxK]` 之和',
              '化简后 `f[i][j] = s[j − j0]`：前缀和后整体右移 `j0` 格，再用一维数组倒着滚动'],
        summary=['时间 `O(nm)`，`m = nums[n-1]`；空间 `O(m)`',
                 '易错：`f` 只开 `nums[-1]+1`，所以要 `min(cur, m)`；`j0 > m2` 时直接返回 0',
                 '这里选的是题解「进一步优化」写法；方法一是二维 `f` 再用 `accumulate` 前缀和',
                 '方法二是组合数学：`C(m+n, n)`，其中 `m = nums[-1] − Σmax(nums[i]−nums[i-1], 0)`'],
    ),
)
