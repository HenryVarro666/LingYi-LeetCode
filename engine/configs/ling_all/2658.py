G0 = [[2, 1, 0, 0], [4, 0, 0, 3], [0, 0, 3, 4]]


def _col(S, i, j, v):
    if '_inner' not in S:
        return None
    return 'green' if v == 0 and G0[i][j] > 0 else None


CONFIG = dict(
    num=2658, title='网格图中鱼的最大数目', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='DFS 求连通块元素和',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1490'],
    code='''
class Solution:
    def findMaxFish(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int) -> int:
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                return 0
            s = grid[i][j]
            grid[i][j] = 0  # 标记成访问过
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                s += dfs(x, y)  # 四方向移动
            return s
        return max(max(dfs(i, j) for j in range(n)) for i in range(m))
''',
    call=f'Solution().findMaxFish({G0})',
    expect=10,
    max_steps=84,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已访问并清零；黄框 = 当前格子）', cell=84, h=330,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='calls', h=250),
    ],
    watch=['i', 'j', ('s', 's', 'green')],
    captions={
        'if i < 0 or i >= m': lambda S, B, r: (
            f'`({S.i},{S.j})` 越界或是陆地 → 没有鱼，返回 ==0=='
            if not (0 <= S.i < S.m and 0 <= S.j < S.n) or B.grid[S.i][S.j] == 0
            else f'`({S.i},{S.j})` 是水域且没访问过，继续'),
        's = grid[i][j]': '先捞走这格的鱼：`s = {s}`',
        'grid[i][j] = 0': '把格子清零 = 标记访问过，之后再走到这里会当陆地返回 0，不会重复统计',
        'for x, y in': '向下、上、右、左四个方向各递归一次',
        's += dfs': '把这个方向连通块的鱼加进来：`s = {s}`',
        'return s': '四个方向都走完，这一块返回 `s` = =={s}==',
        'return max': lambda S, B, r: f'每个格子都当过起点，最大连通块的鱼数就是答案 =={r}==',
    },
    cards=dict(
        one_liner='最大的水域连通块里，所有鱼之和就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid[r][c] = 0` 是陆地，`> 0` 是水域，数值是鱼的条数',
                 '渔夫可从任一水域出发，捕鱼、走到相邻水域，不限次数',
                 '求最多能捞多少鱼；示例 `[[2,1,0,0],[4,0,0,3],[0,0,3,4]]` → `10`'],
        quote='DFS 统计每个包含正数的连通块的元素和，最大值即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['渔夫能走遍的就是一整个水域连通块，所以鱼数 = ==块内元素和==',
              '`dfs` 返回从 `(i,j)` 出发能到的所有格子的鱼数之和',
              '访问过的格子直接改成 `0`，不用额外的 vis 数组'],
        summary=['时间 `O(mn)`：每个格子最多被清零一次',
                 '空间 `O(mn)`：递归栈最坏是整块蛇形水域',
                 '易错：先清零再递归，否则相邻格子会来回无限递归',
                 '会修改输入 `grid`；不想改就另开 vis 数组'],
    ),
)
