def _cell(S):
    i, j = S['i'], S['j']
    if i < 0 or i >= S['m'] or j < 0 or j >= S['n']:
        return f'`({i},{j})` ==出界== → 直接返回'
    v = S['grid'][i][j]
    if v == '0':
        return f'`({i},{j})` 是==水== → 直接返回'
    if v == '2':
        return f'`({i},{j})` ==已插旗==（来过了）→ 直接返回，不会来回横跳'
    return f'`({i},{j})` 是没插旗的陆地 → 条件不成立，继续往下：插旗 + 向四周扩散'


def _scan(S, B, ret):
    if 'i' not in B:
        return f'从第 `{S.i}` 行开始逐格扫描，寻找还没插旗的 `1`'
    if B.i == S.i:
        return '所有格子扫描完毕'
    return f'扫描第 `{S.i}` 行'


def _found(S, B, ret):
    c, i, j = S.c, S.i, S.j
    if c == '1':
        return f'`({i},{j})` 是 `1` 且没插旗 → ==发现了一个新的岛==！'
    if c == '2':
        return f'`({i},{j})` 已经插了旗 → 属于之前的岛，==不能重复计数==，跳过'
    return f'`({i},{j})` 是水，跳过'


def _step(name, di, dj):
    return lambda S, B, ret: f'{name}：从 `({B.i},{B.j})` 递归到 `dfs({B.i + di}, {B.j + dj})`'


CONFIG = dict(
    num=200, title='岛屿数量', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='网格图 DFS · 插旗标记',
    code='''
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(i: int, j: int) -> None:
            # 出界，或者不是 '1'，就不再往下递归
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
                return
            grid[i][j] = '2'  # 插旗！避免来回横跳无限递归
            dfs(i, j - 1)  # 往左走
            dfs(i, j + 1)  # 往右走
            dfs(i - 1, j)  # 往上走
            dfs(i + 1, j)  # 往下走

        ans = 0
        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                if c == '1':  # 找到了一个新的岛
                    dfs(i, j)  # 把这个岛插满旗子，这样后面遍历到的 '1' 一定是新的岛
                    ans += 1
        return ans
''',
    call='Solution().numIslands([list("1100"), list("0100"), list("0001")])',
    expect=2,
    skip=['                return', 'for j, c in enumerate(row)'],
    views=[
        dict(type='text', fn=lambda S: '蓝 = 陆地 `1`　绿 = 已插旗 `2`　黄框 = 当前格子 `(i,j)`', size=24),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], cell=96,
             color=lambda S, i, j, v: {'1': 'blue', '2': 'green'}.get(v), h=380),
        dict(type='calls', label='递归调用栈（dfs 深度）', h=230),
    ],
    watch=[('岛屿数 ans', 'ans', 'green'), ('当前格', lambda S: (S['i'], S['j']))],
    captions={
        'm, n = len': '网格 `{m}` 行 `{n}` 列；`1` 是陆地，`0` 是水',
        "grid[i][j] != '1'": lambda S, B, ret: _cell(S),
        "grid[i][j] = '2'": lambda S, B, ret: (f'插旗：`({S.i},{S.j})` 改成 `2`，==以后再走到这里会立刻返回==，不会无限递归'
                                            if sum(r.count('2') for r in S.grid) == 1 else f'插旗：`({S.i},{S.j})` 改成 `2`'),
        'dfs(i, j - 1)': _step('往左走', 0, -1),
        'dfs(i, j + 1)': _step('往右走', 0, 1),
        'dfs(i - 1, j)': _step('往上走', -1, 0),
        'dfs(i + 1, j)': _step('往下走', 1, 0),
        'ans = 0': '`ans = 0`：还没发现任何岛',
        'for i, row': _scan,
        "if c == '1'": _found,
        'dfs(i, j)': '从 `({i},{j})` 登陆，DFS 把==整座岛插满旗子==',
        'ans += 1': '这座岛插满旗了 → 岛屿数 `ans` = =={ans}==；后面再遇到 `1` 一定是新岛',
        'return ans': '扫描结束，返回岛屿数 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='遇到没插旗的 1 就是新岛：DFS 把整座岛插满旗子',
        complexity='时间 `O(mn)`，空间 `O(mn)`（递归栈）',
        problem=['网格里 `1` 是陆地、`0` 是水，上下左右相连的陆地组成一座岛',
                 '求岛屿数量（斜着不算相连）',
                 '本视频示例：`["1100","0100","0001"]` → ==2== 座岛'],
        quote='假设你是哥伦布。先从左上角开始，把第一个岛全部插上旗子……插满旗子后，把答案加一。找到 1 意味着发现了一个新的岛。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 从 `(i,j)` 往==左右上下==四个方向走，遇到==出界、水、旗子==就返回',
              '==最重要的是不能重复访问==：插旗 `grid[i][j] = \'2\'` 就是“访问过”的标记',
              '插满旗后，后面扫到的 `1` 一定属于==新的岛==，所以 `ans += 1`'],
        summary=['时间 `O(mn)`：每个格子最多插一次旗；空间 `O(mn)`：蛇形岛递归很深',
                 '==先判断出界，再读 grid[i][j]==，否则 `i = -1` 会越界',
                 '插旗必须写在递归==之前==；写在最后会在两格之间来回横跳、无限递归',
                 '不能只往右、往下走：蚊香形的岛需要四个方向',
                 '标记成 `0` 也行，只要不是 `1`'],
    ),
)
