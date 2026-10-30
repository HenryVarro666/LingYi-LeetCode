def _txt(S):
    ln = S.get('_line', 0)
    if ln >= 26:
        if ln in (27, 28) and 'index' in S:
            i = S['index']
            return (f"`min_k[{i}] = {S['min_k'][i]}`：它当最小值时，最长子数组 `[{S['left'][i]+1}, {S['right'][i]-1}]` 长度 "
                    f"`{S['right'][i]}-({S['left'][i]})-1 = {S['right'][i]-S['left'][i]-1}`，要 `>= {S['min_k'][i]}`")
        return '最后一步：逐个检查，最长长度够不够它自己要求的最短长度'
    if ln >= 16:
        return '第三步：从右往左的单调栈，求右边界'
    if ln >= 7:
        return '第二步：从左往右的单调栈，求左边界'
    return '第一步：算 min_k，再用单调栈求每个位置的左右边界'


def _wcap(S, B, ret):
    mk, st, i = S['min_k'], S['stack'], S['index']
    cur = mk[i]
    if st and mk[st[-1]] <= cur:
        return f"栈顶 `min_k[{st[-1]}] = {mk[st[-1]]}` `<= {cur}`：==成立==，它不是「更大」的那个，弹出"
    if not st:
        return '栈空了：这一侧没有更大的元素，边界保持原值'
    return f"栈顶 `min_k[{st[-1]}] = {mk[st[-1]]}` `> {cur}`：停止弹栈，它就是这一侧第一个更大的"


def _if_cap(S, B, ret):
    st, i = S['stack'], S['index']
    if S['_line'] == 13:
        return f"栈顶 `{st[-1]}` 是左边界：`left[{i}] = {st[-1]}`" if st else f"栈空，`left[{i}]` 保持 -1"
    return f"栈顶 `{st[-1]}` 是右边界：`right[{i}] = {st[-1]}`" if st else f"栈空，`right[{i}]` 保持 n = {len(S['nums'])}"


def _for_desc(S, B, ret):
    n = len(S['nums'])
    i = S['index']
    if i == B.get('index') and i == 0:
        return '从右往左扫完了，`right` 全部求好'
    return f"从右往左：`index = {i}`"


def _for_asc(S, B, ret):
    n = len(S['nums'])
    i = S['index']
    if S['_line'] < 20:
        return '从左往右扫完了，`left` 全部求好' if i == B.get('index') else f"从左往右：`index = {i}`"
    if i == B.get('index') and i == n - 1:
        return '`left`、`right` 都求好了，逐个检查结束'
    return f"检查 `index = {i}`"


CONFIG = dict(
    num=2334, title='元素值大于变化阈值的子数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='换成 min_k + 单调栈求左右边界',
    tags=['单调栈', '难度分 2381'],
    code='''
class Solution(object):
    def validSubarraySize(self, nums, threshold):

        min_k = [threshold // num + 1 for num in nums]
        n = len(nums)

        left = [-1] * n
        stack = []
        for index in range(n):
            while stack and min_k[stack[-1]] <= min_k[index]:
                stack.pop()
            
            if stack:
                left[index] = stack[-1]
            
            stack.append(index)
        
        right = [n] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and min_k[stack[-1]] <= min_k[index]:
                stack.pop()
            
            if stack:
                right[index] = stack[-1]
            
            stack.append(index)
        
        for index in range(n):
            if right[index] - left[index] - 1 >= min_k[index]:
                return min_k[index]
        
        return -1
''',
    call='Solution().validSubarraySize([1,3,4,3,1], 6)',
    expect=3,
    skip=['left[index] = stack[-1]', 'right[index] = stack[-1]', 'n = len(nums)', 'stack = []'],
    views=[
        dict(type='text', h=60, size=26, fn=_txt),
        dict(type='array', var='nums', label='nums', h=130),
        dict(type='array', var='min_k', label='min_k（至少要多长）', h=170, pointers={'index': 'blue'},
             window=(lambda S: S['left'][S['index']] + 1 if S.get('_line', 0) in (27, 28) and 'index' in S else None,
                     lambda S: S['right'][S['index']] - 1 if S.get('_line', 0) in (27, 28) and 'index' in S else None)),
        dict(type='stack', var='stack', h=100, fmt=lambda i: str(i)),
        dict(type='array', var='left', label='left', h=90),
        dict(type='array', var='right', label='right', h=90),
    ],
    watch=['index', ('threshold', 'threshold', 'cyan')],
    captions={
        'min_k = [': '`min_k[i] = threshold // nums[i] + 1`：含 `nums[i]` 的合法子数组==至少要这么长==',
        'while stack and min_k': _wcap,
        'for index in range(n - 1': _for_desc,
        'for index in range(n):': _for_asc,
        'left = [-1]': '`left[i]` 先全设 -1：左边没有更大的 `min_k`',
        'right = [n]': '`right[i]` 先全设 n：右边没有更大的 `min_k`',
        'if stack:': _if_cap,
        'stack.append(index)': '下标 `{index}` 入栈',
        'if right[index] - left[index] - 1 >=': lambda S, B, ret: (
            f"最长子数组长度 `{S['right'][S['index']]} - ({S['left'][S['index']]}) - 1 = {S['right'][S['index']] - S['left'][S['index']] - 1}`，"
            + (f"`>= min_k = {S['min_k'][S['index']]}` ==成立==" if S['right'][S['index']] - S['left'][S['index']] - 1 >= S['min_k'][S['index']] else f"`< min_k = {S['min_k'][S['index']]}` 不成立，看下一个")),
        'return min_k[index]': '长度够了：这个长度 `{min_k[index]}` 就是答案',
        'return -1': '都不满足，返回 `-1`',
    },
    cards=dict(
        one_liner='把阈值换成「至少多长」，再看最长长度够不够',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找长度为 `k` 的子数组，每个元素都 `> threshold / k`，返回任意合法 `k`，没有返回 `-1`',
                 '示例：`nums=[1,3,4,3,1], threshold=6` → `3`'],
        quote='可以先计算出 min_k[i] = threshold / nums[i] + 1，其含义是包含第 i 个数的合法子数组的最短长度，那么问题就变成了能否在 min_k 中找出一个子数组，其中的最小值大于等于这个子数组的长度。',
        quote_src='—— yiduobo 题解',
        idea=['`nums[i]` 要在长度 `k` 的数组里合法，等价于 `k >= min_k[i]`',
              '子数组合法 ⇔ `min_k` 的最小值 `>=` 子数组长度',
              '枚举 `min_k[index]` 当最小值，两个单调栈求左右边界，长度 `right-left-1 >= min_k[index]` 就找到了'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`threshold / num` 的整数除法已改为 `//`',
                 '这里是 `min_k` 的「最大」范围：弹栈用 `<=`，边界是第一个严格更大的',
                 '返回的是 `min_k[index]`（满足条件的一个 `k`），不是 `index`'],
    ),
)
