CONFIG = dict(
    num=1306, title='跳跃游戏 III', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='DFS 遍历有向图', tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 1397'],
    code='''
class Solution:
    def canReach(self, arr: list[int], start: int) -> bool:
        n = len(arr)
        vis = [False] * n

        def dfs(i: int) -> bool:
            if not 0 <= i < n or vis[i]:  # 出界，或者之前访问过（没找到）
                return False
            if arr[i] == 0:  # 找到了
                return True
            vis[i] = True  # 避免重复访问
            return dfs(i + arr[i]) or dfs(i - arr[i])

        return dfs(start)
''',
    call='Solution().canReach([4,2,3,0,3,1,2], 5)',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 已访问，蓝箭头 = 当前下标 i，绿 = 值为 0 的目标）', cell=100, h=230,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if v == 0 else ('blue' if S.get('vis') and S['vis'][i] else None)),
        dict(type='text', h=70, fn=lambda S: (f"从 `{S['i']}` 出发：可以跳到 `{S['i']} + {S['arr'][S['i']]} = {S['i'] + S['arr'][S['i']]}` 或 `{S['i']} − {S['arr'][S['i']]} = {S['i'] - S['arr'][S['i']]}`"
                                               if 'i' in S and 0 <= S['i'] < len(S['arr']) else '下标出界，这条路走不通')),
        dict(type='calls', h=250),
    ],
    watch=['start', 'i', ('vis', lambda S: ''.join('1' if x else '0' for x in S['vis']) if 'vis' in S else '')],
    captions={
        'vis = [False]': '`vis[i]` 记录下标 i 有没有访问过，初始全是 False',
        'if not 0 <= i < n': lambda S, B, r: (f'`i = {S.i}` 出界 → 返回 False' if not 0 <= S.i < S.n
                                              else (f'`vis[{S.i}]` 已访问过 → 之前来过没找到，返回 False' if S.vis[S.i] else f'`i = {S.i}` 在范围内且没访问过，继续')),
        'if arr[i] == 0': lambda S, B, r: (f'`arr[{S.i}] = 0` → ==找到了==，返回 True' if S.arr[S.i] == 0 else f'`arr[{S.i}] = {S.arr[S.i]}` 不是 0，还得往下跳'),
        'vis[i] = True': '先标记 `{i}` 已访问，==避免重复访问==（不然会在环里转圈）',
        'return dfs(i + arr[i])': '从 `{B.i}` 往两边跳：先递归 `dfs({B.i} + {B.arr[B.i]})`，不行再 `dfs({B.i} - {B.arr[B.i]})`，==or 有一边为真就够了==',
        'return dfs(start)': '从起点 `{start}` 开始 DFS',
        'return False': '`dfs({i})` 返回 False',
        'return True': '`dfs({i})` 返回 True，一路传回起点',
    },
    cards=dict(
        one_liner='把跳跃看成有向图：从起点 DFS，找到值为 0 的点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr` 非负，站在下标 `i` 可以跳到 `i + arr[i]` 或 `i - arr[i]`，不能出界',
                 '问能否从 `start` 跳到某个值为 0 的下标',
                 '示例：`arr=[4,2,3,0,3,1,2], start=5` → `true`'],
        quote='给你一个 n 个节点的有向图，节点编号从 0 到 n-1。图中的边为 i→i+arr[i] 和 i→i-arr[i]（如果节点存在）。从 start 开始，DFS（或者 BFS）访问这张图。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个下标是一个点，向 `i±arr[i]` 各连一条边',
              '问题变成：起点能否到达某个 `arr[i]=0` 的点',
              '`vis` 防止在环里无限递归；找到目标立刻返回 True'],
        summary=['时间 `O(n)`：每个点最多访问一次，边只有 2n 条',
                 '空间 `O(n)`：`vis` 数组和递归栈',
                 '易错：出界判断要先于 `vis[i]` 访问，否则下标越界',
                 '先判断 `arr[i]==0` 再标记 `vis`，找到目标就不用标记了',
                 '也可以用 BFS；本题还能用 DP 的视角理解成可达性'],
    ),
)
