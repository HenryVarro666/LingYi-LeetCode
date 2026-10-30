CONFIG = dict(
    num=2903, title='找出满足差值条件的下标 I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='暴力枚举下标对', tags=[],
    code='''
class Solution(object):
    def findIndices(self, nums, indexDifference, valueDifference):

        for i in range(len(nums)):
            for j in range(i, len(nums)):
                if abs(i - j) >= indexDifference and abs(nums[i] - nums[j]) >= valueDifference:
                    return [i, j]
        
        return [-1, -1]
''',
    call='Solution().findIndices([3,5,2,6,1,9], 2, 5)',
    expect=[0, 5],
    views=[
        dict(type='array', var='nums', h=260, label='nums', pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: 'blue' if i == S.get('i') else 'pink' if i == S.get('j') else None),
        dict(type='text', size=32, fn=lambda S: f"下标差 `{abs(S['i']-S['j'])}`（需 ≥ {S['indexDifference']}），值差 `{abs(S['nums'][S['i']]-S['nums'][S['j']])}`（需 ≥ {S['valueDifference']}）" if 'j' in S and 'i' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'for i in range': '固定左边的 `i = {i}`',
        'for j in range': '`j` 从 `i` 开始往右试：`j = {j}`（可以等于 i）',
        'if abs(i - j)': '下标差 `|{i}-{j}| = {abs(i-j)}` {"≥" if abs(i-j) >= indexDifference else "<"} `{indexDifference}`；值差 `|{nums[i]}-{nums[j]}| = {abs(nums[i]-nums[j])}` {"≥" if abs(nums[i]-nums[j]) >= valueDifference else "<"} `{valueDifference}` → {"两个条件都成立" if abs(i-j) >= indexDifference and abs(nums[i]-nums[j]) >= valueDifference else "不满足，继续试"}',
        'return [i, j]': '找到一对 → 返回 `[{i}, {j}]`',
        'return [-1, -1]': '所有下标对都试过了，没有满足的 → `[-1, -1]`',
    },
    cards=dict(
        one_liner='数据规模很小，直接枚举所有下标对检查两个条件',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['找下标 `i, j`，要求 `|i-j| ≥ indexDifference` 且 `|nums[i]-nums[j]| ≥ valueDifference`',
                 '找不到返回 `[-1, -1]`，`i` 和 `j` 可以相等',
                 '本视频：`[3,5,2,6,1,9]`，下标差 2，值差 5'],
        quote='题目的数据规模很小，因此可以直接枚举下标i和j，然后检测下标差和数值差是否符合条件即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 100`，`n^2` 完全能过',
              '外层枚举 `i`，内层 `j` 从 `i` 开始，同时检查两个条件',
              '第一个满足的下标对就返回，题目允许任意一组'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`j` 从 `i` 开始，因为 `i == j` 合法（两个差值要求都为 0 时）',
                 '两个条件要同时成立，用 `and` 连接',
                 '对比灵神：他枚举 j 并维护左侧最值，降到 `O(n)`'],
    ),
)
