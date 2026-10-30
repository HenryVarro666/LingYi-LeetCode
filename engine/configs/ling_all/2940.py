def _qs_line(S):
    qs = S.get('qs')
    if qs is None:
        return ''
    parts = [f'位置{b}: {v}' for b, v in enumerate(qs) if v]
    return '离线询问 `qs[b]` = (heights[a], 询问编号)：' + ('；'.join(parts) if parts else '（空）')


CONFIG = dict(
    num=2940, title='找到 Alice 和 Bob 可以相遇的建筑', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线 + 最小堆',
    tags=['难度分 2327'],
    code='''
class Solution:
    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        ans = [-1] * len(queries)
        qs = [[] for _ in heights]
        for i, (a, b) in enumerate(queries):
            if a > b:
                a, b = b, a  # 保证 a <= b
            if a == b or heights[a] < heights[b]:
                ans[i] = b  # a 直接跳到 b
            else:
                qs[b].append((heights[a], i))  # 离线询问

        h = []
        for i, x in enumerate(heights):
            while h and h[0][0] < x:
                # 堆顶的 heights[a] 可以跳到 heights[i]
                ans[heappop(h)[1]] = i
            for q in qs[i]:
                heappush(h, q)  # 后面再回答
        return ans
''',
    call='Solution().leftmostBuildingQueries([6,4,8,5,2,7], [[0,1],[0,3],[2,4],[3,4],[2,2]])',
    expect=[2, 5, -1, 5, 2],
    views=[
        dict(type='bars', var='heights', label='heights（黄 = 当前 i）', h=250,
             color=lambda S, k, v: 'yellow' if S.get('_line', 0) >= 14 and S.get('i') == k else None),
        dict(type='text', fn=_qs_line, h=95, size=22),
        dict(type='heap', var='h', label='h 最小堆 = (heights[a], 询问编号)', fmt=lambda t: f'({t[0]},q{t[1]})', top_color='blue', h=110),
        dict(type='array', var='ans', label='ans（-1 = 还没答案）', h=130,
             color=lambda S, k, v: 'green' if v != -1 else None),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'orange'), ('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'ans = [-1]': '答案先全填 `-1`（不能相遇）',
        'qs = [[]': '`qs[b]`：把「以 b 为右端点的询问」挂在位置 b，==离线==处理',
        'if a > b': lambda S, B, r: (f'询问 {S.i} = `({S.a}, {S.b})`' if 'a' in S else '') + ('：`a > b` → 交换' if S.a > S.b else '：`a ≤ b`，不用换'),
        'a, b = b, a': '交换后保证 `a ≤ b`：`a = {a}`，`b = {b}`',
        'if a == b or': lambda S, B, r: (
            f'`a == b` 或 `heights[{S.a}] = {S.heights[S.a]} < heights[{S.b}] = {S.heights[S.b]}` → ==a 直接跳到 b=='
            if S.a == S.b or S.heights[S.a] < S.heights[S.b] else
            f'`heights[{S.a}] = {S.heights[S.a]} ≥ heights[{S.b}] = {S.heights[S.b]}`：谁都不能直接跳 → 要找右边更高的楼'),
        'ans[i] = b': '答案就是 `b = {b}`：`ans[{i}] = {b}`',
        'qs[b].append': '记在位置 `b = {b}`：以后某栋楼比 `heights[a] = {heights[a]}` 高，就是答案（它也一定比 `heights[b]` 高）',
        'h = []': '最小堆放「已经入堆的询问」，按 `heights[a]` 从小到大',
        'for i, x in enumerate(heights)': '从左到右扫楼：当前楼 `i = {i}`，高 `x = {x}`',
        'while h and h[0][0] < x': lambda S, B, r: (
            '堆是空的，没有等着回答的询问' if not S.h else
            f'堆顶 `heights[a] = {S.h[0][0]} < x = {S.x}` → 这个询问的 a 能跳到 i，==最左的相遇点就是 i==' if S.h[0][0] < S.x else
            f'堆顶 `{S.h[0][0]} ≥ x = {S.x}`：堆顶最小都跳不上来，==其余更不行==，先不回答'),
        'ans[heappop(h)[1]] = i': lambda S, B, r: f'回答堆顶询问：`ans[{[k for k in range(len(S.ans)) if S.ans[k] != B.ans[k]][0]}] = {S.i}`（从左到右扫，第一次满足的 i 就是最左）',
        'for q in qs[i]': lambda S, B, r: (f'位置 `{S.i}` 有 `{len(S.qs[S.i])}` 个询问挂在这里' if S.qs[S.i] else f'位置 `{S.i}` 没有挂询问'),
        'heappush(h, q)': '`b = {i}` 到了才入堆 `{q}`：之后只比 `heights[a]`，因为 `heights[b] ≤ heights[a]`',
        'return ans': '没被回答的保持 `-1`：右边没有更高的楼。结果 `{ret}`',
    },
    skip=['for q in qs[i]'],
    max_steps=90,
    cards=dict(
        one_liner='把询问挂到较右的 b 上，从左往右扫，最小堆里谁先被超过就回答谁',
        complexity='时间 `O(n + q log q)`，空间 `O(n + q)`',
        problem=['`heights[i]` 是建筑高度，只能从低楼跳到右边更高的楼；每个询问 `(a, b)` 问 Alice 和 Bob 能相遇的==最左==建筑',
                 '不能相遇答 `-1`，`a == b` 时就在原地',
                 '示例：`heights=[6,4,8,5,2,7]`，询问 `[[0,1],[0,3],[2,4],[3,4],[2,2]]` → `[2,5,-1,5,2]`'],
        quote='离线：按照自己定义的某种顺序回答询问，而不是按照输入顺序回答询问。……在位置 b 记录「左边有个 heights[a]，它属于第 i 个询问」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `a ≤ b`。`a == b` 或 `heights[a] < heights[b]` → 直接去 `b`',
              '否则要找 `b` 右边第一个高于 `heights[a]` 的楼：把 `(heights[a], 询问编号)` 挂在位置 `b`',
              '从左往右扫：先回答堆里所有 `heights[a] < x` 的询问，再把挂在 `i` 的询问入堆；堆顶最小，堆顶不行其余也不行'],
        summary=['时间 `O(n + q log q)`，空间 `O(n + q)`',
                 '易错点：必须到位置 `b` 才入堆，否则会把 `b` 左边的楼当成答案',
                 '回答在入堆之前：当前楼 `i` 不能回答挂在 `i` 的询问（`heights[b] ≥ heights[b]`）',
                 '题解另有两种写法：倒序单调栈 + 二分，以及在线的线段树二分（可支持修改）'],
    ),
)
