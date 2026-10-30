NUMS = [3, 5, 2, 6, 1, 7]
K = 3


def _cond(S):
    line = S.get('_line')
    if 'index' not in S or line not in (6, 7, 8):
        if line in (10, 11):
            return f'扫描结束：栈里有 `{len(S["stack"])}` 个，只留栈底 `k = {K}` 个'
        return '弹栈条件：栈非空、栈顶 `> nums[index]`、弹完后 `len(stack) − 1 + n − index ≥ k`'
    st, idx = S['stack'], S['index']
    n = len(S['nums'])
    if not st:
        return f'`nums[{idx}] = {S["nums"][idx]}`：栈空'
    top = S['nums'][st[-1]]
    left = len(st) - 1 + n - idx
    return (f'栈顶 `{top}` {">" if top > S["nums"][idx] else "≤"} `nums[{idx}] = {S["nums"][idx]}`；'
            f'弹完剩 `{len(st) - 1} + {n - idx} = {left}` {"≥" if left >= K else "<"} `k = {K}`')


def _cap_while(S, B, ret):
    st, idx, nums = B.stack, B.index, B.nums
    n = len(nums)
    if not st:
        return '栈空 → 直接压入'
    top = nums[st[-1]]
    if top <= nums[idx]:
        return f'栈顶 `{top} ≤ {nums[idx]}`：保持递增 → 不弹'
    left = len(st) - 1 + n - idx
    if left < K:
        return f'栈顶 `{top} > {nums[idx]}`，但弹完只剩 `{left} < k` 个数可用 → ==剩余数字不足，不能弹=='
    return f'栈顶 `{top} > {nums[idx]}`，弹完还有 `{left} ≥ k` 个数可用 → 弹出，让小的数往前'


CONFIG = dict(
    num=1673, title='找出最具竞争力的子序列', difficulty='Medium', category='栈',
    author='yiduobo', technique='单调栈存下标 · 最后截取前 k 个',
    tags=['字节30天'],
    code='''
class Solution(object):
    def mostCompetitive(self, nums, k):
        stack = []
        n = len(nums)
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index] and len(stack) - 1 + n - index >= k:
                stack.pop()
            stack.append(index)

        while len(stack) > k:
            stack.pop()

        return [nums[index] for index in stack]
''',
    call=f'Solution().mostCompetitive({NUMS}, {K})',
    expect=[2, 1, 7],
    views=[
        dict(type='text', fn=_cond, h=60, size=25),
        dict(type='array', var='nums', label='nums（紫 = 栈里的下标）', cell=96, pointers={'index': 'blue'},
             color=lambda S, j, v: 'blue' if j == S.get('index') and S.get('_line') in (5, 6, 7, 8)
             else ('purple' if j in (S.get('stack') or []) else None)),
        dict(type='stack', var='stack', label=f'stack（存下标 i:值；k = {K}）', h=150, font=32,
             fmt=lambda i: f'{i}:{NUMS[i]}'),
    ],
    watch=[('index', 'index', 'blue'), ('len(stack)', 'len(stack)'), ('n', 'n')],
    captions={
        'stack = []': '单调栈里存==下标==，栈底到栈顶对应的数单调递增',
        'n = len(nums)': '`n = {n}`，要选 `k = {k}` 个',
        'for index in range(n)': lambda S, B, r: (f'看 `nums[{S.index}] = {S.nums[S.index]}`'
                                                  if B.get('index') != S.get('index') else '扫描结束'),
        'while stack and': _cap_while,
        'stack.pop()': lambda S, B, r: (f'弹出下标 `{B.stack[-1]}`（值 `{S.nums[B.stack[-1]]}`）'
                                        if S.get('_line') == 7 else f'多出来的栈顶 `{B.stack[-1]}:{S.nums[B.stack[-1]]}` 弹掉'),
        'stack.append(index)': '无论如何都压入下标 `{index}`（值 `{nums[index]}`）',
        'while len(stack) > k': lambda S, B, r: (f'`len(stack) = {len(S.stack)} > k`：栈顶的数是多余的' if len(S.stack) > K
                                                 else f'`len(stack) = {len(S.stack)} = k`，正好'),
        'return [nums[index]': '栈底的 k 个下标对应的数就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='在剩余数字充足的前提下，让答案序列单调递增',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['返回 `nums` 长度为 `k` 且==最具竞争力==的子序列',
                 '即长度恰好为 `k` 的==字典序最小==子序列',
                 '示例：`nums = [3,5,2,6], k = 2` → `[2,6]`',
                 '本视频：`[3,5,2,6,1,7], k = 3` → `[2,1,7]`'],
        quote='总结一下，就是==在保证剩余数字充足的前提下，答案序列满足单调递增==。那么可以从头开始向后一趟扫描，使用单调栈来维护当前的答案序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前数比栈顶小、且弹完后 `栈长 − 1 + 剩下的数 ≥ k`，就弹栈',
              '然后==总是==把当前下标压入（不判断栈满）',
              '扫描完后栈可能超过 k 个（比如末尾一直递增）：==栈底的 k 个==就是答案，多的从栈顶弹掉'],
        result='`[2,1,7]`：看到 1 时不能再弹 2，否则凑不够 3 个',
        summary=['时间 `O(n)`：每个下标至多入栈、出栈各一次',
                 '易错：剩余充足的判断是 `len(stack) - 1 + n - index >= k`（弹完后还够）',
                 '对比灵神：灵神入栈前判 `len(st) < k`，栈永远不超过 k；yiduobo 先全压再截断',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
