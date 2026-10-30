def _top(S):
    ln = S.get('_line', 0)
    if 'i' not in S:
        return '枚举替换的位置 `i`：左边看 `pre`（以 i-1 结尾的最长），右边看 `suf`（以 i+1 开头的最长）'
    if ln <= 14:
        return '第一遍从右往左：`suf[i]` = 以 `nums[i]` 开头的最长非递减子数组'
    pre = S.get('pre')
    return f'第二遍从左往右：替换 `nums[{S["i"]}]`，左边 `pre = {pre}`，右边 `suf[{S["i"] + 1}] = {S["suf"][S["i"] + 1]}`'


def _sufc(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    if S.get('_line', 0) <= 14:
        return 'green' if k > i else ('blue' if k == i else None)
    return 'green' if k == i + 1 else None


CONFIG = dict(
    num=3738, title='替换至多一个元素后最长非递减子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解 · 枚举替换位置',
    tags=['分组循环', '状态机 DP', '难度分 1811'],
    code='''
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 1

        suf = [0] * n
        suf[-1] = 1
        ans = 2
        for i in range(n - 2, 0, -1):
            if nums[i] <= nums[i + 1]:
                suf[i] = suf[i + 1] + 1
                ans = max(ans, suf[i] + 1)  # 把 nums[i-1] 拼在 suf[i] 前面
            else:
                suf[i] = 1

        pre = 1
        for i in range(1, n - 1):
            if nums[i - 1] <= nums[i + 1]:
                ans = max(ans, pre + 1 + suf[i + 1])  # 替换 nums[i]
            if nums[i - 1] <= nums[i]:
                pre += 1
                ans = max(ans, pre + 1)  # 把 nums[i+1] 拼在 pre 后面
            else:
                pre = 1
        return ans
''',
    call='Solution().longestSubarray([1,2,5,3,4,2,6])',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='nums', label='nums', cell=96, h=230,
             pointers={'i - 1': 'pink', 'i': 'blue', 'i + 1': 'orange'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else None)),
        dict(type='array', var='suf', label='suf（以 nums[i] 开头的最长非递减子数组长度）', cell=96, h=230, index=False,
             color=_sufc),
        dict(type='text', fn=lambda S: (f"`ans = {S['ans']}`" if 'ans' in S else ''), size=26, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'if n == 1': '只有一个元素时，不用替换，长度就是 1',
        'suf = [0] * n': '`suf[i]`：以 `nums[i]` ==开头==的最长非递减子数组长度',
        'suf[-1] = 1': '最后一个数后面没有数，`suf[n-1] = 1`',
        'ans = 2': '`n ≥ 2`，把另一个数替换成相同的值，至少能得到 2',
        'for i in range(n - 2': lambda S, B, r: (f'倒着算 `suf`：`i = {S.i}`' if 'i' not in B or S.i != B.i else '`suf` 算完了'),
        'if nums[i] <= nums[i + 1]': lambda S, B, r: (f'`{S.nums[S.i]} ≤ {S.nums[S.i + 1]}` → `nums[{S.i}]` 能拼在 `suf[{S.i + 1}]` 前面'
                                                      if S.nums[S.i] <= S.nums[S.i + 1] else f'`{S.nums[S.i]} > {S.nums[S.i + 1]}` → 断开，`nums[{S.i}]` 只能自成一段'),
        'suf[i] = suf[i + 1] + 1': '`suf[{i}] = suf[{i + 1}] + 1 = {suf[i]}`',
        'ans = max(ans, suf[i] + 1)': '把 `nums[{i - 1}]` 替换成合适的值拼在前面：`ans = max({B.ans}, {suf[i]} + 1) = {ans}`',
        'suf[i] = 1': '断开了：`suf[{i}] = 1`',
        17: '`pre`：以 `nums[i-1]` 结尾的最长非递减子数组长度，起点 `pre = 1`',
        'for i in range(1, n - 1)': lambda S, B, r: (f'正着枚举替换位置 `i = {S.i}`' if B.get('i') != S.i or S.i == 1 else '枚举结束，不会再有更长的了'),
        'if nums[i - 1] <= nums[i + 1]': lambda S, B, r: (f'`{S.nums[S.i - 1]} ≤ {S.nums[S.i + 1]}` → 把 `nums[{S.i}]` 换成两者之间的数，左右两段能连起来'
                                                         if S.nums[S.i - 1] <= S.nums[S.i + 1] else f'`{S.nums[S.i - 1]} > {S.nums[S.i + 1]}` → 换一个数也连不起左右两段'),
        'ans = max(ans, pre + 1 + suf[i + 1])': '连起来的长度 = `pre + 1 + suf[{i + 1}]` = `{pre} + 1 + {suf[i + 1]}`，`ans = {ans}`',
        'if nums[i - 1] <= nums[i]': lambda S, B, r: (f'`{S.nums[S.i - 1]} ≤ {S.nums[S.i]}` → `pre` 可以延长到 `nums[{S.i}]`'
                                                      if S.nums[S.i - 1] <= S.nums[S.i] else f'`{S.nums[S.i - 1]} > {S.nums[S.i]}` → 左边这一段断了，`pre` 重新开始'),
        'pre += 1': '`pre` → {pre}',
        'ans = max(ans, pre + 1)': '把 `nums[{i + 1}]` 替换成 `nums[{i}]` 拼在 `pre` 后面：`ans = max({B.ans}, {pre} + 1) = {ans}`',
        25: '左边这一段断了，`pre` 重新从 1 开始',
        'return ans': '替换至多一个元素后，最长非递减子数组为 `{ans}`',
    },
    cards=dict(
        one_liner='枚举替换谁：左边最长 pre + 自己 + 右边最长 suf',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['最多把 `nums` 中的一个元素替换成任意整数',
                 '求替换后的==最长非递减子数组==长度',
                 '示例：`[1,2,5,3,4,2,6]` → `5`（把 5 换成 3，得 `1,2,3,3,4`）'],
        quote='枚举替换的元素是 nums[i]，我们需要知道什么？以 nums[i-1] 结尾的最长非递减子数组的长度 pre[i-1]；以 nums[i+1] 开头的最长非递减子数组的长度 suf[i+1]。',
        quote_src='—— 灵茶山艾府题解（方法一：前后缀分解）',
        idea=['若 `nums[i-1] ≤ nums[i+1]`，把 `nums[i]` 换成两者之间的数，得 `pre + 1 + suf`',
              '也可以换成 `nums[i-1]` 拼在 `pre` 后面，或换成 `nums[i+1]` 拼在 `suf` 前面',
              '`suf` 先倒着算出；`pre` 边枚举边维护，压成一个变量'],
        result='`pre + 1 + suf` 在 `i = 2` 时取到 `2 + 1 + 2 = 5` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（`suf` 数组）',
                 '先特判 `n == 1`，否则 `suf[-1]` 与循环范围都会出问题',
                 '三种拼接都要考虑：连两段、接在 pre 后、接在 suf 前',
                 '题解还给了分组循环和状态机 DP，本视频演示前后缀分解'],
    ),
)
