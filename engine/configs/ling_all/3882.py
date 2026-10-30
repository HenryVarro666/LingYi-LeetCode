G = [[1, 2, 3], [3, 1, 2]]


def _cell(S, i, j, v):
    I = S['_inner']
    ci, cj = I.get('i'), I.get('j')
    if ci is not None and cj is not None and (ci, cj) == (i, j) and 0 <= ci and 0 <= cj:
        return 'yellow'
    vis = S.get('vis') or ()
    if any(a == i and b == j for a, b, _ in vis):
        return 'green' if (i, j) == (0, 0) and S.get('ans', 99) != float('inf') else 'blue'
    return None


def _formula(S):
    I = S['_inner']
    if 'xor' not in I:
        return '从终点倒着走（向上/向左），把路上的格子值异或起来'
    i, j = I['i'], I['j']
    if i < 0 or j < 0:
        return f'`({i},{j})` 出界，这条分支不用继续'
    x = S['grid'][i][j]
    if S['_line'] >= 12:
        return f"`({i},{j})` 的值 `{x}` 已异或进来，`xor` = =={I['xor']}=="
    return f"带着 `xor = {I['xor']}` 来到 `({i},{j})`，格子值 `{x}`"


CONFIG = dict(
    num=3882, title='网格图中最小异或路径', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 DFS + 状态去重',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1771'],
    code='''
class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        vis = set()
        ans = inf

        def dfs(i: int, j: int, xor: int) -> None:
            nonlocal ans
            # 最优性剪枝：如果答案已经最小（等于 0），那么不再搜索
            if ans == 0 or i < 0 or j < 0 or (i, j, xor) in vis:
                return
            vis.add((i, j, xor))
            xor ^= grid[i][j]
            if i == 0 and j == 0:
                ans = min(ans, xor)
                return
            dfs(i - 1, j, xor)
            dfs(i, j - 1, xor)

        dfs(len(grid) - 1, len(grid[0]) - 1, 0)
        return ans
''',
    call=f'Solution().minCost({G})',
    expect=0,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格，蓝 = 已访问过的状态所在格，绿 = 起点已到达）', cell=84, h=250,
             color=_cell, cursors=[(lambda S: S['_inner'].get('i'), lambda S: S['_inner'].get('j'), 'yellow')]),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='calls', h=210),
        dict(type='set', var='vis', label='vis：访问过的状态 (i, j, xor)', fmt=lambda x: f'{x[0]},{x[1]},{x[2]}', h=170),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('j', "_inner.get('j')", 'pink'), ('xor', "_inner.get('xor')", 'purple'),
           ('ans', 'ans', 'green')],
    captions={
        'vis = set()': '`vis` 记录访问过的状态 `(i, j, xor)`：位置相同、异或和也相同才算重复',
        'ans = inf': '`ans = inf`：还没走到过起点',
        'if ans == 0 or': lambda S, B, r: (
            '`ans = 0`：答案已经不可能更小 → ==最优性剪枝==，直接返回' if S['ans'] == 0 else
            f"`({S['i']},{S['j']})` 出界 → 返回" if S['i'] < 0 or S['j'] < 0 else
            f"状态 `({S['i']},{S['j']},{S['xor']})` ==已经搜过== → 返回，避免重复" if (S['i'], S['j'], S['xor']) in S['vis'] else
            f"`({S['i']},{S['j']})` 带着 `xor = {S['xor']}` 第一次来 → 继续搜"),
        'vis.add': '记下状态 `({i},{j},{xor})`',
        'xor ^= grid[i][j]': '把格子值异或进来：`{B.xor} ^ {grid[i][j]}` = =={xor}==',
        'if i == 0 and j == 0': lambda S, B, r: ('走到起点 `(0,0)`：这是一条完整路径' if S['i'] == 0 and S['j'] == 0
                                                 else f"`({S['i']},{S['j']})` 还不是起点 → 继续往上、往左"),
        'ans = min': '整条路径异或值是 `{xor}`：`ans = min({B.ans}, {xor})` = =={ans}==',
        'dfs(i - 1, j, xor)': '先往上走一格，进入 `({i},{j})`，带着 `xor = {xor}`',
        'dfs(i, j - 1, xor)': '再往左走一格，进入 `({i},{j})`，带着 `xor = {xor}`',
        'dfs(len(grid) - 1': '从终点 `({i},{j})` 倒着搜，初始 `xor = 0`',
        'return ans': '最小异或值 `{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='异或不能只留最小值，所以带着 xor 搜，并给状态去重',
        complexity='时间 `O(mnU)`，空间 `O(mnU)`',
        problem=['`m × n` 的网格，从左上角走到右下角，只能向右或向下',
                 '路径代价 = 路上所有格子值的==按位异或==，求最小代价',
                 '示例：`[[1,2],[3,4]]` → `6`；本视频：`[[1,2,3],[3,1,2]]` → `0`'],
        quote='写一个网格图 DFS，除了有参数 (i,j) 表示当前位置外，还需要参数 xor 表示走过的格子的异或和。……为避免重复访问相同的状态，用 vis 数组（哈希集合）标记访问过的状态 (i,j,xor)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`xor` 是 DFS 的第三个参数：每进一个格子就异或进去',
              '同一个格子 `xor` 相同 → 后面的搜索完全一样，用 `vis` 去重',
              '`ans == 0` 已经是理论最小，直接剪枝不再搜'],
        summary=['时间/空间 `O(mnU)`，`U = max(grid)`，题目保证 `mn ≤ 1000`',
                 '易错：状态要带上 `xor`，只记录 `(i,j)` 会漏掉别的异或值',
                 '灵神提到：改成上下左右四个方向，同样的写法也能做',
                 '这里从终点倒着搜，到起点时才更新答案'],
    ),
)
