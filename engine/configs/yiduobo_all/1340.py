ARR = [3, 1, 4, 2]
D = 2


def _txt(S):
    if 'left' not in S:
        return f'`d = {D}`：单调栈求每个位置左右「下一跳」候选（值最大的那批），再记忆化 dfs'
    r = S.get('right')
    return f'`left = {S["left"]}`' + (f'\n`right = {r}`' if r is not None else '')


def _cand(S, B, ret, side):
    lst = S['left'] if side == 'left' else S['right']
    return lst


CONFIG = dict(
    num=1340, title='跳跃游戏 V', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='单调栈求候选落点 + 记忆化 dfs',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 1866'],
    code='''
class Solution(object):
    def maxJumps(self, arr, d):

        n = len(arr)
        stack = [0]
        left = [None]
        for index in range(1, n):
            left.append(None)
            while stack and arr[stack[-1]] < arr[index]:
                if index - stack[-1] <= d:
                    if left[-1] is None or arr[left[-1][0]] < arr[stack[-1]]:
                        left[-1] = [stack[-1]]
                    else:
                        left[-1].append(stack[-1])
                stack.pop()
            stack.append(index)
        
        stack = [n - 1]
        right = [None]
        for index in range(n - 2, -1, -1):
            right.append(None)
            while stack and arr[stack[-1]] < arr[index]:
                if stack[-1] - index <= d:
                    if right[-1] is None or arr[right[-1][0]] < arr[stack[-1]]:
                        right[-1] = [stack[-1]]
                    else:
                        right[-1].append(stack[-1])
                stack.pop()
            stack.append(index)
        right.reverse()

        f = [None] * n
        for index in range(n):
            if f[index] is None:
                self.dfs(index, f, left, right)
        
        return max(f)
    
    def dfs(self, now, f, left, right):
        if f[now] is None:
            tmp = 0
            if left[now] is not None:
                for next in left[now]:
                    tmp = max(tmp, self.dfs(next, f, left, right))
            if right[now] is not None:
                for next in right[now]:
                    tmp = max(tmp, self.dfs(next, f, left, right))
            f[now] = tmp + 1
        
        return f[now]
''',
    call=f'Solution().maxJumps({ARR!r}, {D})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=24, h=100),
        dict(type='bars', var='arr', label='arr（蓝 = 当前 index，粉 = dfs 的 now）', h=210,
             pointers={'index': 'blue', 'now': 'pink'},
             color=lambda S, i, v: 'yellow' if i in S.get('stack', ()) and i != S.get('index') else None),
        dict(type='stack', var='stack', label='stack（下标:值，单调递减）', fmt=lambda i: f'{i}:{ARR[i]}', h=110),
        dict(type='array', var='f', label='f[i]：从 i 起跳最多访问几个位置（· = 还没算）', h=130),
        dict(type='calls', h=150, hide=('dfs',)),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('stack', 'stack', 'purple'), ('f', 'f', 'green')],
    max_steps=130,
    skip=['left = [None]', 'right = [None]', 'left.append(None)', 'right.append(None)', 'right.reverse()', 'tmp = 0', 'stack.append(index)', 'return f[now]'],
    captions={
        'stack = [0]': '正向扫：栈里存下标，值单调递减；先放下标 0',
        'while stack and arr[stack[-1]] < arr[index]': lambda S, B, r: (
            f'`index = {S.index}`（值 {S.arr[S.index]}）：' + ('栈空，不再弹' if not S.stack else
            f'栈顶 `arr[{S.stack[-1]}] = {S.arr[S.stack[-1]]}` ' + ('更小 → 它能跳到 index 吗？看距离' if S.arr[S.stack[-1]] < S.arr[S.index] else '不更小，停止弹栈'))),
        'if index - stack[-1] <= d': '距离 `{index} - {stack[-1]} = {index - stack[-1]}` ' + '{"≤" if index - stack[-1] <= d else ">"} `d = {d}`：{"在射程内，是候选" if index - stack[-1] <= d else "太远，跳不到"}',
        'if left[-1] is None or': lambda S, B, r: ('`index` 还没有候选，直接记下' if S.left[-1] is None else
            f'已有候选值 `{S.arr[S.left[-1][0]]}`，和新的 `{S.arr[S.stack[-1]]}` 比：' + ('新的更大 → 替换（只留最大的那批）' if S.arr[S.left[-1][0]] < S.arr[S.stack[-1]] else '一样大 → 一起保留')),
        'left[-1] = [stack[-1]]': '`index = {index}` 的左侧候选改为 `{left[-1]}`',
        'left[-1].append': '一样大也都能跳：左侧候选变成 `{left[-1]}`',
        'stack.pop()': '下标 `{B.stack[-1]}` 出栈：右边出现了更大的数，对 index 之后的位置它都被挡住了',
        'stack.append(index)': '`index = {index}` 入栈',
        'stack = [n - 1]': '反向扫一遍，同样的方法求右侧候选',
        'if stack[-1] - index <= d': '距离 `{stack[-1]} - {index} = {stack[-1] - index}` {"≤" if stack[-1] - index <= d else ">"} `d = {d}`',
        'if right[-1] is None or': lambda S, B, r: ('还没有候选，直接记下' if S.right[-1] is None else
            f'已有候选值 `{S.arr[S.right[-1][0]]}`，和新的 `{S.arr[S.stack[-1]]}` 比：' + ('新的更大 → 替换' if S.arr[S.right[-1][0]] < S.arr[S.stack[-1]] else '一样大 → 一起保留')),
        'right[-1] = [stack[-1]]': '右侧候选改为 `{right[-1]}`',
        'right[-1].append': '右侧候选变成 `{right[-1]}`',
        'f = [None] * n': '`f[i]`：从 i 起跳最多访问几个位置，None 表示没算过',
        'if f[index] is None': '`f[{index}]` {"还没算 → 调用 dfs" if f[index] is None else "算过了，跳过"}',
        'self.dfs(index': '进入 `dfs({index})`',
        'if f[now] is None': '`f[{now}]` {"没算过，往下算" if f[now] is None else "已算过，直接用（记忆化）"}',
        'for next in left[now]': '枚举左侧候选 `{left[now]}`：下一跳 `next = {next}`',
        'for next in right[now]': '枚举右侧候选 `{right[now]}`：下一跳 `next = {next}`',
        'tmp = max(tmp': '要用下一跳 `{next}` 的结果：先 `dfs({next})`（算过就直接取 `f`），再和 `tmp` 取较大',
        'f[now] = tmp + 1': '`f[{now}] = {tmp} + 1 = {f[now]}`：加上自己',
        'return f[now]': '`dfs({now})` 返回 `{f[now]}`',
        'return max(f)': '答案取所有起点的最大值 `{ret}`',
    },
    cards=dict(
        one_liner='每个位置只需考虑「落点里最高的那批」下一跳',
        complexity='时间 `O(n)`（均摊），空间 `O(n)`',
        problem=['一次最多跳 `d` 格，只能跳到更矮的柱子，且中间的柱子都要比出发点矮',
                 '可以从任意下标出发，求最多访问多少个下标',
                 '本视频：`arr = [3,1,4,2]`，`d = 2` → `3`'],
        quote='对于每个位置p，实际上可以选择的下一跳的位置并不多。',
        quote_src='—— yiduobo 题解原文',
        idea=['能跳到的位置里，==值最大的那些==才值得跳：先跳到 `i` 再跳到 `j`，比直接跳到 `j` 更优',
              '正反两趟单调栈，求出每个位置左右两侧射程内「最大值」的下标列表',
              '`f[i]` = 候选下一跳的 `f` 最大值 + 1，用 dfs 记忆化计算'],
        summary=['时间 `O(n)`：每个位置至多成为一次左候选、一次右候选，均摊 `O(1)`',
                 '相同的最大值都要保留（候选是列表），所以才有 `append` 分支',
                 '栈里存下标、值单调递减；右边出现更大的数就弹出旧的',
                 '原文只用到 `-`、`+`，无需 Python 2 改动',
                 '对比灵神：灵神只取左右「最近更大」两个来源倒着跳；yiduobo 正着跳，保留射程内最大的一批落点'],
    ),
)
