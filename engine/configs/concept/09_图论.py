def _cell_state(S):
    i, j, g = S['i'], S['j'], S['grid']
    if not (0 <= i < len(g) and 0 <= j < len(g[0])):
        return 'out'
    return g[i][j]


def _formula(S):
    if 'grid' not in S or 'i' not in S or 'j' not in S:
        return '网格 DFS：==访问过就插旗==，一个入口插满一个岛'
    st = _cell_state(S)
    pos = f"`({S['i']}, {S['j']})`"
    msg = {'out': '出界', '0': '是水', '2': '已插旗', '1': '未发现的陆地'}[st]
    return f"当前格子 {pos}：{msg}　|　已发现岛屿 `ans = {S.get('ans', 0)}`"


def _if_cap(S, B, ret):
    st = _cell_state(B)
    pos = f'`({B.i}, {B.j})`'
    if st == 'out':
        return f'{pos} 出界 → 递归边界，直接返回'
    if st == '0':
        return f'{pos} 是水 → 直接返回'
    if st == '2':
        return f'{pos} 已经插过旗 → 返回，==不重复访问=='
    return f'{pos} 是未发现的陆地，继续'


_dir = {'j - 1': ('左', 0, -1), 'j + 1': ('右', 0, 1), 'i - 1': ('上', -1, 0), 'i + 1': ('下', 1, 0)}


def _go(key):
    name, di, dj = _dir[key]
    return lambda S, B, ret: f'往{name}走：`({B.i}, {B.j})` → `({B.i + di}, {B.j + dj})`'


CONFIG = dict(
    num=None, title='图论 · 通用思想与模板', author='概念讲解', category='图论',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def num_islands(grid):               # 200. 岛屿数量（网格 DFS）
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        # 出界，或者不是 '1'，就不再往下递归
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '2'             # 插旗！避免来回横跳
        dfs(i, j - 1)                # 往左走
        dfs(i, j + 1)                # 往右走
        dfs(i - 1, j)                # 往上走
        dfs(i + 1, j)                # 往下走
    ans = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == '1':             # 找到了一个新的岛
                dfs(i, j)            # 把这个岛插满旗子
                ans += 1
    return ans
''',
    call="num_islands([['1', '1', '0'], ['0', '0', '1']])",
    expect=2,
    skip=['            return'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='grid', label='grid（蓝 = 陆地，绿 = 已插旗，黄框 = 当前格子）', cell=120,
             color=lambda S, i, j, v: {'1': 'blue', '2': 'green'}.get(v),
             cursors=[('i', 'j', 'yellow')], h=330),
        dict(type='calls', label='递归调用栈', h=230),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'm, n = len': "网格 `{m} × {n}`：`'1'` 是陆地，`'0'` 是水",
        'ans = 0': '`ans` 统计岛屿个数；接下来 ==逐格扫描==，找还没插旗的陆地',
        'for i, row': lambda S, B, ret: (f'扫描第 `{S.i}` 行' if B.get('i') != S.i or 'row' not in B
                                         else '所有格子都扫描完了'),
        'for j, c': lambda S, B, ret: (f"看格子 `({S.i}, {S.j})` = `'{S.c}'`" if (B.get('j'), B.get('i')) != (S.j, S.i)
                                       or 'c' not in B else f'第 `{S.i}` 行扫完'),
        "if c == '1'": lambda S, B, ret: ("是 `'1'`：==发现一个新岛==！从这里登陆" if S.c == '1' else
                                          ("是水，跳过" if S.c == '0' else "已插旗（属于之前的岛），跳过")),
        'dfs(i, j)  ': '登陆 `({i}, {j})`，DFS 把整个岛插满旗',
        'ans += 1': '这个岛插满旗了，`ans = {ans}`——之后再遇到 `1` 一定是 ==新的岛==',
        'if i < 0': _if_cap,
        "grid[i][j] = '2'": lambda S, B, ret: (f"插旗：`({S.i}, {S.j})` 改成 `'2'`——==先插旗再递归==，否则会来回横跳"
                                               if (S.i, S.j) == (0, 0) else f"插旗：`({S.i}, {S.j})` 改成 `'2'`"),
        'dfs(i, j - 1)': _go('j - 1'),
        'dfs(i, j + 1)': _go('j + 1'),
        'dfs(i - 1, j)': _go('i - 1'),
        'dfs(i + 1, j)': _go('i + 1'),
        'return ans': '共 `{ret}` 个岛屿：每个格子最多插旗一次，时间 `O(mn)`',
    },
    cards=dict(
        one_liner='网格就是图：从入口出发向四个方向扩散，访问过就插旗',
        complexity='时间 `O(mn)`（一般图 `O(V + E)`），空间 `O(mn)`',
        problem_heading='什么时候用？',
        problem=['网格里的连通块：岛屿个数、面积、染色 → DFS / BFS 插旗',
                 '最少几步、同时扩散（腐烂橘子）→ BFS 一层一层（多源）',
                 '先修关系、依赖、判断有没有环 → 拓扑排序 / 三色标记',
                 '前缀匹配、单词查找 → Trie（字典树）'],
        before=[dict(heading='核心概念：访问过就插旗', lines=[
            '网格 = 图：每个格子是点，上下左右相邻就连一条边',
            'DFS 三要素：入口（新发现的 `1`）、方向（4 个邻居）、边界',
            '边界：出界 / 是水 / ==已插旗==；先判出界再访问 `grid[i][j]`',
            'BFS 按层扩散：队列里同一批 = 同一时刻，适合求「最少几步」']),
        ],
        idea_heading='两位作者怎么说',
        quote='DFS 的过程中，最重要的是==不能重复访问之前访问过的格子==……怎么避免重复访问？本题的做法是把访问过的格子都插上旗子。',
        quote_src='—— 灵茶山艾府 · 200. 岛屿数量',
        idea=['灵神把网格 DFS 和二叉树对照：入口、方向、边界三件事一一对应',
              'yiduobo 200 叫它 ==种子染色法==：每发现一个岛换一种颜色，最后数颜色',
              '207：灵神用 DFS ==三色标记== 判环，yiduobo 用 BFS ==拓扑排序==（入度）'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`200` 岛屿数量：扫描 + DFS 插旗，数登陆次数',
                 '`994` 腐烂的橘子：多源 BFS，一层 = 一分钟',
                 '`207` 课程表：拓扑排序（入度为 0 入队）/ DFS 三色判环',
                 '`208` 实现 Trie：每个节点一个孩子表 + 单词结尾标记',
                 '易错：插旗要在递归之前；先判出界再读 `grid[i][j]`'],
    ),
)
