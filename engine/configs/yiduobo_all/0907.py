def _txt(S):
    if 'stack' not in S or 'arr' not in S:
        return ''
    if S.get('_line') == 16 and 'l' in S and 'r' in S:
        v = S['stack'][-1][0]
        return f"`{v}`：左 `{S['l']}` 种 × 右 `{S['r']}` 种 → 贡献 `{v} × {S['l']} × {S['r']}` = =={v * S['l'] * S['r']}=="
    return '栈里放 `[值, 下标]`：还没找到右边界的数，从底到顶不减'


CONFIG = dict(
    num=907, title='子数组的最小值之和', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 出栈时结算贡献',
    tags=['难度分 1976'],
    code='''
class Solution(object):
    def sumSubarrayMins(self, arr):

        res = 0
        mod = 10 ** 9 + 7
        stack = []
        for index, num in enumerate(arr):
            while stack and stack[-1][0] > num:
                if len(stack) == 1:
                    l = stack[-1][1] + 1
                else:
                    l = stack[-1][1] - stack[-2][1]
                
                r = index - stack[-1][1]

                res = (res + stack[-1][0] * l * r) % mod
                stack.pop()
            
            stack.append([num, index])

        n = len(arr)
        for index in range(len(stack) - 1, -1, -1):
            if index == 0:
                l = stack[index][1] + 1
            else:
                l = stack[index][1] - stack[index - 1][1]
            
            r = n - stack[index][1]

            res = (res + stack[index][0] * l * r) % mod
        
        return res
''',
    call='Solution().sumSubarrayMins([3,1,2,4])',
    expect=17,
    skip=['res = 0', 'mod = ', 'stack = []', 'n = len'],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='arr', label='arr', pointers={'index': 'blue'}, cell=90, h=210),
        dict(type='stack', var=lambda S: [f'{a} @{b}' for a, b in S['stack']] if 'stack' in S else None,
             label='stack（值 @下标；栈顶最大）', h=280),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'while stack and stack[-1][0] > num': lambda S, B, r: (
            f'栈顶 `{B.stack[-1][0]}` > 当前 `{B.num}` → ==右边界就是 `index = {B.index}`==，可以结算栈顶'
            if B.stack and B.stack[-1][0] > B.num else '栈空或栈顶 ≤ 当前数：不用弹，当前数入栈'),
        'l = stack[-1][1] + 1': '栈里只有它一个：左边没有更小的，左端点有 `{l}` 种',
        'l = stack[-1][1] - stack[-2][1]': '栈中下面那个是它的左边界：左端点有 `{l}` 种',
        'r = index - stack[-1][1]': '右端点有 `{r}` 种（到 `index - 1` 为止）',
        'res = (res + stack[-1][0]': '`{stack[-1][0]} × {l} × {r}` 累加进 `res` = =={res}==',
        'stack.pop()': '结算完毕，弹出栈顶',
        'stack.append': '`[{num}, {index}]` 入栈，等它的右边界出现',
        'for index in range(len(stack) - 1': '扫描完了，栈里剩下的数右边界都是数组末尾 `n = {n}`，从栈顶往下逐个结算',
        'if index == 0': lambda S, B, r: ('栈底元素：左边没有更小的' if S.index == 0 else '不是栈底：左边界是下面那个元素'),
        'l = stack[index][1] + 1': '左端点有 `{l}` 种',
        'l = stack[index][1] - stack[index - 1][1]': '左端点有 `{l}` 种',
        'r = n - stack[index][1]': '右端点有 `{r}` 种（一直到末尾）',
        'res = (res + stack[index][0]': '`{stack[index][0]} × {l} × {r}` 累加进 `res` = =={res}==',
        'return res': '最终答案 ==`{res}`==',
    },
    cards=dict(
        one_liner='每个数能当多少个子数组的最小值，就贡献多少次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求 `arr` 所有连续子数组的最小值之和，对 `10^9 + 7` 取模',
                 '示例：`[3,1,2,4]` → `17`',
                 '3 贡献 3，1 贡献 6，2 贡献 4，4 贡献 4'],
        quote='将计算各个子数组的最小值之和，转变为对于数组中的每个数来说，这个数是多少个子数组的最小值？',
        quote_src='—— yiduobo 题解原文',
        idea=['左边第一个 ≥ 它的位置为 `l`、右边第一个 > 它的位置为 `r`（相同数取下标较小者）',
              '个数 = 左边选择数 × 右边选择数',
              '用栈保存还不知道右边界的数；遇到更小的数就结算栈顶'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '相同数字只算一次：弹出条件用严格大于 `>`',
                 '扫描结束后栈里还有元素，右边界是数组末尾，要再结算一遍',
                 '对比灵神：灵神用哨兵与末尾 -1 一次遍历搞定；yiduobo 这里栈存 `[值, 下标]` 并在最后补算'],
    ),
)
