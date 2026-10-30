def _a(S):
    return [x - y for x, y in zip(S['nums1'], S['nums2'])]


def _txt(S):
    if 'x' not in S or 'k' not in S:
        return ''
    x, k = S['x'], S['k']
    if k == 0:
        return '`k = 0`：不能操作，只能要求 `x == 0`'
    return f'差 `x = {x}`，`x % k = {x % k}`，`x // k = {x // k}`；累计 `sum = {S["sum"]}`，`ans = {S["ans"]}`'


CONFIG = dict(
    num=2541, title='使数组中所有元素相等的最小操作数 II', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='作差 · 倍数与总和判定',
    tags=['灵神题单', '数学算法', '难度分 1620'],
    code='''
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int], k: int) -> int:
        ans = sum = 0
        for x, y in zip(nums1, nums2):
            x -= y
            if k:
                if x % k: return -1
                sum += x // k
                if x > 0: ans += x // k
            elif x: return -1
        return -1 if sum else ans
''',
    call='Solution().minOperations([4,3,1,4], [1,3,7,1], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums1', label='nums1', h=170),
        dict(type='array', var='nums2', label='nums2', h=170),
        dict(type='array', var=lambda S: _a(S), label='a[i] = nums1[i] − nums2[i]（目标：全变 0）', h=200,
             color=lambda S, i, v: 'green' if v > 0 else 'pink' if v < 0 else None),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=['x', 'y', ('sum', 'sum', 'yellow'), ('ans', 'ans', 'green'), 'k'],
    captions={
        'ans = sum = 0': '`ans` 统计答案，`sum` 统计所有 `a[i] / k` 之和（应为 0）',
        'x -= y': '令 `a[i] = nums1[i] − nums2[i]`，现在 `x = {x}`：要把它变成 0',
        'if k:': '`k = {k}`，不为 0：可以放心取模、做除法',
        'if x % k': '每次只能改 `±k`，所以 `x` 必须是 `k` 的倍数：`{x} % {k} = {x % k}` → {"不行，返回 -1" if x % k else "通过"}',
        'sum += x // k': '`x` 需要 `{x // k}` 个 `k`（负数表示要减）→ `sum` = =={sum}==',
        'if x > 0': '只数正数：一次操作 +k 一个、−k 一个，负数那边是被顺带改的 → {"`x > 0`，`ans += " + str(x // k) + "`" if x > 0 else "`x ≤ 0`，不计入"}',
        'elif x': '`k = 0` 不能操作：`x = {x}` 不为 0 就无解',
        'return -1 if sum': '总和不变：`sum = {sum}`，{"不为 0 → 加减凑不平，返回 -1" if sum else "为 0 → 加减能配对，答案 ans = " + str(ans)}',
    },
    cards=dict(
        one_liner='作差后，正数的 x/k 之和就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：`nums1[i] += k`，`nums1[j] -= k`',
                 '求让 `nums1` 变成 `nums2` 的最少操作数，不行返回 `-1`',
                 '示例：`[4,3,1,4]`、`[1,3,7,1]`、`k=3` → `2`'],
        quote='由于「一个数 +k，另一个数 −k」这个操作不会影响整个 a[i] 的和，所以如果 a[i] 的和不为 0，也无法满足要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['令 `a[i] = nums1[i] − nums2[i]`，问题变成把每个 `a[i]` 变成 0',
              '`k = 0` 不能操作；`k > 0` 时每个 `a[i]` 必须是 `k` 的倍数，且总和为 0',
              '每次操作配一正一负，==只数正数的 `a[i]/k`== 就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`k = 0` 要单独判：不能取模，`x != 0` 就返回 -1',
                 '总和判定用 `sum` 累加 `x // k`，负数也要加',
                 '变量名 `sum` 覆盖了内置函数，原文如此'],
    ),
)
