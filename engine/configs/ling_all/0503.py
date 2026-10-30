NUMS = [1, 2, 1]


def _while(S, B, ret):
    st, x, a = B.st, B.x, B.nums
    if st and x > a[st[-1]]:
        return f'`x = {x} > nums[{st[-1]}] = {a[st[-1]]}`：==x 就是栈顶的下一个更大元素=='
    if st:
        return f'`x = {x} ≤ nums[{st[-1]}] = {a[st[-1]]}`：栈顶还没等到更大的数，停止弹栈'
    return '栈为空：没有待办的下标'


def _if(S, B, ret):
    if S.i < S.n:
        return f'`i = {S.i} < n = {S.n}`：第一圈的下标==入栈==，等它的答案'
    return f'`i = {S.i} ≥ n`：复制出来的部分==只负责当答案==，不入栈（每个下标只入栈一次）'


def _show(S):
    if 'x' not in S:
        return '把 `nums` 复制一份拼在右边，环形数组就变成了一般数组'
    i, n = S['i'], S['n']
    tail = '（复制部分）' if i >= n else ''
    return f'`i = {i}` → `x = nums[{i} % {n}] = nums[{i % n}]` = =={S["x"]}=={tail}'


CONFIG = dict(
    num=503, title='下一个更大元素 II', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 从左到右遍历两圈',
    tags=['labuladong', '灵神题单·单调栈'],
    code='''
class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        st = []

        for i in range(n * 2):
            x = nums[i % n]
            while st and x > nums[st[-1]]:
                # x 是 nums[st[-1]] 的下一个更大元素
                # 既然 nums[st[-1]] 已经算出答案，则从栈顶弹出
                ans[st.pop()] = x
            if i < n:
                st.append(i)

        return ans
''',
    call=f'Solution().nextGreaterElements({NUMS})',
    expect=[2, -1, 2],
    views=[
        dict(type='text', fn=_show, size=28, h=60),
        dict(type='array', var=lambda S: S['nums'] * 2 if 'nums' in S else None,
             label='nums 拼两份（下标 0..n−1 是原数组，n..2n−1 是复制的）', cell=96,
             pointers={'i': 'blue'},
             dim=lambda S, i, v: 'i' in S and i < S['i'] and i not in (S.get('st') or []),
             color=lambda S, i, v: 'blue' if i == S.get('i') else ('purple' if i in (S.get('st') or []) else None)),
        dict(type='array', var='ans', label='ans（绿 = 已找到答案）', cell=96,
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='stack', var='st', label='st（todolist，存下标  下标:值）', fmt=lambda i: f'{i}:{NUMS[i]}', h=125, font=30),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('st', 'st', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'ans = [-1]': '`ans` 先全填 `-1`：最后还留在栈里的，就是找不到更大元素的',
        'st = []': '栈 `st` 存==还没算出答案的下标==（todolist）',
        'for i in range': lambda S, B, ret: ('遍历结束' if 'i' in B and B.i == S.i else
                                             (f'第一圈：`i = {S.i}`' if S.i < S.n else
                                              f'第二圈：`i = {S.i}`，对应复制出来的 `nums[{S.i % S.n}]`')),
        'x = nums[i % n]': lambda S, B, ret: (f'`x = nums[{S.i}] = {S.x}`' if S.i < S.n else
                                              f'`x = nums[{S.i} % {S.n}] = nums[{S.i % S.n}] = {S.x}`：==下标模 n==，不用真的复制数组'),
        'while st and': _while,
        'ans[st.pop()] = x': '弹出下标 `{B.st[-1]}`，记录答案 `ans[{B.st[-1]}] = {x}`',
        'if i < n': _if,
        'st.append(i)': '下标 `{i}`（值 `{x}`）入栈',
        'return ans': '栈里剩下的下标没有更大元素，保持 `-1` → 返回 =={ans}==',
    },
    cards=dict(
        one_liner='把数组复制一份拼在后面，环形就变成了一般数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是==循环数组==：`nums[n−1]` 的下一个元素是 `nums[0]`',
                 '求每个元素的下一个更大元素（要绕回开头找），不存在则 `-1`',
                 '示例：`[1,2,1]` → `[2,-1,2]`；`[1,2,3,4,3]` → `[2,3,4,-1,4]`'],
        quote='我们可以把 nums 复制一份，拼在 nums 右边，这样就把环形数组变成一般数组了。例如 [1,2,1] 变成 [1,2,1,1,2,1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['栈中记录还没算出答案的==下标==，把栈视作 todolist',
              '遍历 `2n` 次，`x = nums[i % n]`；`x` 比栈顶大，栈顶的答案就是 `x`',
              '只有 `i < n` 时入栈：复制部分只用来给前面的下标当答案'],
        summary=['时间 `O(n)`：每个下标最多入栈、出栈各一次；空间 `O(n)`',
                 '不用真的复制数组，下标对 `n` 取模即可',
                 '栈里存下标而不是值：要写 `ans[下标]`',
                 '另一种写法：从右到左遍历 `2n−1..0`，栈里存下一个更大元素的候选值'],
    ),
)
