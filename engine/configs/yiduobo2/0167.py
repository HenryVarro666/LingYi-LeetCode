NUMS = [1, 3, 4, 5, 7, 10, 11]
TARGET = 9


def _formula(S):
    if 'r' not in S:
        return f'从两端往中间扫，找和为 `target = {TARGET}` 的两个数'
    l, r = S['l'], S['r']
    s = NUMS[l] + NUMS[r]
    rel = '>' if s > TARGET else '<' if s < TARGET else '=='
    return f"`now = {NUMS[l]} + {NUMS[r]} = {s}` {rel} `{TARGET}`"


def _cap_elif(S, B, ret):
    if S.now > TARGET:
        return f'`{S.now} > {TARGET}`：和大了 → 右边换个更小的数'
    return f'`{S.now} < {TARGET}`：和小了 → 走 else，左边换个更大的数'


CONFIG = dict(
    num=167, title='两数之和 II - 输入有序数组', difficulty='Medium', category='双指针',
    author='yiduobo', technique='有序 → 双指针从两端往中间扫',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def twoSum(self, numbers, target):
        l = 0
        r = len(numbers) - 1

        while l < r:
            now = numbers[l] + numbers[r]
            if now == target:
                return l + 1, r + 1
            elif now > target:
                r -= 1
            else:
                l += 1
''',
    call=f'Solution().twoSum({NUMS}, {TARGET})',
    expect=(3, 4),
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='numbers', label='numbers（Python 下标从 0 开始）', cell=100, h=230,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'),
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i <= S['r']),
             color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'r' in S else None),
        dict(type='array', var=lambda S: [i + 1 for i in range(len(NUMS))], label='题目要求的下标（从 1 开始）', cell=100, h=150,
             index=False, color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'r' in S else None,
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i <= S['r'])),
        dict(type='text', fn=lambda S: f"返回时要换算：`({S['l']}, {S['r']})` → `({S['l'] + 1}, {S['r'] + 1})`" if 'r' in S else '', size=26, h=60),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', 'now'), ('target', 'target', 'green')],
    captions={
        'l = 0': '`l` 从最左边（最小的数）出发',
        'r = len': '`r = {r}` 从最右边（最大的数）出发',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：两个指针还没相遇，继续扫' if B.l < B.r else '指针相遇，没有答案'),
        'now = numbers': '`now = numbers[{l}] + numbers[{r}] = {numbers[l]} + {numbers[r]} = {now}`',
        'if now == target': lambda S, B, r: (f'`{S.now} == {S.target}` → 找到了' if S.now == S.target else f'`{S.now} ≠ {S.target}`'),
        'return l + 1': '`now == target`，找到了！注意 Python 下标从 0 开始，题目从 1 开始 → 返回 `({l} + 1, {r} + 1)` = =={ret}==',
        'elif now > target': _cap_elif,
        'r -= 1': '`r` 左移到 {r}：`numbers[{r}] = {numbers[r]}` 更小，和会变小',
        'l += 1': '`l` 右移到 {l}：`numbers[{l}] = {numbers[l]}` 更大，和会变大',
    },
    skip=['if now == target'],
    cards=dict(
        one_liner='数组已经有序：和大了 r 左移，和小了 l 右移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`numbers` 已按==非递减顺序==排列，下标==从 1 开始==',
                 '找出两个数，使它们相加之和等于 `target`，返回 `[index1, index2]`',
                 '保证恰好有一个答案，只能用常数额外空间',
                 '本视频：`[1,3,4,5,7,10,11]`，`target = 9` → `[3,4]`'],
        quote='与第一题相同……这里已经排好序了，==依然是双指针从两端往中间扫即可==。需要注意python数组下标从0，但是题目这里面是从1开始的。',
        quote_src='—— yiduobo 知乎题解',
        idea=['第 1 题他先排序再双指针；这题==已经有序==，直接扫',
              '`now == target` 就返回；`now > target` 说明右边太大 → `r -= 1`；否则 `l += 1`',
              '返回时下标 ==+1==，换成题目要求的从 1 开始'],
        result='返回 `(3, 4)`：`numbers[2] + numbers[3] = 4 + 5 = 9` ✓（LeetCode 接受元组）',
        summary=['时间 `O(n)`：每轮 `l` 或 `r` 至少动一步；空间 `O(1)`',
                 '易错：返回 `l + 1, r + 1`，别忘了题目下标从 1 开始',
                 '原文返回元组 `(l+1, r+1)`，LeetCode 也能通过；`while l < r` 保证两个数不重复',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)
