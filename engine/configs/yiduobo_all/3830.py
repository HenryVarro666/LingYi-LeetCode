CONFIG = dict(
    num=3830, title='移除至多一个元素后的最长交替子数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='波峰波谷 · 正反两趟 DP',
    tags=['动态规划', '难度分 2162'],
    code='''
class Solution(object):
    def longestAlternating(self, nums):
        
        n = len(nums)
        to_left_high = [1] * n
        to_left_low = [1] * n
        for index in range(1, n):
            if nums[index] == nums[index - 1]:
                continue
            if nums[index] < nums[index - 1]:
                to_left_low[index] = to_left_high[index - 1] + 1
            else:
                to_left_high[index] = to_left_low[index - 1] + 1
        
        to_right_high = [1] * n
        to_right_low = [1] * n
        for index in range(n - 2, -1, -1):
            if nums[index] == nums[index + 1]:
                continue
            if nums[index] < nums[index + 1]:
                to_right_low[index] = to_right_high[index + 1] + 1
            else:
                to_right_high[index] = to_right_low[index + 1] + 1
        
        res = max(max(to_left_high), max(to_left_low))
        for index in range(1, n - 1):
            if nums[index - 1] > nums[index + 1]:
                res = max(res, to_left_high[index - 1] + to_right_low[index + 1])
            if nums[index - 1] < nums[index + 1]:
                res = max(res, to_left_low[index - 1] + to_right_high[index + 1])
        return res
''',
    call='Solution().longestAlternating([1,3,2,2,4,1])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=175, pointers={'index': 'blue'},
             color=lambda S, k, v: 'orange' if 'res' in S and S.get('index') is not None and k in (S['index'] - 1, S['index'] + 1) else None),
        dict(type='array', var='to_left_high', label='左·峰', h=100, index=False),
        dict(type='array', var='to_left_low', label='左·谷', h=100, index=False),
        dict(type='array', var='to_right_high', label='右·峰', h=100, index=False),
        dict(type='array', var='to_right_low', label='右·谷', h=100, index=False),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    max_steps=80,
    skip=['n = len(nums)', 'continue', '* n', 'for index in range(n - 2', 'if nums[index] < nums[index - 1]', 'if nums[index] < nums[index + 1]'],
    captions={
        'if nums[index] == nums[index - 1]': lambda S, B, ret: (f"`nums[{S['index']}] == nums[{S['index']-1}]`，相等不能交替：峰、谷都只能是自己（保持 1）" if S['nums'][S['index']] == S['nums'][S['index']-1] else f"`nums[{S['index']}] = {S['nums'][S['index']]}` 与前一个 `{S['nums'][S['index']-1]}` 不等，可以接在后面"),
        'to_left_low[index] = to_left_high[index - 1] + 1': '比前一个小：`nums[{index}]` 当波谷，接在「以 {index-1} 为波峰」的段后面 → `to_left_low[{index}] = {to_left_low[index]}`',
        'to_left_high[index] = to_left_low[index - 1] + 1': '比前一个大：`nums[{index}]` 当波峰，接在「以 {index-1} 为波谷」的段后面 → `to_left_high[{index}] = {to_left_high[index]}`',
        'if nums[index] == nums[index + 1]': lambda S, B, ret: ('反过来从右往左再算一遍：`to_right_*[i]` 表示以 `nums[i]` 作为第一个波谷 / 波峰的最长长度。' if S['index'] == len(S['nums']) - 2 else '') + (f"`nums[{S['index']}]` 与右边相等，保持 1" if S['nums'][S['index']] == S['nums'][S['index']+1] else f"`nums[{S['index']}]={S['nums'][S['index']]}` 与右边 `{S['nums'][S['index']+1]}` 不等，" + ('更小，当波谷' if S['nums'][S['index']] < S['nums'][S['index']+1] else '更大，当波峰')),
        'to_right_low[index] = to_right_high[index + 1] + 1': '`nums[{index}]` 比右边小，当第一个波谷，后面接以 `{index+1}` 为第一个波峰的段 → `to_right_low[{index}] = {to_right_low[index]}`',
        'to_right_high[index] = to_right_low[index + 1] + 1': '`nums[{index}]` 比右边大，当第一个波峰，后面接以 `{index+1}` 为第一个波谷的段 → `to_right_high[{index}] = {to_right_high[index]}`',
        'res = max(max(to_left_high)': '不删元素：to_left_high 与 to_left_low 里的最大值 = =={res}==',
        'if nums[index - 1] > nums[index + 1]': lambda S, B, ret: f"删掉 `nums[{S['index']}]`：`nums[{S['index']-1}]={S['nums'][S['index']-1]}` 与 `nums[{S['index']+1}]={S['nums'][S['index']+1]}`，" + ('左大右小：左边当波峰、右边当波谷，能拼' if S['nums'][S['index']-1] > S['nums'][S['index']+1] else '不满足左大右小'),
        'to_left_high[index - 1] + to_right_low[index + 1]': '左边以峰结尾 `{to_left_high[index-1]}` + 右边以谷开头 `{to_right_low[index+1]}`，`res` → =={res}==',
        'if nums[index - 1] < nums[index + 1]': lambda S, B, ret: ('左小右大：左边当波谷、右边当波峰，能拼' if S['nums'][S['index']-1] < S['nums'][S['index']+1] else '不满足左小右大'),
        'to_left_low[index - 1] + to_right_high[index + 1]': '左边以谷结尾 `{to_left_low[index-1]}` + 右边以峰开头 `{to_right_high[index+1]}`，`res` → =={res}==',
    },
    cards=dict(
        one_liner='波峰波谷各算一遍，删中间那个，左右两段拼起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['交替子数组：相邻元素 ==大、小交替==（波峰-波谷-波峰…），长度 1 也算',
                 '最多删掉 `nums` 里的一个元素，求能得到的最长交替子数组长度',
                 '示例：`[1,3,2,2,4,1]` → 删掉一个 `2`，得到 `[1,3,2,4,1]`，答案 `5`'],
        quote='在移除nums[index]后，要么是nums[index - 1]当波峰，nums[index + 1]当波谷，要么反过来nums[index - 1]当波谷，nums[index + 1]当波峰。',
        quote_src='—— yiduobo 题解',
        idea=['`low[i]` / `high[i]`：以 `nums[i]` 作为最后一个波谷 / 波峰的最长长度，从左到右一趟、从右到左一趟',
              '删掉 `nums[index]`，若 `nums[index-1] > nums[index+1]`：左边当波峰、右边当波谷，长度相加',
              '反之左边当波谷、右边当波峰；删首尾元素没有意义'],
        summary=['时间 `O(n)`，空间 `O(n)`（四个数组）',
                 '相等元素不能相邻，所以 `nums[index-1] == nums[index+1]` 时两个 if 都不进',
                 '易错点：`to_right_*` 的含义是「作为第一个」波谷 / 波峰，不是最后一个',
                 '原文就是 Python 3 可运行的写法，代码未改动'],
    ),
)
