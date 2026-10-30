CONFIG = dict(
    num=2765, title='最长交替子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1581'],
    code='''
class Solution:
    def alternatingSubarray(self, nums: List[int]) -> int:
        ans = -1
        i, n = 0, len(nums)
        while i < n - 1:
            if nums[i + 1] - nums[i] != 1:
                i += 1  # 直接跳过
                continue
            i0 = i  # 记录这一组的开始位置
            i += 2  # i 和 i+1 已经满足要求，从 i+2 开始判断
            while i < n and nums[i] == nums[i - 2]:
                i += 1
            # 从 i0 到 i-1 是满足题目要求的（并且无法再延长的）子数组
            ans = max(ans, i - i0)
            i -= 1
        return ans
''',
    call='Solution().alternatingSubarray([7,3,4,3,4,5,4,5,4])',
    expect=5,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'i0': 'pink'}, window=('i0', 'i - 1'), h=300,
             label='nums（粉 = 这一组的起点 i0，蓝 = i，框 = 当前组 i0..i-1）'),
        dict(type='text', fn=lambda S: f"当前组 `[{S['i0']}, {S['i'] - 1}]`，长度 `{S['i'] - S['i0']}`" if 'i0' in S and S['i'] > S['i0'] else ''),
    ],
    watch=[('i', 'i', 'blue'), ('i0', 'i0', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '没有交替子数组就返回 `-1`，先设成 `-1`',
        'i, n = 0': '`i` 从 0 开始扫，`n = {n}`',
        'while i < n - 1': '外层循环：每一轮处理一组；`i < n - 1` 保证 `i+1` 不越界',
        'if nums[i + 1] - nums[i] != 1': '`nums[{i+1}] - nums[{i}] = {nums[i+1] - nums[i]}`，{"不是 1 → 这里起不了头" if nums[i+1] - nums[i] != 1 else "恰好是 1 → 可以作为一组的开头"}',
        '直接跳过': '起不了头，直接跳过：`i` → {i}',
        'i0 = i': '记下这一组的开始位置 `i0 = {i0}`',
        'i += 2': '`i0` 和 `i0+1` 已经满足 +1，从 `i = {i}` 开始检查',
        'while i < n and': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}`，`nums[{S.i-2}] = {S.nums[S.i-2]}`，相等 → 交替规律成立，继续延长'
                                           if S.i < S.n and S.nums[S.i] == S.nums[S.i - 2]
                                           else (f'`nums[{S.i}] = {S.nums[S.i]} ≠ nums[{S.i-2}] = {S.nums[S.i-2]}` → 这一组到此为止'
                                                 if S.i < S.n else '`i` 到数组末尾 → 这一组结束')),
        'ans = max': '这一组 `[{i0}, {i-1}]` 长 `{i} - {i0} = {i - i0}`；`ans = max({B.ans}, {i - i0}) = {ans}`',
        'i -= 1': '==回退一格==：这一组最后一个数可能是下一组的第一个数（两组重叠一个元素），`i` → {i}',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='分组循环：外层找组头，内层把这一组吃到底',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最长的子数组 `s`：长度 ≥ 2，且按 `s0, s0+1, s0, s0+1, …` 交替',
                 '没有就返回 `-1`',
                 '示例：`[2,3,4,3,4]` → `4`（`[3,4,3,4]`）'],
        quote='内层循环负责遍历组，找出这一组最远在哪结束。……这个写法是所有写法中最不容易出 bug 的，推荐大家记住。',
        quote_src='—— 灵茶山艾府题解',
        idea=['外层：记录组的开始位置 `i0`，组结束后更新答案',
              '内层：组头确定后，后面的数必须满足 `nums[i] == nums[i-2]`',
              '相邻两组会重叠一个元素，所以外层末尾 `i -= 1`'],
        summary=['时间 `O(n)`：`i` 回退的次数是 `O(n)` 的，所以双重循环总共仍是线性',
                 '易错点：忘记 `i -= 1`，会漏掉 `[3,4,3,4,5,4,5]` 里的第二组',
                 '没有找到任何组时 `ans` 保持 `-1`',
                 '同类题：1446、2110、2760、978（都是分组循环）'],
    ),
)
