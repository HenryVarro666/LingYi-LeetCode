G = [[3, 1, 1], [2, 5, 1], [1, 5, 5]]
N = 3


def _st(k):
    return f'({k // N},{k % N})'


def _cmp(S, B, r):
    new = S.f[S.state] + S.grid[S.i][S.next_j] + S.grid[S.i][S.next_k]
    head = f'机器人 1 → 列 `{S.next_j}`，机器人 2 → 列 `{S.next_k}`（`{S.next_j} < {S.next_k}` 不交叉）：候选 `{S.f[S.state]} + {S.grid[S.i][S.next_j]} + {S.grid[S.i][S.next_k]} = {new}`'
    if S.next_state not in S.g:
        return head + '，`g` 里还没有这个状态 → ==记下=='
    old = S.g[S.next_state]
    if old < new:
        return head + f'，比 `g` 里的 `{old}` 大 → ==更新=='
    return head + f'，不比 `g` 里的 `{old}` 大 → ==不更新=='


def _gc(S, r, c, v):
    if 'next_j' in S and S.get('_line') in (14, 15, 16, 17, 18, 19):
        if (r, c) == (S['i'], S['next_j']):
            return 'blue'
        if (r, c) == (S['i'], S['next_k']):
            return 'pink'
    return None


CONFIG = dict(
    num=1463, title='摘樱桃 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='两机器人状态压缩成 j*n+k · 字典滚动 DP',
    tags=['灵神题单', '网格图 DP'],
    code='''
class Solution(object):
    def cherryPickup(self, grid):

        m = len(grid)
        n = len(grid[0])
        f = {}
        f[n - 1] = grid[0][0] + grid[0][-1]
        for i in range(1, m):
            g = {}
            for state in f:
                j = state // n
                k = state % n
                for next_j in range(j - 1, j + 2):
                    if next_j >= 0 and next_j < n - 1:
                        for next_k in range(k - 1, k + 2):
                            if next_k < n and next_k > next_j:
                                next_state = next_j * n + next_k
                                if next_state not in g or g[next_state] < f[state] + grid[i][next_j] + grid[i][next_k]:
                                    g[next_state] = f[state] + grid[i][next_j] + grid[i][next_k]
            
            f = g
        
        return max(g.values())
''',
    call=f'Solution().cherryPickup({G})',
    expect=21,
    skip=['for next_j', 'if next_j >=', 'for next_k', 'if next_k <', 'next_state = next_j'],
    views=[
        dict(type='grid', var='grid', label='grid（框 = 两个机器人上一行的位置，实心 = 这一步要走到的格）', cell=64, h=260, color=_gc,
             cursors=[('i - 1', 'j', 'blue', ''), ('i - 1', 'k', 'pink', '')]),
        dict(type='map', var=lambda S: S.get('g'), fmt=lambda k, v: f'{_st(k)} → {v}', label='g：这一行的状态（key = j*n+k，显示成 (j,k)）', h=180),
        dict(type='map', var=lambda S: S.get('f'), fmt=lambda k, v: f'{_st(k)} → {v}', label='f：上一行的状态', h=180),
    ],
    watch=[('i', 'i'), ('j', 'j', 'blue'), ('k', 'k', 'pink')],
    captions={
        'm = len(grid)': '`m` 行 `n` 列：`m = {m}`',
        'n = len(grid[0])': '`n = {n}`',
        'f = {}': '`f` 是字典：key = `j * n + k`（机器人 1 在第 j 列、机器人 2 在第 k 列，同一行），value = 最多樱桃',
        'f[n - 1] =': '起点：机器人 1 在第 0 列、机器人 2 在第 `{n-1}` 列 → `f[{n-1}] = {f[n-1]}`（两格樱桃都拿）',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行：由上一行 `f` 推出这一行的 `g`' if S.i != B.get('i') else '所有行推完，答案是最后一行 `g` 里的最大值'),
        'g = {}': '`g` 收集这一行能到的状态',
        'for state in f': lambda S, B, r: (f'取上一行的一个状态 `state = {S.state}`' if S.get('state') != B.get('state') else '上一行的状态都处理完了'),
        'j = state': '拆出机器人 1 的列：`j = state // n = {j}`',
        'k = state': '拆出机器人 2 的列：`k = state % n = {k}`，各自可以走到 `±1` 列',
        'if next_state not in g': _cmp,
        'g[next_state] =': lambda S, B, r: f'`g[{_st(S.next_state)}]` 更新为 =={S.g[S.next_state]}==（取较大者）',
        'f = g': '这一行结束：`f = g`，下一行从这些状态出发（滚动数组）',
        'return max': '最后一行所有状态里取最大：`{ret}`',
    },
    cards=dict(
        one_liner='两个机器人同步下行，只记 (j, k)，且保证 j < k',
        complexity='时间 `O(mn^2)`，空间 `O(n^2)`',
        problem=['`grid` 每格是樱桃数，机器人 1 从 `(0,0)`、机器人 2 从 `(0,cols-1)` 出发',
                 '每步下一行，列 `-1/0/+1`；同格只摘一次',
                 '本视频：`[[3,1,1],[2,5,1],[1,5,5]]`'],
        quote='由于地图中不存在负数，那么可以证明最终答案中两个机器人的路线是不相交的，于是此时只需要考虑j < k的这些状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j][k]`：到第 `i` 行，机器人 1 在 `j`、机器人 2 在 `k` 的最大樱桃',
              '路线不会交叉 → 只留 `j < k`，同格重复的情况根本不存在',
              '每行只依赖上一行：用字典 `f`、`g` 滚动，key 压成 `j*n+k`'],
        summary=['时间 `O(mn^2)`，空间 `O(n^2)`',
                 '易错：`next_j < n - 1`、`next_k > next_j`，保证 `j < k` 且在界内',
                 '原文为 Python 2 写法，`state / n` 是整数除法，已改为 `state // n`',
                 '对比灵神：灵神用三维数组 + 下标 +1 哨兵；yiduobo 用字典只存可达状态'],
    ),
)
