CONFIG = dict(
    num=1553, title='吃掉 N 个橘子的最少天数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='Dijkstra 最短路（n → n/2、n/3）',
    tags=['灵神题单', '动态规划', '难度分 2048'],
    code='''
class Solution:
    def minDays(self, n: int) -> int:
        dis = defaultdict(lambda: inf)
        h = [(0, n)]
        while True:
            dx, x = heappop(h)
            if x <= 1:
                return dx + x
            if dx > dis[x]:
                continue
            for d in 2, 3:
                y = x // d
                dy = dx + x % d + 1
                if dy < dis[y]:
                    dis[y] = dy
                    heappush(h, (dy, y))
''',
    call='Solution().minDays(10)',
    expect=4,
    views=[
        dict(type='heap', var='h', label='h：最小堆 (天数, 剩余橘子数)', fmt=lambda t: f'{t[0]}天:{t[1]}', h=250),
        dict(type='map', var='dis', label='dis[y]：吃到只剩 y 个橘子的最少天数', fmt=lambda k, v: f'{k}→{v}', font=28, h=190),
        dict(type='text', size=30, h=80, fn=lambda S: (f"出堆 `x = {S['x']}`，已用 `{S['dx']}` 天" if 'x' in S and 'dx' in S else
                                                         '把「剩余橘子数」当节点，边权 = 减 1 的次数 + 1 次除法')),
    ],
    watch=[('dx', 'dx', 'blue'), ('x', 'x', 'pink'), 'd', 'y', 'dy'],
    captions={
        'dis = defaultdict': '`dis[y]` = 目前已知的、把 n 变成 y 的最少天数，默认无穷大',
        'h = [(0, n)]': '起点：还剩 `n = {n}` 个橘子，已用 0 天',
        'heappop(h)': '取出天数最少的状态：`x = {x}`，已用 `{dx}` 天（最短路：先出堆的就是最优）',
        'if x <= 1': lambda S, B, r: (f'`x = {S.x} ≤ 1`：剩 0 个要 0 天、剩 1 个要 1 天 → 答案 `{S.dx} + {S.x} = {S.dx + S.x}`' if S.x <= 1
                                     else f'`x = {S.x} > 1`，还要继续拆'),
        'return dx + x': '答案 = `dx + x` = =={dx + x}== 天',
        'if dx > dis[x]': lambda S, B, r: (f'`{S.dx}` > `dis[{S.x}] = {S.dis[S.x]}`：这是旧的、更差的记录，==跳过==' if S.dx > S.dis[S.x]
                                          else f'`{S.dx}` 不比 `dis[{S.x}]` 差，是有效状态，往下展开'),
        'while True': '不断取出当前最优的状态',
        'for d in 2, 3': '枚举除数 `d`：2 或 3（循环结束则回到取堆顶）',
        'y = x // d': '先减 `x % {d} = {x % d}` 次 1 变成 {d} 的倍数，再除以 {d}：`y = {x} // {d} = {y}`',
        'dy = dx + x % d + 1': '花费 `{x % d}`（减 1）+ 1（除法）天：`dy = {dx} + {x % d} + 1 = {dy}`',
        'if dy < dis[y]': lambda S, B, r: (f'`dy = {S.dy}` 比已知的 `dis[{S.y}]` 更小 → 松弛' if S.dy < S.dis[S.y]
                                          else f'`dy = {S.dy}` 不比 `dis[{S.y}]` 好，放弃'),
        'dis[y] = dy': '更新 `dis[{y}] = {dy}`',
        'heappush(h, (dy, y))': '把 `({dy}, {y})` 放进堆，之后再展开',
    },
    cards=dict(
        one_liner='把 n 变成 0 当最短路：只在凑整除时才减 1',
        complexity='时间 `O(log²n · loglog n)`，空间 `O(log²n)`',
        problem=['每天三选一：吃 1 个；`n` 被 2 整除吃 `n/2` 个；被 3 整除吃 `2n/3` 个',
                 '求吃光 `n` 个橘子的最少天数，`n` 最大 `2×10^9`',
                 '示例：`10` → `4`；本视频：`10` → `4`'],
        quote='这样建图：x 到 x//2 连一条边权为 x mod 2 + 1 的边；x 到 x//3 连一条边权为 x mod 3 + 1 的边；1 到 0 连一条边权为 1 的边。答案为 n 到 0 的最短路。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['引理：最优解里不会出现「减 1，减 1，再除以 2」，所以减 1 只用来凑整除',
              '于是 `x` 只会走到 `x//2` 或 `x//3`，边权 = `x % d` 次减 1 + 1 次除法',
              '状态只有 `O(log²n)` 个，用 Dijkstra 求 `n` 到 0 的最短路，无需真的建图'],
        after=[dict(heading='另一种写法', lines=['方法一：记忆化搜索 `dfs(i) = min(dfs(i//2) + i%2, dfs(i//3) + i%3) + 1`',
                                              '边界 `dfs(0)=0, dfs(1)=1`，Python 用 `@cache`'])],
        summary=['状态 `n // (2^x·3^y)` 只有 `O(log²n)` 个，所以 n 再大也能跑',
                 '`x <= 1` 直接返回 `dx + x`，不用把 0 也入堆',
                 '`dx > dis[x]` 要跳过，否则会重复展开旧状态',
                 '不能直接 O(n) 递推：`n` 可达 2×10^9'],
    ),
)
