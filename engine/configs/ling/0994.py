ORANGE = {1: 'orange', 2: 'red'}


def _init(S, B, ret):
    i, j, x = S.i, S.j, S.x
    if x == 1:
        return f'`({i},{j})` 是新鲜橘子 → 计数'
    if x == 2:
        return f'`({i},{j})` 不是新鲜橘子，而是==一开始就烂的橘子=='
    return f'`({i},{j})` 是空格子，跳过'


def _nb(S, B, ret):
    i, j = S.i, S.j
    if not (0 <= i < S.m and 0 <= j < S.n):
        return f'`({S.x},{S.y})` 的邻居 `({i},{j})` ==出界=='
    v = B.grid[i][j]
    if v == 1:
        return f'`({S.x},{S.y})` 的邻居 `({i},{j})` 是==新鲜橘子== → 这一分钟被传染'
    if v == 2:
        return f'`({S.x},{S.y})` 的邻居 `({i},{j})` 已经烂了 → ==不会重复入队=='
    return f'`({S.x},{S.y})` 的邻居 `({i},{j})` 是空格子'


def _while(S, B, ret):
    q, fresh = B.q, B.fresh
    if q and fresh:
        return f'还有 `{fresh}` 个新鲜橘子，且有 `{len(q)}` 个烂橘子能传染 → 再过一分钟'
    if not fresh:
        return '`fresh = 0`：==新鲜橘子全烂了==，退出循环（不判断 fresh 会多算一分钟）'
    return '`q` 空了：烂橘子再也传染不到别人，退出循环'


CONFIG = dict(
    num=994, title='腐烂的橘子', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='多源 BFS · 按分钟分层',
    code='''
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        fresh = 0
        q = []
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    fresh += 1  # 统计新鲜橘子个数
                elif x == 2:
                    q.append((i, j))  # 一开始就腐烂的橘子

        ans = 0
        while q and fresh:
            ans += 1  # 经过一分钟
            tmp = q
            q = []
            for x, y in tmp:  # 已经腐烂的橘子
                for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):  # 四方向
                    if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:  # 新鲜橘子
                        fresh -= 1
                        grid[i][j] = 2  # 变成腐烂橘子
                        q.append((i, j))

        return -1 if fresh else ans
''',
    call='Solution().orangesRotting([[2, 1, 1, 0], [0, 1, 1, 2]])',
    expect=2,
    skip=['for j, x in enumerate(row)', 'elif x == 2', 'for i, j in (x - 1', 'fresh -= 1', 'fresh = 0'],
    views=[
        dict(type='text', fn=lambda S: f"第 =={S['ans']}== 分钟　橙 = 新鲜 `1`　红 = 腐烂 `2`" if 'ans' in S
             else '橙 = 新鲜橘子 `1`　红 = 腐烂橘子 `2`', size=26),
        dict(type='grid', var='grid', cell=100, h=330,
             cursors=[('x', 'y', 'blue', '传染源'), ('i', 'j', 'yellow', '邻居')],
             color=lambda S, i, j, v: ORANGE.get(v)),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['tmp']], label='tmp（上一分钟烂掉的橘子，蓝 = 正在传染）',
             color=lambda S, i, v: 'blue' if S['tmp'][i] == (S['x'], S['y']) else None, index=False),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']], label='q（这一分钟新烂的橘子 = 下一层）', index=False),
    ],
    watch=[('ans', 'ans', 'green'), ('fresh', 'fresh', 'orange')],
    captions={
        'm, n = len': '网格 `{m}` 行 `{n}` 列；`fresh = 0` 用来数新鲜橘子',
        5: '`q = []`：等会儿用来放==一开始就烂的橘子==',
        'for i, row': lambda S, B, ret: f'扫描第 `{S.i}` 行' if B.get('i') != S.i or 'i' not in B else '扫描完毕',
        'if x == 1': _init,
        'fresh += 1': '统计新鲜橘子个数：`fresh` = {fresh}',
        'q.append((i, j))  # 一开始': '一开始就腐烂的橘子 `({i},{j})` 加入 `q`：==所有烂橘子同时作为起点==（多源）',
        'ans = 0': '初始化 `q = {q}`，`fresh = {fresh}`，`ans = 0` 分钟',
        'while q and fresh': _while,
        'ans += 1': '经过一分钟：`ans` = =={ans}==',
        'tmp = q': '`tmp` = 上一分钟烂掉的橘子 `{tmp}`，它们这一分钟去传染邻居',
        'q = []': '`q` 清空，用来装==这一分钟新烂的橘子==（下一层）',
        'for x, y in tmp': lambda S, B, ret: (f'取出烂橘子 `({S.x},{S.y})`，看它四方向的邻居'
                                              if (B.get('x'), B.get('y')) != (S.x, S.y) or 'x' not in B
                                              else '`tmp` 里的橘子都传染过了，这一分钟结束'),
        'if 0 <= i < m': _nb,
        'grid[i][j] = 2': '`fresh` 减到 {fresh}；`({i},{j})` 变成烂橘子，==改成 2 保证它只入队一次==',
        '                        q.append((i, j))': '`({i},{j})` 加入 `q`，下一分钟由它去传染别人',
        'return -1 if fresh': lambda S, B, ret: ('`fresh = 0`：全烂了，返回分钟数 ==' + str(ret) + '==') if ret != -1
        else f'还剩 `{S.fresh}` 个新鲜橘子永远烂不掉 → 返回 ==-1==',
    },
    max_steps=70,
    cards=dict(
        one_liner='所有烂橘子同时出发，一分钟扩散一层，层数就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`0` 空格子，`1` 新鲜橘子，`2` 烂橘子；每分钟烂橘子会传染上下左右的新鲜橘子',
                 '求所有橘子都烂掉的最少分钟数；不可能则返回 `-1`',
                 '本视频示例：`[[2,1,1,0],[0,1,1,2]]` → ==2=='],
        quote='在 BFS 中要将 grid[i][j]=1 的橘子修改成 2，这可以保证每个橘子加入 q 中至多一次。如果不修改……程序就会陷入死循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把==所有==烂橘子放进 `q`，同时作为 BFS 起点（多源 BFS）',
              '每轮：`ans += 1`，用上一层 `tmp` 传染出新的一层 `q`',
              '用 `fresh` 计数：最后 `fresh > 0` 说明有橘子永远烂不掉 → `-1`'],
        summary=['时间 `O(mn)`：每个橘子最多入队一次',
                 '==循环条件必须带上 fresh==：否则全烂之后还会多转一圈，`ans` 多 1',
                 '传染时立刻把 `grid[i][j]` 改成 2，避免重复入队、死循环',
                 '`tmp = q; q = []` 是“按层 BFS”的写法，层号就是分钟数'],
    ),
)
