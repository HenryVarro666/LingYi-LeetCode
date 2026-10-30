CONFIG = dict(
    num=1345, title='跳跃游戏 IV', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='BFS + 哈希表（相同值只展开一次）',
    tags=['难度分 1810'],
    code='''
class Solution:
    def minJumps(self, arr: list[int]) -> int:
        pos = defaultdict(list)  # 元素值 -> [下标]
        for i, x in enumerate(arr):
            pos[x].append(i)

        n = len(arr)
        vis = [False] * n
        vis[0] = True
        q = [0]  # 起点

        for ans in count(0):
            tmp = q
            q = []
            for i in tmp:
                if i == n - 1:  # 到达终点
                    return ans

                # 往右
                if not vis[i + 1]:
                    vis[i + 1] = True
                    q.append(i + 1)

                # 往左
                if i > 0 and not vis[i - 1]:
                    vis[i - 1] = True
                    q.append(i - 1)

                # 访问所有元素值为 arr[i] 的点（下标）
                x = arr[i]
                if x not in pos:  # 之前访问过
                    continue
                for j in pos[x]:
                    if not vis[j]:
                        vis[j] = True
                        q.append(j)
                del pos[x]  # 避免重复访问
''',
    call='Solution().minJumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404])',
    expect=3,
    setup='from itertools import count',
    views=[
        dict(type='array', var='arr', label='arr（绿 = 已访问；蓝 = 当前展开的下标 i）', cell=70, h=170, pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if i == S.get('i') else 'green' if S['vis'][i] else None) if 'vis' in S else None),
        dict(type='map', var='pos', label='pos（值 → 下标列表；用过的值会被删掉）', h=180, font=24),
        dict(type='array', var='q', label='q（下一层）', cell=60, h=130),
        dict(type='text', h=60, fn=lambda S: f"BFS 第 `{S['ans']}` 层：这一层的点都是 =={S['ans']}== 步到达" if 'ans' in S else ''),
    ],
    watch=[('ans', 'ans', 'green'), ('i', 'i', 'blue'), 'x', 'n'],
    captions={
        'n = len(arr)': '先扫一遍建好 `pos`：值 → 所有下标。`n = {n}`，终点是下标 `{n - 1}`',
        'vis = [False]': '`vis[i]` 标记下标 i 是否入过队',
        'vis[0] = True': '起点下标 0 已访问',
        'q = [0]': '队列从起点 `0` 开始',
        'for ans in count(0)': '第 `{ans}` 层 BFS：队列里的点都是 `{ans}` 步能到的',
        14: '`q` 清空，用来装下一层',
        'tmp = q': '`tmp` 取出这一层的所有点',
        'if i == n - 1': lambda S, B, r: (f'`i = {S.i}` 是终点 → 最少 `{S.ans}` 步，返回' if S.i == S.n - 1 else f'`i = {S.i}` 不是终点 `{S.n - 1}`，往外扩展'),
        'if not vis[i + 1]': lambda S, B, r: (f'往右：`{S.i + 1}` 没访问过 → 入队' if not S.vis[S.i + 1] else f'往右：`{S.i + 1}` 已访问过'),
        'if i > 0 and not vis[i - 1]': lambda S, B, r: (f'往左：`{S.i - 1}` 没访问过 → 入队' if S.i > 0 and not B.vis[S.i - 1] else ('已经在最左边，不能往左' if S.i == 0 else f'往左：`{S.i - 1}` 已访问过')),
        'x = arr[i]': '当前值 `x = {x}`：同值的点都能一步跳到',
        'if x not in pos': lambda S, B, r: (f'`{S.x}` 不在 `pos` 里：这个值之前已经展开过 → 同值的点都入队了，`continue`' if S.x not in S.pos
                                            else f'`pos[{S.x}] = {S.pos[S.x]}`：这个值第一次出现，一次性访问所有同值点'),
        'for j in pos[x]': '枚举同值下标 `j`',
        'if not vis[j]': lambda S, B, r: (f'`{S.j}` 没访问过 → 入队' if not B.vis[S.j] else f'`{S.j}` 已访问过，跳过'),
        'del pos[x]': '把 `{x}` 从哈希表删掉：同值的点已全部入队，之后不会再遍历（均摊 `O(n)` 的关键）',
        'return ans': '返回 =={ans}==',
    },
    skip=['pos[x].append', 'continue', 'vis[i + 1] = True', 'vis[i - 1] = True', 'vis[j] = True', 'q.append(i + 1)', 'q.append(i - 1)', 'q.append(j)', 'pos = defaultdict', 'for i, x in enumerate'],
    max_steps=70,
    cards=dict(
        one_liner='相同值的点之间都有边：展开一次后就把这个值从表里删掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 出发，每步可跳到 `i+1`、`i-1`，或任意满足 `arr[j] == arr[i]` 的下标 `j`',
                 '求到达最后一个下标的最少步数',
                 '示例：`[100,-23,-23,404,100,23,23,23,3,404]` → `3`（0→4→3→9）'],
        quote='对于元素 x，我们可以在把所有与元素 x 相同的点（下标）入队后，删除哈希表中的 x。这样可以保证哈希表中的每个下标至多访问一次，从而做到 O(n) 时间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['建图：`i ↔ i+1`，且所有点权相同的点两两相连；求 `0` 到 `n-1` 的最短路',
              '同值边最坏 `O(n²)` 条，不能逐条遍历',
              '用哈希表存「值 → 下标列表」，第一次遇到某个值就把整串入队，然后 `del pos[x]`'],
        summary=['时间 `O(n)`：每个下标至多入队出队一次，哈希表里每个下标最多被扫一次',
                 '易错点：不删 `pos[x]` 会退化成 `O(n²)`（全是相同值时）',
                 '双列表 BFS：`tmp` 当前层，`q` 下一层，`ans` 就是层数',
                 '相似题：3629 通过质数传送到达终点的最少跳跃次数'],
    ),
)
