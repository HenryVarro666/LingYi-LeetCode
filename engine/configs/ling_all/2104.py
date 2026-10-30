def _p2(S):
    return bool(S.get('nums')) and S['nums'][0] < 0


def _top(S):
    if 'left' not in S or 'right' not in S:
        return '把每个元素当「最大值」，数它出现在多少个子数组里'
    p = '第 2 轮：nums 取反，算「最小值」的贡献' if _p2(S) else '第 1 轮：算每个元素作为「最大值」的贡献'
    if S['_line'] == 17 and 'i' in S and 'v' in S:
        i = S['i']
        return f"`({i} − ({S['left'][i]})) × ({S['right'][i]} − {i}) × {S['nums'][i]}` = =={(i - S['left'][i]) * (S['right'][i] - i) * S['nums'][i]}=="
    return p


def _inpop(S):
    return S['_line'] in (16, 17, 18)


def _ncolor(S, i, v):
    if 'i' not in S or 'left' not in S or 'right' not in S or S['_line'] != 17:
        return None
    if i == S['i']:
        return 'blue'
    if S['left'][S['i']] < i < S['right'][S['i']]:
        return 'cyan'
    return None


CONFIG = dict(
    num=2104, title='子数组范围和', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 + 贡献法（Go 原文转写）',
    tags=['灵神题单', '单调栈', '难度分 2000'],
    code='''
class Solution:
    def solve(self, nums: List[int]) -> int:
        ans = 0
        n = len(nums)
        left = [0] * n  # left[i] 为左侧严格大于 num[i] 的最近元素位置（不存在时为 -1）
        right = [0] * n  # right[i] 为右侧大于等于 num[i] 的最近元素位置（不存在时为 n）
        for i in range(n):
            right[i] = n
        st = [-1]
        for i, v in enumerate(nums):
            while len(st) > 1 and nums[st[-1]] <= v:
                right[st[-1]] = i
                st.pop()
            left[i] = st[-1]
            st.append(i)
        for i, v in enumerate(nums):
            ans += (i - left[i]) * (right[i] - i) * v
        return ans

    def subArrayRanges(self, nums: List[int]) -> int:
        ans = self.solve(nums)
        for i, v in enumerate(nums):  # 小技巧：所有元素取反后算的就是最小值的贡献
            nums[i] = -v
        return ans + self.solve(nums)
''',
    call='Solution().subArrayRanges([1,3,2])',
    expect=5, max_steps=110,
    skip=['ans = 0', 'n = len(nums)', 'right[i] = n', 'for i in range(n)'],
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var='nums', pointers={'i': 'blue'}, label='nums（蓝 = 当前元素，青 = 它当最大值能覆盖的范围）', h=200, cell=80, color=_ncolor),
        dict(type='array', var='left', pointers={'i': 'blue'}, label='left（左侧严格更大的最近位置）', h=170, cell=80),
        dict(type='array', var='right', pointers={'i': 'blue'}, label='right（右侧大于等于的最近位置）', h=170, cell=80),
        dict(type='stack', var='st', label='单调栈 st（存下标，栈底哨兵 -1）', h=200, fmt=lambda x: str(x)),
    ],
    watch=['i', 'v', ('ans', 'ans', 'green')],
    captions={
        'left = [0]': '`left[i]`：左侧==严格大于==它的最近位置，没有则 `-1`',
        'right = [0]': '`right[i]`：右侧==大于等于==它的最近位置，没有则 `n`',
        'st = [-1]': '栈里放下标，先放哨兵 `-1`（表示左边没有更大的）',
        'while len(st) > 1': lambda S, B, r: (f'栈顶 `nums[{S.st[-1]}] = {S.nums[S.st[-1]]}` <= `{S.v}` → ==弹出==，它右边第一个不小于它的就是 `i = {S.i}`' if len(S.st) > 1 and S.nums[S.st[-1]] <= S.v else (f'栈里只剩哨兵，不再弹' if len(S.st) <= 1 else f'栈顶 `nums[{S.st[-1]}] = {S.nums[S.st[-1]]}` > `{S.v}`，停止弹出')),
        'right[st[-1]] = i': '`right[{B.st[-1]}] = {i}`：被弹出的元素，右边第一个 >= 它的是 `i`',
        'st.pop()': '弹出栈顶，`st = {st}`',
        'left[i] = st[-1]': '栈顶就是左侧严格更大的最近元素：`left[{i}] = {left[i]}`',
        'st.append(i)': '`i` 入栈：`st = {st}`',
        'ans += ': '`nums[{i}]` 作最大值的子数组数 `({i} − ({left[i]})) × ({right[i]} − {i})` = {(i - left[i]) * (right[i] - i)}，贡献 `{(i - left[i]) * (right[i] - i) * v}` → `ans = {ans}`',
        'return ans + self.solve': '最大值之和 `{B.ans}`；再对取反后的 nums 算一遍，得到最小值之和的相反数，两者相加',
        'return ans': '这一轮的贡献和 `{ans}`',
        'ans = self.solve(nums)': '第 1 轮：每个元素作==最大值==的总贡献',
        'nums[i] = -v': '`nums[{i}]` 取反 → {nums[i]}：取反后的最大值就是原来的最小值',
    },
    cards=dict(
        result='最大值之和 `15` + 取反后的 `-10` = ==5==',
        one_liner='不枚举子数组，而是数每个元素当最大值/最小值的次数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的「范围」= 最大值 − 最小值，求所有子数组范围之和',
                 '示例：`[1,3,2]` → 6 个子数组，范围和 `5`',
                 '进阶：能否做到 `O(n)`'],
        quote='我们可以考虑每个元素作为最大值出现在了多少子数组中，以及作为最小值出现在了多少子数组中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`left[i]`：左侧严格大于；`right[i]`：右侧大于等于 → 重复元素不重复统计',
              '`nums[i]` 当最大值的子数组数 `(i − left[i]) × (right[i] − i)`',
              '小技巧：所有元素取反，同一份代码就算出最小值的贡献（带负号）'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；灵神还给了 `O(n²)` 暴力写法，本视频用单调栈写法',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：一侧严格、一侧不严格，否则相等元素会重复计数',
                 '思考题：改成子序列就是 891. 子序列宽度之和',
                 '同类题：907. 子数组的最小值之和（贡献法）'],
    ),
)
