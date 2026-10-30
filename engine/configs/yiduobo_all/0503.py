NUMS = [3, 1, 2]


def _val(S, i):
    return S['nums'][i % len(S['nums'])]


def _while(S, B, ret):
    st, i = B.stack, B.index
    x = _val(B, i)
    if st and x >= _val(B, st[-1]):
        return (f'`nums[{i % B.l}] = {x} ≥ 栈顶值 {_val(B, st[-1])}`：栈顶更靠后又不比它大'
                f' → ==不可能再成为答案==，弹出')
    if st:
        return f'`{x} < 栈顶值 {_val(B, st[-1])}`：停止弹栈'
    return '栈已经空了，停止弹栈'


def _for(S, B, ret):
    if 'index' in B and B.index == S.index:
        return '扫描结束'
    i, l = S.index, S.l
    if i >= l:
        return f'扫描复制部分：`index = {i}`，对应 `nums[{i} % {l}] = nums[{i % l}] = {_val(S, i)}`'
    return f'扫描原数组：`index = {i}`，`nums[{i}] = {_val(S, i)}`'


def _show(S):
    if 'index' not in S:
        return '把 nums 原样复制一遍接在后面，再从后往前求下一个更大元素'
    i, l = S['index'], S['l']
    if S.get('_line') in (20, 21):
        return '`res` 是倒序收集的，翻转后就是答案'
    if i >= l:
        return f'复制部分（`index ≥ {l}`）：==只把数压进栈==，给原数组当「右边的数」'
    return f'原数组部分（`index < {l}`）：弹完栈后，==栈顶就是答案=='


CONFIG = dict(
    num=503, title='下一个更大元素 II', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 取模模拟复制数组',
    tags=['labuladong', '灵神题单·单调栈'],
    code='''
class Solution(object):
    def nextGreaterElements(self, nums):

        if not nums:
            return []

        stack = [nums[-1]]
        res = []
        l = len(nums)
        for index in range(l + l - 1, -1, -1):
            while stack and nums[index % l] >= nums[stack[-1] % l]:
                stack.pop()
            if index < len(nums):
                if stack:
                    res.append(nums[stack[-1] % l])
                else:
                    res.append(-1)
            stack.append(index)

        res.reverse()
        return res
''',
    call=f'Solution().nextGreaterElements({NUMS})',
    expect=[-1, 2, 3],
    views=[
        dict(type='array', var=lambda S: S['nums'] * 2 if 'nums' in S else None,
             label='复制一遍后的数组（紫 = 栈里的下标，暗 = 已扫描且被弹出）', cell=96,
             pointers={'index': 'blue'},
             dim=lambda S, i, v: 'index' in S and i > S['index'] and i not in (S.get('stack') or []),
             color=lambda S, i, v: 'blue' if i == S.get('index') else ('purple' if i in (S.get('stack') or []) else None)),
        dict(type='stack', var='stack', label='stack（存下标  下标:值）', fmt=lambda i: f'{i}:{NUMS[i % 3]}', h=120, font=30),
        dict(type='array', var='res', label='res（从后往前收集的答案）', cell=96, min_slots=3),
        dict(type='text', fn=_show, size=27, h=64),
    ],
    watch=[('index', 'index', 'blue'), ('index % l', 'index % l'), ('stack', 'stack', 'purple'), ('res', 'res', 'green')],
    captions={
        'if not nums': '特判：`nums` 不为空，继续',
        'stack = [nums[-1]]': '栈里先放入 `nums[-1] = {nums[-1]}`（栈中的数都按 `% l` 当下标用）',
        'res = []': '`res` 按扫描顺序收集答案（==倒序==）',
        'l = len': '`l = {l}`：把 nums 复制一遍接在后面，相当于长度 `{2 * l}` 的数组',
        'for index in range': _for,
        'while stack and': _while,
        'stack.pop()': '弹出栈顶下标 `{B.stack[-1]}`',
        'if index < len(nums)': lambda S, B, ret: (f'`index = {S.index} < {S.l}`：是原数组的元素 → ==记录答案=='
                                                   if S.index < S.l else
                                                   f'`index = {S.index} ≥ {S.l}`：复制部分==不记录答案==，只压栈'),
        'if stack:': lambda S, B, ret: (f'栈不空 → 下一个更大元素是栈顶的值 `{_val(S, S.stack[-1])}`' if S.stack
                                        else '栈为空 → 绕一圈也没有更大的数，答案 `-1`'),
        'res.append(nums[': '`res` 追加 `{res[-1]}`（`nums[{index}] = {nums[index]}` 的答案）',
        'res.append(-1)': '`res` 追加 `-1`（`nums[{index}] = {nums[index]}` 的答案）',
        'stack.append(index)': '当前下标 `{index}` 压栈：它可能是左边元素的答案',
        'res.reverse()': '答案是从后往前收集的 → ==翻转==，得到 `{res}`',
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='循环数组复制一遍接在后面，再套用 496 的单调栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是==循环数组==：`nums[n−1]` 的下一个元素是 `nums[0]`',
                 '求每个元素的下一个更大元素（可以绕回开头找），不存在则 `-1`',
                 '示例：`[1,2,1]` → `[2,-1,2]`',
                 '本视频：`[3,1,2]` → `[-1,2,3]`'],
        quote='对于循环数组，一种普遍的做法是==将数组原样复制一遍，然后接在原始数组的后面==。复制好之后，就可以对新得到的这个数组使用之前求下一个更大元素的做法了。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有真的复制，而是用 `index % l` 模拟复制后的数组',
              '从后往前扫 `2l` 个位置，栈里存可能成为答案的下标',
              '只有 `index < l` 才记录答案；最后把倒序的 `res` 翻转'],
        summary=['时间 `O(n)`：`2n` 个下标各入栈、出栈最多一次；空间 `O(n)`',
                 '弹栈用 `>=`：相等的数不是「更大」元素',
                 '初始 `stack = [nums[-1]]` 存的是值，会被当成下标 `% l` 使用；它在复制部分一定会被弹出，不影响答案',
                 '原文代码可直接在 Python 3 运行，未做修改'],
    ),
)
