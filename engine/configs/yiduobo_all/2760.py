CONFIG = dict(
    num=2760, title='最长奇偶子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='找起点 · 向右扩展',
    tags=['分组循环', '难度分 1420'],
    code='''
class Solution(object):
    def longestAlternatingSubarray(self, nums, threshold):

        left = 0
        res = 0
        while left < len(nums):
            while left < len(nums) and (nums[left] > threshold or nums[left] % 2 == 1):
                left += 1
        
            if left == len(nums):
                return res
        
            right = left + 1
            while right < len(nums) and nums[right] <= threshold and (nums[right - 1] + nums[right]) % 2 == 1:
                right += 1

            res = max(res, right - left)
            left = right
        
        return res
''',
    call='Solution().longestAlternatingSubarray([2,1,1,4,3,4,2,8], 5)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"`nums[{S['left']}] = {S['nums'][S['left']]}`：" + ('偶数' if S['nums'][S['left']] % 2 == 0 else '奇数') + ('，超过 threshold' if S['nums'][S['left']] > S['threshold'] else f"，不超过 {S['threshold']}")) if S.get('left') is not None and S['left'] < len(S['nums']) else '', size=30),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', lambda S: max(S['left'], S['right'] - 1) if 'right' in S else S['left']), h=300, cell=90,
             color=lambda S, k, v: 'orange' if v > S['threshold'] else None,
             dim=lambda S, k, v: v > S['threshold']),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('threshold', 'threshold', 'orange'), ('res', 'res', 'green')],
    captions={
        'left = 0': '`left` 是候选子数组的起点',
        'res = 0': '`res` 记最长长度',
        'while left < len(nums) and (': lambda S, B, r: ('`left` 到头了' if S.left >= len(S.nums) else
                                                         (f"`nums[{S.left}] = {S.nums[S.left]}`：" + ('超过 threshold' if S.nums[S.left] > S.threshold else '是奇数') + ' → 不能当起点，继续找' if (S.nums[S.left] > S.threshold or S.nums[S.left] % 2 == 1)
                                                          else f"`nums[{S.left}] = {S.nums[S.left]}` 是不超过 threshold 的偶数 → 找到起点")),
        'left += 1': '`left` → {left}',
        'if left == len': lambda S, B, r: ('起点找到头了：没有更多合法子数组，直接返回 `res`' if S.left == len(S.nums) else '还有合法起点，继续'),
        'right = left + 1': '`right` 从 `left + 1` 开始往右扩（起点自己已合法）',
        'while right < len': lambda S, B, r: ('`right` 到头了，停止' if S.right >= len(S.nums) else
                                              (f"`nums[{S.right}] = {S.nums[S.right]}` 不超过 {S.threshold}，且 `{S.nums[S.right-1]} + {S.nums[S.right]} = {S.nums[S.right-1]+S.nums[S.right]}` 是奇数（奇偶不同）→ 能扩" if (S.nums[S.right] <= S.threshold and (S.nums[S.right-1] + S.nums[S.right]) % 2 == 1)
                                               else f"`nums[{S.right}] = {S.nums[S.right]}`：" + ('超过 threshold' if S.nums[S.right] > S.threshold else f'和前一个 {S.nums[S.right-1]} 之和是偶数，奇偶相同') + ' → 停止扩展')),
        'right += 1': '`right` → {right}',
        'res = max': '子数组 `[{left}, {right-1}]`，长度 `right - left = {right - left}`，`res = max({B.res}, {right - left}) = {res}`',
        'left = right': '下一轮从 `right = {right}` 开始找起点，不回头',
        'return res': '最长奇偶子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='先找合法起点，再尽量向右扩，扩不动就换下一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最长子数组：首元素是偶数，相邻奇偶交替，且每个数都 `<= threshold`',
                 '示例：`[3,2,5,4]`，`threshold = 5` → `3`',
                 '本视频：`[2,1,1,4,3,4,2,8]`，`threshold = 5` → `3`'],
        quote='先找出数组中第一个大小不超过 threshold 的偶数，记这个下标为 left，那么 nums[left] 就可以作为一个合法子数组的开头。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，也可以枚举端点；这里一趟扫描更省',
              '`right` 向右扩：不超过 threshold，且相邻两数之和为奇数 ==保证奇偶交替==',
              '结算后令 `left = right` 重新找起点，不回头'],
        summary=['时间 `O(n)`，空间 `O(1)`：`left` 只增不减',
                 '易错：起点要同时是偶数且不超过 threshold',
                 '易错：`left == len(nums)` 时要提前返回，避免越界',
                 '原文已是 Python 3 可运行，未做修改',
                 '对比灵神：灵神用 `i` 一个指针做分组循环；这里是 left、right 两个指针'],
    ),
)
