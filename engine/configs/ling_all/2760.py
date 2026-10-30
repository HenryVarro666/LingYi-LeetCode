CONFIG = dict(
    num=2760, title='最长奇偶子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环',
    tags=['分组循环', '难度分 1420'],
    code='''
class Solution:
    def longestAlternatingSubarray(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        ans = i = 0
        while i < n:
            if nums[i] > threshold or nums[i] % 2:
                i += 1  # 直接跳过
                continue
            start = i  # 记录这一组的开始位置
            i += 1  # 开始位置已经满足要求，从下一个位置开始判断
            while i < n and nums[i] <= threshold and nums[i] % 2 != nums[i - 1] % 2:
                i += 1
            # 从 start 到 i-1 是满足题目要求的（并且无法再延长的）子数组
            ans = max(ans, i - start)
        return ans
''',
    call='Solution().longestAlternatingSubarray([2,1,1,4,3,4,2,8], 5)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"`nums[{S['i']}] = {S['nums'][S['i']]}`：" + ('偶数' if S['nums'][S['i']] % 2 == 0 else '奇数') + ('，超过 threshold' if S['nums'][S['i']] > S['threshold'] else f"，不超过 {S['threshold']}")) if S.get('i') is not None and S['i'] < len(S['nums']) else '', size=30),
        dict(type='array', var='nums', pointers={'i': 'pink', 'start': 'blue'},
             window=(lambda S: S['start'], lambda S: max(S['start'], S['i'] - 1)), h=300, cell=90,
             color=lambda S, k, v: 'orange' if v > S['threshold'] else None,
             dim=lambda S, k, v: v > S['threshold']),
    ],
    watch=[('i', 'i', 'pink'), ('start', 'start', 'blue'), ('threshold', 'threshold', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = i = 0': '`i` 是扫描位置，只增不减；`ans` 记最长长度',
        'if nums[i] > threshold': lambda S, B, r: (f"`nums[{S.i}] = {S.nums[S.i]}`：" + ('超过 threshold' if S.nums[S.i] > S.threshold else '是奇数') + ' → 不能当起点' if (S.nums[S.i] > S.threshold or S.nums[S.i] % 2)
                                                  else f"`nums[{S.i}] = {S.nums[S.i]}` 是不超过 threshold 的偶数 → 可以当起点"),
        'i += 1  # 直接跳过': '不能当起点 → 跳过，`i` → {i}',
        'start = i': '==分组循环==：记下这一组的起点 `start = {start}`',
        'i += 1  # 开始位置': '起点已满足要求，从下一个位置开始判断',
        'while i < n and nums[i] <=': lambda S, B, r: ('`i` 到头了，这一组结束' if S.i >= S.n else
                                                         (f"`nums[{S.i}] = {S.nums[S.i]}` 不超过 {S.threshold}，奇偶性和前一个（{S.nums[S.i-1]}）不同 → 成立，组继续" if (S.nums[S.i] <= S.threshold and S.nums[S.i] % 2 != S.nums[S.i-1] % 2)
                                                          else f"`nums[{S.i}] = {S.nums[S.i]}`：" + ('超过 threshold' if S.nums[S.i] > S.threshold else f'和前一个 {S.nums[S.i-1]} 奇偶相同') + ' → 这一组最远到 `i-1`')),
        12: '这个数还在组里 → `i` → {i}，继续往右看',
        'ans = max': '这组是 `[{start}, {i-1}]`，长度 `{i - start}`，`ans = max({B.ans}, {i - start}) = {ans}`',
        'return ans': '最长奇偶子数组长度 `{ans}`',
    },
    cards=dict(
        one_liner='分组循环：外层找起点，内层把这一组走到头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最长子数组：首元素是偶数，奇偶交替，且所有元素都 `<= threshold`',
                 '示例：`[3,2,5,4]`，`threshold = 5` → `3`',
                 '本视频：`[2,1,1,4,3,4,2,8]`，`threshold = 5` → `3`'],
        quote='外层循环负责遍历组之前的准备工作（记录开始位置），和遍历组之后的统计工作（更新答案最大值）。内层循环负责遍历组，找出这一组最远在哪结束。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组被切成若干组，每组判断逻辑相同 → 分组循环模板',
              '外层：不合格的起点跳过；合格就记 `start`',
              '内层：`i` 往后走到违反条件为止，下一组直接从 `i` 开始，不必回退'],
        summary=['时间 `O(n)`，空间 `O(1)`：`i` 只增不减，二重循环总共 `O(n)`',
                 '好处：不用特判最后一组，是最不容易出 bug 的写法',
                 '起点要同时满足偶数和 `<= threshold`',
                 '同类题：1446、1869、1957、2110、228 等分组循环题'],
    ),
)
