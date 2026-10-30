EDGES = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
TH = 4
N = 4


def _color(S, i, j, v):
    line = S.get('_line', 0)
    if line == 16:
        k = S.get('k')
        if (i == S.get('i') and j == k) or (i == k and j == S.get('j')):
            return 'blue'
        return None
    if line >= 27 and 'cnt' in S:
        if i == S.get('i') and j != i and v is not None and v <= TH:
            return 'green'
    return None


def _counts(S):
    if 'min_cnt' not in S:
        return f'边：`0-1` 3，`1-2` 1，`1-3` 4，`2-3` 1；`distanceThreshold = {TH}`'
    f = S['f']
    cur = S.get('i')
    parts = []
    for a in range(N):
        c = sum(1 for b in range(N) if b != a and f[a][b] <= TH)
        if cur is not None and (a < cur or (a == cur and S.get('_line', 0) >= 29)):
            parts.append(f'城市{a}: =={c}==')
        else:
            parts.append(f'城市{a}: ?')
    return f'`min_cnt` 从 `n={N}` 起；阈值内邻居数  ' + '    '.join(parts)


CONFIG = dict(
    num=1334, title='阈值距离内邻居最少的城市', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Floyd 两两距离 + 统计阈值内城市数',
    tags=['灵神题单·图论算法', '难度分 1855'],
    code='''
class Solution(object):
    def findTheCity(self, n, edges, distanceThreshold):

        f = [[None] * n for _ in range(n)]
        for index in range(n):
            f[index][index] = 0
        for x, y, dis in edges:
            f[x][y] = dis
            f[y][x] = dis
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if f[i][k] is not None and f[k][j] is not None:
                        if f[i][j] is None or f[i][j] > f[i][k] + f[k][j]:
                            f[i][j] = f[i][k] + f[k][j]
        
        min_cnt = n
        res = None
        for i in range(n):
            cnt = 0
            for j in range(n):
                if i == j:
                    continue
                if f[i][j] > distanceThreshold:
                    continue
                cnt += 1
            
            if cnt <= min_cnt:
                min_cnt = cnt
                res = i
        
        return res
''',
    call=f'Solution().findTheCity({N}, {EDGES}, {TH})',
    expect=3,
    skip=['for index in range(n)', 'f[index][index] = 0', 'for x, y, dis in edges', 'f[x][y] = dis', 'f[y][x] = dis',
          'for i in range(n)', 'for j in range(n)', 'if f[i][k] is not None', 'if f[i][j] is None or', 'cnt = 0',
          'if i == j', 'continue', 'if f[i][j] > distanceThreshold', 'min_cnt = n', 'res = None'],
    views=[
        dict(type='text', fn=_counts, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]：i 到 j 的距离（· = None = 还不知道；蓝 = 经过 k 的两段，绿 = 阈值内）', h=420, cell=84,
             rows=lambda S: list(range(N)), cols=lambda S: list(range(N)), color=_color,
             cursors=[(lambda S: S.get('i') if S.get('_line', 0) == 16 or S.get('_line', 0) >= 27 else None, lambda S: S.get('j'), 'yellow')]),
    ],
    watch=[('k', 'k', 'blue'), ('i', 'i', 'cyan'), ('cnt', 'cnt', 'green'), ('min_cnt', 'min_cnt', 'orange'), ('res', 'res', 'pink')],
    captions={
        'f = [[None]': '`f[i][j]`：城市 i 到 j 的距离，`None` 表示暂时不知道；先全设成 `None`',
        'for k in range': lambda S, B, r: (f'`k = {S.k}`：试试把城市 `{S.k}` 当中转，更新所有 `f[i][j]`' if 'k' not in B or S.get('k') != B.get('k')
                                           else '三重循环结束：`f` 已是任意两城市的最短距离'),
        'f[i][j] = f[i][k] + f[k][j]': lambda S, B, r: (f'`k = {S.k}`：`f[{S.i}][{S.k}] + f[{S.k}][{S.j}]` = `{S.f[S.i][S.k]} + {S.f[S.k][S.j]}` '
                                                       f'→ 更短（或原来是 `None`），`f[{S.i}][{S.j}]` 变成 =={S.f[S.i][S.j]}=='),
        'cnt += 1': '`f[{i}][{j}] = {f[i][j]} <= {distanceThreshold}`：城市 `{j}` 在阈值内 → `cnt` = {cnt}',
        'if cnt <= min_cnt': lambda S, B, r: (f'城市 `{S.i}` 阈值内有 `{S.cnt}` 个；`{S.cnt} <= min_cnt = {S.min_cnt}` → '
                                              + ('==成立==，更新答案' if S.cnt <= S.min_cnt else '不成立，保持')),
        'min_cnt = cnt': lambda S, B, r: (f'`min_cnt` = {S.cnt}' + ('（和之前相等：==用 `<=`，同样少时取编号更大的==）' if B.get('min_cnt') == S.cnt else '')),
        'res = i': '`res = {i}`：当前最优城市',
        'return res': '邻居最少、并列取编号最大的城市是 =={ret}==',
    },
    cards=dict(
        one_liner='先求出城市两两之间的距离，再逐个城市数阈值内的邻居',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['`n` 个城市，双向带权边，给定距离阈值 `distanceThreshold`',
                 '数每个城市在阈值内能到的城市个数，返回个数最少的城市；并列取编号最大',
                 '本视频：`n=4`，阈值 `4` → `3`'],
        quote='需要知道对于每一个城市而言，与其距离小于等于threshold的城市的数目，因此我们需要首先知道每个城市两两之间的距离，那么可以先使用经典的弗洛伊德算法求解出城市两两之间的距离。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 是 i 到 j 的当前最短距离；`None` 代表还没有路',
              '外层 `k` 是中转点：`f[i][k]`、`f[k][j]` 都有值，且更短才更新',
              '对角线先设成 `0`，所以 `f[i][i]` 不会被「往返」改坏',
              '最后每个城市数一遍阈值内的邻居；`<=` 保证并列时取更大的编号',
              '视频里只保留发生更新的那几步，其余判断折叠了'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '外层 `k` 必须是最外层循环',
                 '`cnt <= min_cnt`：并列时后面的（编号大的）覆盖前面的',
                 '`None` 与整数比较：Python 3 会报错；原文只在 `f[i][j]` 一定有值（图连通）时才比较。本例图是连通的，所以直接可用',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
