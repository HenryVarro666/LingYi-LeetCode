def _txt(S):
    ln = S.get('_line', 0)
    if ln in (17, 18):
        return (f"以 `{S['num']}` 为最小值：左右边界 `({S['l']}, {S['r']})`，长度 `k = {S['k']}`；"
                f"要 `{S['num']} > {S['threshold']}//{S['k']} = {S['threshold'] // S['k']}`")
    if ln >= 16:
        return '第三遍：逐个把元素当最小值，检查它撑起的最长子数组'
    if ln >= 10:
        return '第二遍：从右往左的单调栈，求右边界'
    return '第一遍：从左往右的单调栈，求左边界'


def _pop_cap(side):
    def f(S, B, ret):
        nums = S['nums']
        st0 = []
        order = range(S['i']) if side == 'L' else range(len(nums) - 1, S['i'], -1)
        for j in order:  # 重放前面的入栈出栈，得到进入本轮 while 之前的栈
            while st0 and nums[st0[-1]] >= nums[j]:
                st0.pop()
            st0.append(j)
        st1 = S['st']
        popped = st0[len(st1):] if len(st1) < len(st0) else []
        cur = S['v'] if side == 'L' else S['nums'][S['i']]
        pre = '、'.join(f"nums[{j}]={S['nums'][j]}" for j in reversed(popped))
        if popped:
            head = f"栈顶 {pre} 都 `>= {cur}`：它们不可能是 `{cur}` 的「更小」邻居，==弹出==；"
        else:
            head = f"栈顶 `>= {cur}` 的一个也没有，不用弹；"
        if st1:
            j = st1[-1]
            return head + f"栈顶 `nums[{j}] = {S['nums'][j]}` 严格小于 `{cur}`，是最近的更小元素"
        return head + '栈空了，这一侧没有更小的元素'
    return f


CONFIG = dict(
    num=2334, title='元素值大于变化阈值的子数组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='单调栈求最小值的左右边界',
    tags=['单调栈', '难度分 2381'],
    code='''
class Solution:
    def validSubarraySize(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        left, st = [-1] * n, []  # left[i] 为左侧小于 nums[i] 的最近元素位置（不存在时为 -1）
        for i, v in enumerate(nums):
            while st and nums[st[-1]] >= v: st.pop()
            if st: left[i] = st[-1]
            st.append(i)

        right, st = [n] * n, []  # right[i] 为右侧小于 nums[i] 的最近元素位置（不存在时为 n）
        for i in range(n - 1, -1, -1):
            while st and nums[st[-1]] >= nums[i]: st.pop()
            if st: right[i] = st[-1]
            st.append(i)

        for num, l, r in zip(nums, left, right):
            k = r - l - 1
            if num > threshold // k: return k
        return -1
''',
    call='Solution().validSubarraySize([1,3,4,3,1], 6)',
    expect=3,
    views=[
        dict(type='text', h=50, fn=_txt),
        dict(type='array', var='nums', label='nums', h=150,
             window=(lambda S: S['l'] + 1 if S.get('_line') in (17, 18) and 'l' in S else None,
                     lambda S: S['r'] - 1 if S.get('_line') in (17, 18) and 'r' in S else None),
             color=lambda S, j, v: ('blue' if S.get('i') == j else None) if S.get('_line', 0) < 16 else (
                 'pink' if S.get('_line') in (17, 18) and S['l'] < j < S['r'] and v == S['num'] and j == S['nums'].index(v, S['l'] + 1) else None)),
        dict(type='stack', var='st', h=90, fmt=lambda i: str(i)),
        dict(type='array', var='left', label='left', h=100),
        dict(type='array', var='right', label='right', h=100),
    ],
    watch=['i', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('k', 'k', 'yellow'), 'threshold'],
    captions={
        'while st and nums[st[-1]] >= v': _pop_cap('L'),
        'while st and nums[st[-1]] >= nums[i]': _pop_cap('R'),
        'left, st = ': '`left` 先全设为 -1（没有更小元素），`st` 是空栈',
        'right, st = ': '`right` 先全设为 n，`st` 清空，这次从右往左扫',
        'for i in range(n - 1': lambda S, B, ret: ('从右往左扫完了，`right` 全部求好' if S['st'] and S['i'] == B.get('i') else f"从右往左：`i = {S['i']}`"),
        'if st: left[i]': lambda S, B, ret: (f"栈顶 `{S['st'][-1]}` 就是左边界：`left[{S['i']}] = {S['left'][S['i']]}`" if S['st'] else f"栈空 → `left[{S['i']}]` 保持 -1"),
        'if st: right[i]': lambda S, B, ret: (f"栈顶 `{S['st'][-1]}` 就是右边界：`right[{S['i']}] = {S['right'][S['i']]}`" if S['st'] else f"栈空 → `right[{S['i']}]` 保持 n = {S['n']}"),
        'st.append': '下标 `{i}` 入栈',
        'k = r - l - 1': '最小值 `{num}`，它撑起的子数组：开区间 `({l}, {r})`，长度 `k = {r} - ({l}) - 1 = {k}`',
        'if num > threshold': lambda S, B, ret: (
            f"子数组每个数都 `>= {S['num']}`，只要最小值 `{S['num']} > threshold/k = {S['threshold']}//{S['k']} = {S['threshold'] // S['k']}` 就全满足 → ==成立，返回 k = {S['k']}=="
            if S['num'] > S['threshold'] // S['k'] else
            f"`{S['num']} > {S['threshold']}//{S['k']} = {S['threshold'] // S['k']}` 不成立：最小值太小，这个长度不行，换下一个元素"),
        'return -1': '所有最小值都不满足，返回 `-1`',
    },
    cards=dict(
        one_liner='枚举最小值，单调栈给出它能撑起的最长子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找一个长度为 `k` 的子数组，每个元素都 `> threshold / k`，返回任意一个合法的 `k`，没有则返回 `-1`',
                 '示例：`nums=[1,3,4,3,1], threshold=6` → `3`（`[3,4,3]` 每个都 `> 2`）'],
        quote='枚举每个元素，假设它是子数组中的最小值。子数组的左右边界最远能到哪？用单调栈来计算左右边界。',
        quote_src='—— 灵茶山艾府题解 方法二',
        idea=['`nums[i]` 当最小值时，子数组越长越容易满足 `> threshold/k`，所以取最长的 `k = r - l - 1`',
              '左边界 `left`、右边界 `right` 是两侧最近的更小元素，用单调栈各扫一遍',
              '只要 `nums[i] > threshold // k`，整段每个元素（都 `>= nums[i]`）就全部合法'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：用 `threshold // k` 比较（整数除法），`num > threshold // k` 与 `num * k > threshold` 等价',
                 '弹栈用 `>=`，保证栈里留下的是严格更小的元素',
                 '另一种写法：按值从大到小加入元素，并查集维护连续段长度（方法一，`O(n log n)`）'],
    ),
)
