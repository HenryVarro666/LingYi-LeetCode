def _rows(S):
    n = len(S['arr'])

    def pad(name, f):
        v = S.get(name)
        return [f(x) for x in v] if v is not None else ['-'] * n
    return [pad('next_odd', lambda x: x), pad('next_even', lambda x: x),
            pad('odd', lambda x: 'T' if x else 'F'), pad('even', lambda x: 'T' if x else 'F')]


CONFIG = dict(
    num=975, title='奇偶跳', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='排序下标 + 单调栈求落点 + 倒推 DP',
    tags=['灵神题单·单调栈', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def oddEvenJumps(self, arr):

        n = len(arr)
        
        sorted_index = sorted(range(n), key = lambda x:(arr[x], x))
        next_odd = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and stack[-1] < sorted_index[index]:
                stack.pop()
            
            if stack:
                next_odd[sorted_index[index]] = stack[-1]

            stack.append(sorted_index[index])

        sorted_index = sorted(range(n), key = lambda x:(-arr[x], x))
        next_even = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and stack[-1] < sorted_index[index]:
                stack.pop()
            
            if stack:
                next_even[sorted_index[index]] = stack[-1]
            
            stack.append(sorted_index[index])

        odd = [False] * n
        even = [False] * n
        odd[-1] = even[-1] = True
        res = 1
        for index in range(n - 2, -1, -1):
            if next_odd[index] != -1 and even[next_odd[index]]:
                odd[index] = True
                res += 1
            if next_even[index] != -1 and odd[next_even[index]]:
                even[index] = True

        return res
''',
    call='Solution().oddEvenJumps([2,3,1,1,4])',
    expect=3,
    views=[
        dict(type='array', var='arr', h=110, label='arr',
             color=lambda S, i, v: 'blue' if 'index' in S and 'sorted_index' in S and S['_line'] in (9, 10, 11, 14, 21, 22, 23, 26) and i == S['sorted_index'][S['index']] else None),
        dict(type='array', var='sorted_index', h=110, label='sorted_index：下标按数值排序', pointers={'index': 'pink'}),
        dict(type='stack', var='stack', h=120, fmt=lambda i: f'下标{i}'),
        dict(type='table', h=270, var=_rows, rows=['奇落点', '偶落点', 'odd', 'even'], label='奇偶落点（-1 无）、odd/even（T 能到终点）',
             color=lambda S, r, c, v: 'green' if v not in ('-', 'F', -1) else None),
    ],
    watch=[('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'sorted_index = sorted(range(n), key = lambda x:(arr[x], x))': '奇数跳要找 ==>= 且最小== 的值：先把下标按 `(值, 下标)` 从小到大排好 → `{sorted_index}`',
        'next_odd = [-1] * n': '`next_odd[i]`：奇数跳的落点（先全设 -1）；单调栈 `stack` 存还可能当落点的下标',
        9: lambda S, B, r: (
            f'倒着扫排好序的下标：`index = {S.index}`，当前下标 `{S.sorted_index[S.index]}`' if not (B.get('index') == S.index == 0) else '扫描结束'),
        10: lambda S, B, r: (
            f'栈顶 `{S.stack[-1]}` < 当前下标 `{S.sorted_index[S.index]}`：它在当前下标左边，不能当落点（只能向右跳）→ 弹出' if S.stack and S.stack[-1] < S.sorted_index[S.index]
            else ('栈空了：没有可跳的落点' if not S.stack else f'栈顶 `{S.stack[-1]}` 在当前下标右边，保留；当前下标随后入栈')),
        11: '弹出：当前下标 `{sorted_index[index]}` 比它大，排在更前面的下标也只会选当前下标，用不到它了',
        23: '栈顶在左边，弹出',
        14: '栈顶 `{stack[-1]}` 是下标 `{sorted_index[index]}` 右边、值不小于它里最近的 → 落点 `next_odd[{sorted_index[index]}] = {stack[-1]}`',
        'sorted_index = sorted(range(n), key = lambda x:(-arr[x], x))': '偶数跳要找 ==<= 且最大==：按 `(-值, 下标)` 排序，其余流程和奇数跳一样',
        21: lambda S, B, r: (
            f'倒着扫：`index = {S.index}`，当前下标 `{S.sorted_index[S.index]}`' if not (B.get('index') == S.index == 0) else '扫描结束'),
        22: lambda S, B, r: (
            f'栈顶 `{S.stack[-1]}` < 当前下标 `{S.sorted_index[S.index]}`：在左边，弹出' if S.stack and S.stack[-1] < S.sorted_index[S.index]
            else ('栈空了：没有可跳的落点' if not S.stack else f'栈顶 `{S.stack[-1]}` 在右边，保留；当前下标随后入栈')),
        26: '`next_even[{sorted_index[index]}] = {stack[-1]}`',
        'odd[-1] = even[-1] = True': '终点本身：不管下一跳是奇是偶，都已经到了 → 两个都是 True',
        'res = 1': '`res` 数好起点：终点本身算 1 个（奇数跳起点能到终点才算）',
        'for index in range(n - 2, -1, -1)': lambda S, B, r: (
            f'从后往前倒推：`index = {S.index}`' if S.index != B.get('index') else '倒推结束'),
        'if next_odd[index] != -1': lambda S, B, r: (
            f'奇数跳落点 `{S.next_odd[S.index]}`；落点处下一跳是偶数跳，`even[{S.next_odd[S.index]}] = {S.even[S.next_odd[S.index]]}`' if S.next_odd[S.index] != -1
            else f'`index = {S.index}` 没有奇数跳落点：卡住了，`odd[{S.index}]` 保持 False'),
        'odd[index] = True': '`odd[{index}] = True`：先奇数跳到 `{next_odd[index]}`，之后能到终点',
        'res += 1': '奇数跳起点能到终点 → `res` = =={res}==',
        'if next_even[index] != -1': lambda S, B, r: (
            f'偶数跳落点 `{S.next_even[S.index]}`；落点处下一跳是奇数跳，`odd[{S.next_even[S.index]}] = {S.odd[S.next_even[S.index]]}`' if S.next_even[S.index] != -1
            else f'`index = {S.index}` 没有偶数跳落点：`even[{S.index}]` 保持 False'),
        'even[index] = True': '`even[{index}] = True`：先偶数跳到 `{next_even[index]}`，之后能到终点',
        'return res': '一共 `{res}` 个好起点',
    },
    skip=['n = len(arr)', 'odd = [False]', 'even = [False]', 'if stack:', 'stack.append(sorted_index[index])', 'next_even = [-1]', 'stack = []'],
    max_steps=140,
    cards=dict(
        one_liner='先求每个点奇数跳、偶数跳的落点，再从终点往回倒推',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['从某个下标起跳，第 1、3、5… 次是奇数跳，第 2、4… 次是偶数跳',
                 '奇数跳：跳到右边 `arr[j] >= arr[i]` 中值最小的（相同取最小下标）',
                 '偶数跳：跳到右边 `arr[j] <= arr[i]` 中值最大的；能到末尾的起点是好起点，数一数',
                 '本视频示例：`[2,3,1,1,4]` → `3`'],
        quote='一旦选择了起点，那么整个跳跃的路径都是确定好了的，我们只需要判断出奇数跳和偶数跳时，从每个点起跳的目标点是哪一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把下标按数值排序，再倒着扫，用单调栈找落点（不用平衡树）',
              '栈顶下标比当前小就弹出：它在左边，跳不过去',
              '落点出来后倒推：`odd[i]` 看落点的 `even`，`even[i]` 看落点的 `odd`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '偶数跳只是排序键换成 `-arr[x]`，最后答案数 ==odd== 为真的个数（奇数跳起头）',
                 '落点为 -1 时要先判断，再访问 `even[...]` / `odd[...]`',
                 '题解没有给题面，题意按 LeetCode 975 原题补写'],
    ),
)
