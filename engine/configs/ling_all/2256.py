def _f(S):
    i = S.get('i')
    if i is None or 'pre' not in S:
        return '平均差 = `|前缀平均 − 后缀平均|`，向下取整'
    n = len(S['nums'])
    if i == n - 1 and S.get('_line') is not None and S['_line'] > 12:
        return '最后一个下标：后缀为空，平均值视为 0'
    return f"前缀 `{S['pre']}//{i + 1}` = {S['pre'] // (i + 1)}，后缀 `{S['suf']}//{n - 1 - i}` = {S['suf'] // (n - 1 - i)}"


CONFIG = dict(
    num=2256, title='最小平均差', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 1395'],
    code='''
class Solution:
    def minimumAverageDifference(self, nums: List[int]) -> int:
        ans = 0
        pre, suf, n = 0, 0, len(nums)
        for v in nums:
            suf += v  # 后缀和
        min_diff = inf
        for i, v in enumerate(nums[:n - 1]):
            pre += v  # 前缀和
            suf -= v  # 后缀和
            d = abs(pre // (i + 1) - suf // (n - 1 - i))
            if d < min_diff:
                min_diff, ans = d, i
        if (pre + nums[n - 1]) // n < min_diff:
            ans = n - 1
        return ans
''',
    call='Solution().minimumAverageDifference([2,5,3,9,5,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 前缀，其余 = 后缀）', cell=84, h=190,
             pointers={'i': 'blue'}, window=(lambda S: 0, 'i'),
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='text', fn=_f, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'cyan'), ('suf', 'suf', 'orange'), ('d', 'd', 'pink'),
           ('min_diff', 'min_diff', 'yellow'), ('ans', 'ans', 'green')],
    skip=['ans = 0', 'for v in nums:'],
    captions={
        'pre, suf, n': '`pre` 前缀和、`suf` 后缀和，先都为 0；`n = {n}`',
        'suf += v': '先把所有数加起来当作后缀和：`suf` = {suf}',
        'min_diff = inf': '`min_diff` 记录目前最小的平均差，初始为无穷大',
        'for i, v in enumerate': lambda S, B, r: (f'枚举分割点 `i = {S.i}`，只枚举到 `n-2`，最后一个下标单独处理'
                                                   if S.get('i') != B.get('i') or S.get('v') != B.get('v') else '前 `n-1` 个下标枚举完，接着单独处理最后一个下标'),
        'pre += v': '`nums[{i}] = {v}` 划入前缀：`pre` = =={pre}==',
        'suf -= v': '同一个数从后缀移出：`suf` = =={suf}==',
        'd = abs': '前缀平均 `{pre}//{i+1}` = {pre//(i+1)}，后缀平均 `{suf}//{n-1-i}` = {suf//(n-1-i)}，差 `d` = =={d}==',
        'if d < min_diff': '`d = {d}` {"<" if d < min_diff else "≥"} `min_diff = {min_diff}`：'
                           '{"更小，更新" if d < min_diff else "不更小（相等取下标小的）"}',
        'min_diff, ans = d, i': '`min_diff` → =={min_diff}==，`ans` → =={ans}==',
        'if (pre + nums[n - 1])': '最后一个下标：后缀为空（平均 0），前缀平均 `{(pre+nums[n-1])//n}` 对比 `min_diff = {min_diff}`',
        'ans = n - 1': '最后一个下标更优，`ans = {ans}`',
        'return ans': '平均差最小的下标是 `{ret}`',
    },
    cards=dict(
        one_liner='边枚举边维护前缀和，后缀和 = 总和 − 前缀和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['下标 `i` 的平均差 = ==前 i+1 个数的平均值== 与 ==后 n-i-1 个数的平均值== 的绝对差（向下取整）',
                 '空后缀的平均值视为 0；差相等时返回最小的下标',
                 '示例：`[2,5,3,9,5,3]` → `3`'],
        quote='前缀和、后缀和：先把所有数加到 suf，枚举时 pre += v、suf -= v。',
        quote_src='—— 灵茶山艾府题解（代码注释）',
        idea=['先算整个数组的和当作后缀和 `suf`，前缀和 `pre` 为 0',
              '每枚举一个数：它从后缀移到前缀，`O(1)` 算出两个平均值',
              '`i = n-1` 时后缀为空，除数会为 0，所以放到循环外单独判断'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python：`/` 为整数除法 → `//`，`math.MaxInt64` → `inf`，`abs` 用内置函数',
                 '易错点：最后一个下标后缀为空，不能除以 0；相等时要保留更小的下标（所以用严格小于）',
                 '同类题：前后缀分解专题'],
    ),
)
