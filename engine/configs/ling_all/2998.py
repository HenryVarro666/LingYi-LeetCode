CONFIG = dict(
    num=2998, title='使 X 和 Y 相等的最少操作次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='图论建模 + BFS 最短路（双数组）',
    tags=['图论算法', '难度分 1795'],
    code='''
class Solution:
    def minimumOperationsToMakeEqual(self, x: int, y: int) -> int:
        if x <= y:
            return y - x
        ans = x - y  # 总操作次数不会超过 x-y
        vis = [False] * (x + ans + 1)  # +1 操作至多执行 x-y 次
        q = []
        step = 0

        def add(v: int) -> None:
            if v < y:
                nonlocal ans
                ans = min(ans, step + 1 + y - v)  # 只能执行 +1 操作
            elif not vis[v]:
                vis[v] = True
                q.append(v)

        add(x)
        while True:
            tmp = q
            q = []
            for v in tmp:
                if v == y:
                    return min(ans, step)
                if v % 11 == 0:
                    add(v // 11)
                if v % 5 == 0:
                    add(v // 5)
                add(v - 1)
                add(v + 1)
            step += 1
''',
    call='Solution().minimumOperationsToMakeEqual(26, 1)',
    expect=3,
    views=[
        dict(type='text', h=70, fn=lambda S: f"目标 `y = {S['y']}`；当前层数 `step` = =={S['step']}==；只用 +1 能到的候选答案 `ans` = ==" + f"{S['ans']}==" if 'step' in S and 'ans' in S else ''),
        dict(type='array', var='tmp', label='tmp（当前这一层的点）', cell=70, h=170, pointers={lambda S: S['_inner'].get('v') and S['tmp'].index(S['_inner']['v']) if S['_inner'].get('v') in S.get('tmp', []) else None: 'blue'}),
        dict(type='array', var='q', label='q（下一层的点，刚入队的是绿色）', cell=70, h=170,
             color=lambda S, i, v: 'green' if i == len(S['q']) - 1 and S['_inner'].get('v') is not None and S['_line'] in (16, 17) else None),
    ],
    watch=['v', ('step', 'step', 'blue'), ('ans', 'ans', 'green'), 'x', 'y'],
    captions={
        'if x <= y': lambda S, B, r: (f'`x = {S.x} <= y = {S.y}`：只能不停 +1 → 直接返回 `y - x`' if S.x <= S.y
                                      else f'`x = {S.x} > y = {S.y}`：要减小 x，需要搜索'),
        'ans = x - y': '只用 -1 就能到 y，所以答案不会超过 `x - y = {ans}`',
        'vis = [False]': '`vis[v]` 标记数字 v 是否访问过；+1 最多执行 x−y 次，所以长度开 `x + ans + 1`',
        7: '`q` 存下一层的点，`step` 是从 x 出发走的步数（层数）',
        21: '`q` 清空，准备装下一层',
        'add(x)': '把起点 `x = {x}` 放进队列',
        
        'if v == y': lambda S, B, r: (f'`v = y = {S.y}`：BFS 第一次到达 y，层数 `step = {S.step}` 就是最短路 → 返回 `min(ans, step)`' if S.v == S.y
                                      else f'`v = {S.v}` 还不是 `y = {S.y}`'),
        'if v % 11 == 0': lambda S, B, r: (f'`{S.v} % 11 == 0`：能除以 11 → 连一条边到 `{S.v // 11}`' if S.v % 11 == 0 else f'`{S.v}` 不是 11 的倍数，没有这条边'),
        'if v % 5 == 0': lambda S, B, r: (f'`{S.v} % 5 == 0`：能除以 5 → 连一条边到 `{S.v // 5}`' if S.v % 5 == 0 else f'`{S.v}` 不是 5 的倍数，没有这条边'),
        'add(v - 1)': '减一操作：邻居 `{B.v - 1}`',
        'add(v + 1)': '加一操作：邻居 `{B.v + 1}`',
        'if v < y': lambda S, B, r: (f'`{S.v} < y = {S.y}`：比 y 小的数不用入队，只能靠 +1 走到 y，总代价 `step + 1 + y - v` → 更新 `ans`' if S.v < S.y
                                     else f'`{S.v} >= y`：正常的点，看有没有访问过'),
        'ans = min': '`ans = min(ans, {step} + 1 + {y} - {v}) = {ans}`',
        'elif not vis[v]': lambda S, B, r: (f'`{S.v}` 没访问过 → 入队' if not B.vis[S.v] else f'`{S.v}` 已访问过 → 不重复入队'),
        'vis[v] = True': '标记 `{v}` 已访问（入队时标记，保证每个点只入队一次）',
        'q.append(v)': '`{v}` 加入下一层队列：`q = {q}`',
        'step += 1': '这一层处理完，层数 `step` → {step}',
        'return min': '返回 `min(ans, step)` = =={ret}==',
    },
    skip=['nonlocal'],
    max_steps=80,
    cards=dict(
        one_liner='每个操作都是一条边：在图上 BFS 求最短路',
        complexity='时间 `O(x)`，空间 `O(x)`',
        problem=['正整数 `x`、`y`，每次可：被 11 整除就除以 11；被 5 整除就除以 5；`x-1`；`x+1`',
                 '求让 `x` 等于 `y` 的最少操作次数',
                 '示例：`x=26, y=1` → `3`（减 1，除 5，除 5）'],
        quote='每个操作都可以理解成：从 x 向操作后的数连边。在这张图上跑 BFS，求出从 x 到 y 的最短路，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x <= y` 只能 +1，答案直接是 `y - x`',
              '否则从 `x` 开始 BFS：每个点最多连 4 条边，边权都是 1',
              '比 `y` 小的点不再入队，直接算「再 +1 走到 y」的代价更新 `ans`，避免数组越界'],
        summary=['时间 `O(x)`，空间 `O(x)`；`vis` 长度 `x + (x-y) + 1`',
                 '双数组 BFS：`tmp` 是当前层，`q` 是下一层，`step` 就是层数',
                 '易错点：`v < y` 时不能入队，要用 `ans` 记录「走到 v 后只靠 +1」的方案',
                 '灵神另给了记忆化搜索写法（枚举先加减到 11 / 5 的倍数再除），状态数只有 `O(log^2)`，此处不演示'],
    ),
)
