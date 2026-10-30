def _txt(S):
    if 'i' not in S or 'suf_sum' not in S:
        return ''
    i, n = S['i'], S['n']
    cntr = n - 1 - i
    return f"`nums[{i}] × {cntr}` = =={S['nums'][i] * cntr}== 　对比 　后缀和 `suf_sum` = =={S['suf_sum']}=="


CONFIG = dict(
    num=3833, title='统计主导元素下标数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='倒序遍历 · 后缀和',
    tags=[],
    code='''
class Solution:
    def dominantIndices(self, nums: List[int]) -> int:
        n = len(nums)
        suf_sum = ans = 0
        for i in range(n - 2, -1, -1):
            suf_sum += nums[i + 1]
            if nums[i] * (n - 1 - i) > suf_sum:
                ans += 1
        return ans
''',
    call='Solution().dominantIndices([5, 4, 3, 8, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（框 = 右侧后缀 [i+1, n-1]）', pointers={'i': 'blue'},
             window=(lambda S: S['i'] + 1 if 'i' in S else None, lambda S: S['n'] - 1), cell=96, h=230,
             color=lambda S, i, v: 'green' if 'i' in S and i == S['i'] and S['_line'] == 8 else None),
        dict(type='text', h=110, size=32, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('suf_sum', 'suf_sum', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`，最右边的元素没有右侧，不算主导，所以 `i` 从 `n - 2` 开始',
        'suf_sum = ans = 0': '`suf_sum` 维护后缀 `[i+1, n-1]` 的元素和，`ans` 计数',
        'for i in range': lambda S, B, r: (f'倒着遍历：现在看下标 `i = {S.i}`，值 `{S.nums[S.i]}`' if 'i' not in B or S.i != B.i else '`i` 已经走完，遍历结束'),
        'suf_sum += nums[i + 1]': '后缀向左扩一格，加入 `nums[{i + 1}] = {nums[i + 1]}` → `suf_sum = {suf_sum}`',
        'if nums[i] * (n - 1 - i) > suf_sum': lambda S, B, r: (
            f'平均值比较改成乘法（避免小数）：`{S.nums[S.i]} × {S.n - 1 - S.i} = {S.nums[S.i] * (S.n - 1 - S.i)}` '
            + (f'> `{S.suf_sum}` → ==是主导元素==' if S.nums[S.i] * (S.n - 1 - S.i) > S.suf_sum else f'≤ `{S.suf_sum}` → 不是主导元素')),
        'ans += 1': '主导元素 +1 → `ans = {ans}`',
        'return ans': '共 `{ans}` 个主导元素',
    },
    max_steps=60,
    cards=dict(
        one_liner='倒着遍历，用后缀和把「大于平均数」换成乘法比较',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[i]` 严格大于右侧所有数的平均值，就是主导元素；最右边不算',
                 '统计主导元素的下标个数',
                 '示例：`[5,4,3]` → `2`；本视频：`[5,4,3,8,1]` → `2`'],
        quote='倒着遍历 nums，用一个变量 sufSum 维护后缀 [i+1,n-1] 的元素和。如果发现 nums[i]·(n-1-i) > sufSum，那么答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后缀 `[i+1, n-1]` 有 `n-1-i` 个数，平均值 = 和 ÷ 个数',
              '`nums[i] > 平均值` 两边乘个数，等价于 `nums[i] × (n-1-i) > 后缀和`',
              '`i` 从右往左走，后缀和每步只加一个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`i` 从 `n - 2` 开始，最右边元素没有右侧、不算',
                 '用乘法代替除法，避免浮点误差；是严格大于',
                 '后缀和技巧：倒着遍历时边走边累加，不用额外数组'],
    ),
)
