NUMS = [5, 3, 4, 2, 6, 1, 7]


def _st(S):
    return S.get('stack')


def _hl(S, i, v):
    st = S.get('stack') or []
    return 'green' if i in st else None


def _info(S):
    st = S.get('stack')
    if st is None:
        return ''
    if S.get('_line', 0) and 'res' in S:
        return f"备选左边界下标 `{st}`，当前答案 `res = {S['res']}`"
    return f"备选左边界下标 `{st}`"


CONFIG = dict(
    num=2863, title='最长半递减数组', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 备选左边界 + 从右往左匹配',
    tags=['灵神题单·单调栈'],
    code='''
class Solution(object):
    def maxSubarrayLength(self, nums):

        stack = []
        n = len(nums)
        for index in range(n):
            if not stack or nums[stack[-1]] < nums[index]:
                stack.append(index)

        res = 0
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[index]:
                res = max(res, index - stack.pop() + 1)
            
            if not stack:
                break
        
        return res
''',
    call=f'Solution().maxSubarrayLength({NUMS})',
    expect=6,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=200, label='nums（绿色 = 栈里的备选左边界）',
             color=lambda S, i, v: ('blue' if S.get('index') == i else ('green' if i in (S.get('stack') or []) else None))),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}:{NUMS[i]}', label='stack（备选左边界：下标:数值，栈顶在右）', h=170),
        dict(type='text', fn=_info, size=28, h=90),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'green'), ('res', 'res', 'yellow')],
    captions={
        'stack = []': '`stack` 存==备选左边界==的下标',
        'for index in range(n):': '第一趟从左往右，挑出所有可能当左边界的位置',
        'if not stack or nums[stack[-1]] < nums[index]': lambda S, B, r: (
            f"栈空 → `{S.index}` 直接入栈" if not S.stack else
            f"`nums[{S.index}] = {S.nums[S.index]}` > 栈顶值 `{S.nums[S.stack[-1]]}` → 有资格当备选左边界"
            if S.nums[S.stack[-1]] < S.nums[S.index] else
            f"`nums[{S.index}] = {S.nums[S.index]}` ≤ 栈顶值 `{S.nums[S.stack[-1]]}` → ==前面有个不更小的数，它当左边界更长==，跳过"),
        'stack.append(index)': '`{index}` 成为备选左边界，栈里的值保持==严格递增==：`{[nums[i] for i in stack]}`',
        'res = 0': '`res` 初始为 0：万一匹配出负长度，也不会更新答案',
        'for index in range(n - 1, -1, -1)': '第二趟从右往左枚举右边界 `index = {index}`（值 `{nums[index]}`）',
        'while stack and nums[stack[-1]] > nums[index]': lambda S, B, r: (
            f"栈空，没有左边界可匹配了" if not S.stack else
            f"栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` > 右边界 `{S.nums[S.index]}` → ==能组成半递减==，弹出匹配"
            if S.nums[S.stack[-1]] > S.nums[S.index] else
            f"栈顶 `{S.nums[S.stack[-1]]}` ≤ 右边界 `{S.nums[S.index]}`，其余左边界更小，更不行 → 右边界左移"),
        'res = max(res, index - stack.pop() + 1)': lambda S, B, r: f"弹出左边界 `{B.stack[-1]}`，长度 `{S.index} - {B.stack[-1]} + 1` = =={S.index - B.stack[-1] + 1}==" + ('（≤ 0：右边界在左边界左侧，不合法，不会更新答案）' if S.index - B.stack[-1] + 1 <= 0 else '') + f"，`res` → {S.res}。==右边界不动==，它还能匹配更靠左的左边界",
        'if not stack': lambda S, B, r: ('栈空：所有备选左边界都匹配完了 → ==break==' if not S.stack else '栈里还有左边界，继续往左找右边界'),
        'return res': '最长半递减子数组长度 =={ret}==',
    },
    cards=dict(
        one_liner='备选左边界是递增栈；右边界从右往左，能匹配就弹出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['半递减数组：==第一个元素 > 最后一个元素==的子数组',
                 '求 `nums` 中最长的半递减子数组长度，没有则返回 `0`',
                 '本视频：`[5,3,4,2,6,1,7]` → `6`（`[5,3,4,2,6,1]`，5 > 1）'],
        quote='若存在两个下标i、j满足i < j且nums[i] >= nums[j]，那么j就不可能成为答案数组的左边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['左边有个不更小的 `nums[i]` 时，用它当左边界总比 `j` 更长 → 备选左边界必然递增，一趟用栈挑出来',
              '再从后往前：栈顶 ≤ 右边界值，其他更小，全匹配不了 → 右边界左移',
              '栈顶更大就匹配并弹出，右边界不动，继续尝试下一个更靠左的备选'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`res` 初值 0：匹配到的右边界若在左边界左侧，长度 ≤ 0，不会更新答案',
                 '匹配成功后==右边界不动==，因为一个右边界可能匹配多个左边界',
                 '原文本身已是 Python 3 可运行的写法，未做修改'],
    ),
)
