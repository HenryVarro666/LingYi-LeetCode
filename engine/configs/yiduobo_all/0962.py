A_ = [6, 0, 8, 2, 1, 5]


def _draw_info(S):
    st = S.get('stack')
    if st is None:
        return ''
    return f'候选左端（单调递减）：`{[A_[i] for i in st]}`，位置 `{st}`；当前最宽 ==`{S.get("res", 0)}`=='


CONFIG = dict(
    num=962, title='最大宽度坡', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈：先选左端候选，再从右往左配对',
    tags=['单调栈'],
    code='''
class Solution(object):
    def maxWidthRamp(self, A):

        stack = [0]
        for index in range(1, len(A)):
            if A[index] < A[stack[-1]]:
                stack.append(index)

        res = 0
        for index in range(len(A) - 1, -1, -1):
            while stack and A[stack[-1]] <= A[index]:
                res = max(res, index - stack[-1])
                stack.pop()
            
        return res
''',
    call='Solution().maxWidthRamp([6,0,8,2,1,5])',
    expect=4,
    views=[
        dict(type='text', fn=_draw_info),
        dict(type='array', var='A', label='A（蓝 = 当前 index，黄 = 栈顶候选）',
             pointers={'index': 'blue'}, h=230,
             color=lambda S, i, v: ('yellow' if S.get('stack') and i == S['stack'][-1] else None)),
        dict(type='stack', var='stack', label='栈：候选左端的下标（值递减）', fmt=lambda i: f'{i}:{A_[i]}', h=250),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'yellow'), ('res', 'res', 'green')],
    captions={
        'stack = [0]': '下标 0 一定是左端候选：它最靠左',
        'for index in range(1, len(A))': '第一趟从左往右，挑出所有可能的==较小一侧==',
        'if A[index] < A[stack[-1]]': lambda S, B, ret: (
            f'`A[{S.index}] = {S.A[S.index]}` < 栈顶值 `{S.A[S.stack[-1]]}` → 比前面所有候选都小，可能当左端' if S.A[S.index] < S.A[S.stack[-1]]
            else f'`A[{S.index}] = {S.A[S.index]}` ≥ 栈顶值 `{S.A[S.stack[-1]]}` → 它更靠右还更大，必输给栈顶，放弃'),
        'stack.append(index)': '下标 `{index}` 入栈：栈里的值严格递减',
        'res = 0': '第一趟结束，候选左端 `{stack}`。第二趟从右往左找较大一侧',
        'for index in range(len(A) - 1, -1, -1)': '从右往左枚举右端 `index`：越早遇到越宽',
        'while stack and A[stack[-1]] <= A[index]': lambda S, B, ret: (
            f'栈顶值 `{S.A[S.stack[-1]]}` ≤ `A[{S.index}] = {S.A[S.index]}` → 这是它能配到的最远右端' if S.stack and S.A[S.stack[-1]] <= S.A[S.index]
            else ('栈已空，没有候选了' if not S.stack else f'栈顶值 `{S.A[S.stack[-1]]}` > `A[{S.index}] = {S.A[S.index]}` → 配不上，继续往左找右端')),
        'res = max': '宽度 `{index} − {B.stack[-1]}` = {index - B.stack[-1]}，`res = max(…) = {res}`',
        'stack.pop()': '这个左端已经配到最远右端，==弹出==，不会再有更宽的',
        'return res': '最宽的坡 `{res}`',
    },
    cards=dict(
        one_liner='左端候选只留递减序列，再从右往左一一配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['坡：`i < j` 且 `A[i] <= A[j]`，宽度为 `j - i`',
                 '求数组中最大宽度的坡，没有则为 0',
                 '本视频：`[6,0,8,2,1,5]` → `4`（`A[1]=0` 与 `A[5]=5`）'],
        quote='对于一组A[x]和A[y]，若存在x < y且A[x] <= A[y]，那么A[y]必然不会成为答案中较小的那个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['若左边已有不大的 `A[x]`，用 `A[y]` 当左端一定不如用 `A[x]`',
              '所以候选左端只剩一个单调递减的栈',
              '从右往左枚举右端，大于等于栈顶就配对更新答案并弹出'],
        summary=['时间 `O(n)`，两趟扫描',
                 '第一趟用 `<`：相等的不入栈，因为更靠左的相等值更好',
                 '第二趟从右往左，==先配最远的右端==，栈顶弹出后不会再用',
                 '原文为 Python 2 风格，代码无需改动即可运行；原文无题面，题意按 LeetCode 962 整理'],
    ),
)
