def _text(S):
    if 'suf_min' not in S or 'i' not in S:
        return f"总和 `sum(nums) = {S['pre_sum']}`" if 'pre_sum' in S else ''
    sm = S['suf_min']
    smt = '∞' if sm == inf else sm
    if S['_line'] >= 9 and sm != inf:
        return f"分割点 `{S['i'] - 1}`：前缀和 `{S['pre_sum']}` − 后缀最小 `{smt}` = =={S['pre_sum'] - sm}=="
    return f"前缀和 `pre_sum = {S['pre_sum']}`，后缀最小值 `suf_min = {smt}`"


CONFIG = dict(
    num=3788, title='分割的最大得分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 倒序撤销前缀和',
    tags=['灵神题单', '动态规划', '难度分 1306'],
    code='''
class Solution:
    def maximumScore(self, nums: List[int]) -> int:
        ans = -inf
        pre_sum = sum(nums)
        suf_min = inf
        for i in range(len(nums) - 1, 0, -1):  # 保证前缀至少有一个数
            pre_sum -= nums[i]  # 撤销
            suf_min = min(suf_min, nums[i])
            ans = max(ans, pre_sum - suf_min)
        return ans
''',
    call='Solution().maximumScore([10,-1,3,-4,-5])',
    expect=17,
    views=[
        dict(type='text', fn=_text, size=28),
        dict(type='array', var='nums', label='nums（蓝 = 前缀，橙 = 后缀）', h=420,
             pointers={'i': 'pink'},
             color=lambda S, i, v: None if 'i' not in S or 'suf_min' not in S or S['_line'] < 8 else ('orange' if i >= S['i'] else 'blue')),
    ],
    watch=[('pre_sum', 'pre_sum', 'blue'), ('suf_min', 'suf_min', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'pre_sum = sum': '先算总和 `pre_sum = {pre_sum}`：此时「前缀」是整个数组，后面从右往左一个个撤销',
        'pre_sum -= ': '`i = {i}`：把 `nums[{i}] = {nums[i]}` 从前缀里撤销（加法可逆）：`pre_sum = {B.pre_sum} - ({nums[i]}) = {pre_sum}`，它改归后缀',
        'suf_min = min': '后缀加入 `nums[{i}] = {nums[i]}`：`suf_min = min({B.suf_min}, {nums[i]}) = {suf_min}`（min 不可逆，所以只能从右往左累积）',
        'ans = max': '分割在 `{i - 1}` 与 `{i}` 之间：得分 `{pre_sum} - ({suf_min}) = {pre_sum - suf_min}`，`ans = max({B.ans}, {pre_sum - suf_min}) = {ans}`',
        'return ans': '循环到 `i = 1` 为止，保证前缀至少一个数；最大得分 ==`{ans}`==',
    },
    cards=dict(
        one_liner='倒着走：min 往后缀累积，sum 从总和里扣掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选下标 `i`（`0 <= i < n-1`）把数组切成前缀和后缀',
                 '得分 = 前缀和 − 后缀最小值，求最大得分',
                 '示例：`[10,-1,3,-4,-5]` → `17`（在 `i=2` 切：`12 - (-5)`）'],
        quote='计算 min 不可逆，但计算加法可逆（减法）。我们可以先计算整个数组的总和，再倒着遍历 nums，在计算后缀最小值的同时，从总和中减去 nums[i]，就得到了前缀和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['朴素写法：开 `suf_min` 数组存后缀最小值，再正着枚举（优化前）',
              '优化：先 `sum(nums)`，倒着遍历时 `pre_sum -= nums[i]`，同时更新 `suf_min`',
              '这样不需要数组，空间从 `O(n)` 降到 `O(1)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：循环到 `i = 1` 结束（`range(n-1, 0, -1)`），保证前缀至少一个数',
                 '先「撤销」`pre_sum`，再更新 `suf_min`，两者都含 `nums[i]` 的归属要对齐',
                 '得分可能为负，所以 `ans` 初值用 `-inf` 而不是 0'],
    ),
)
