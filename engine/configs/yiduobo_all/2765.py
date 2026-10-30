CONFIG = dict(
    num=2765, title='最长交替子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左边界 · 向右扩展',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1581'],
    code='''
class Solution(object):
    def alternatingSubarray(self, nums):

        left = 0
        res = -1
        while left < len(nums):
            if left + 1 < len(nums) and nums[left + 1] == nums[left] + 1:
                right = left + 2
                while right < len(nums) and nums[right] == nums[right - 2]:
                    right += 1
                
                res = max(res, right - left)
                left = right - 1
            else:
                left += 1
        
        return res
''',
    call='Solution().alternatingSubarray([7,3,4,3,4,5,4,5,4])',
    expect=5,
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right - 1'), h=300,
             label='nums（蓝 = left，粉 = right，框 = 合法段 left..right-1）'),
        dict(type='text', fn=lambda S: f"合法段 `[{S['left']}, {S['right'] - 1}]`，长度 `right − left = {S['right'] - S['left']}`" if 'right' in S and S['right'] > S['left'] + 1 else ''),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'left = 0': '枚举左边界，`left` 从 0 开始',
        'res = -1': '找不到就返回 `-1`',
        'while left < len': '`left = {left}`，还在数组内 → 继续枚举',
        'if left + 1 < len': lambda S, B, r: (f'`nums[{S.left+1}] = {S.nums[S.left+1]}` 是否等于 `nums[{S.left}] + 1 = {S.nums[S.left]+1}` → 成立，以 left 为左边界的子数组存在'
                                           if S.left + 1 < len(S.nums) and S.nums[S.left+1] == S.nums[S.left] + 1
                                           else '后一个数不是 `nums[left] + 1`（或已到末尾）→ 以 left 为左边界的合法子数组不存在'),
        'right = left + 2': '前两个数已满足，`right` 从 `left + 2 = {right}` 向后扩展',
        'while right < len': lambda S, B, r: (f'`nums[{S.right}] = {S.nums[S.right]}`，`nums[{S.right-2}] = {S.nums[S.right-2]}`，相等 → 继续扩展'
                                           if S.right < len(S.nums) and S.nums[S.right] == S.nums[S.right - 2]
                                           else '到边界或 `nums[right] ≠ nums[right-2]` → 停'),
        'res = max': '`left` 到 `right-1` 是合法段，长 `{right} - {left} = {right-left}`；`res = max({B.res}, {right-left}) = {res}`',
        'left = right - 1': '==跳到 right-1，不是 right==：中间的数作左边界，右边界都是 right-1，不必再算；`right-1` 自己还可能和后面组成新段。`left` → {left}',
        'left += 1': '`left` → {left}',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='枚举左边界，向右扩到不能扩，然后直接跳到 right-1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找最长的子数组 `s`：长度 ≥ 2，且按 `s0, s0+1, s0, s0+1, …` 交替',
                 '没有就返回 `-1`',
                 '本视频：`[7,3,4,3,4,5,4,5,4]` → `5`'],
        quote='left跳转到right - 1的理由是以left + 1到right - 2之间的所有数为左边界的合法子序列，其右边界都是right - 1，因此没有必要再进行计算了。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，暴力枚举也行；这里枚举左边界，找最大右边界',
              '`nums[left+1] == nums[left] + 1` 才能起头，否则 `left += 1`',
              '扩展条件 `nums[right] == nums[right-2]`，停下后用 `right − left` 更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：跳到 `right - 1` 而不是 `right`，否则漏掉重叠的下一段',
                 '起头判断里先写 `left + 1 < len(nums)` 防越界',
                 '原文代码是 Python 3 也能运行的写法，未做修改',
                 '对比灵神：灵神把「组头判断 + 记录 i0 + 回退一格」拆成分组循环模板；yiduobo 用 left/right 讲清跳转理由'],
    ),
)
