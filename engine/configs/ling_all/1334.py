EDGES = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
TH = 4
N = 4


def _color(S, i, j, v):
    line = S.get('_line', 0)
    if line == 15:
        k = S.get('k')
        if (i == S.get('i') and j == k) or (i == k and j == S.get('j')):
            return 'blue'
        return None
    if line >= 22 and 'cnt' in S:
        if i == S.get('i') and j != i and v <= TH:
            return 'green'
    return None


def _counts(S):
    if 'min_cnt' not in S:
        return '边：`0-1` 3，`1-2` 1，`1-3` 4，`2-3` 1；阈值 `distanceThreshold = 4`'
    f = S['f']
    cur = S.get('i')
    parts = []
    for a in range(N):
        c = sum(1 for b in range(N) if b != a and f[a][b] <= TH)
        if cur is not None and a < cur or (a == cur and S.get('_line', 0) >= 24):
            parts.append(f'城市{a}: =={c}==')
        else:
            parts.append(f'城市{a}: ?')
    return '阈值内邻居数  ' + '    '.join(parts)


def _cap_upd(S, B, ret):
    i, j, k, s = S.i, S.j, S.k, S.s
    base = f'中转 `{k}`：`f[{i}][{k}] + f[{k}][{j}]` = `{S.f[i][k]} + {S.f[k][j]}` = {s} < 原值 → `f[{i}][{j}]` = =={s}=='
    if i == j:
        base += '（对角线变成往返长度，不影响答案：统计时跳过 `j == i`）'
    return base


def _cap_cmp(S, B, ret):
    ok = S.cnt <= S.min_cnt
    return (f'城市 `{S.i}` 阈值内有 `{S.cnt}` 个邻居；`{S.cnt} <= min_cnt = {S.min_cnt}` → '
            + ('==成立==，更新' if ok else '不成立，保持'))


def _cap_min(S, B, ret):
    if B.get('min_cnt') == S.cnt:
        return '==相等也更新==：邻居一样少时，保留编号更大的城市 → `min_cnt` 不变，`ans` 马上换成更大的 `i`'
    return '更少 → `min_cnt` 记为 `{}`'.format(S.cnt)


CONFIG = dict(
    num=1334, title='阈值距离内邻居最少的城市', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Floyd 全源最短路（空间优化）',
    tags=['灵神题单·图论算法', '难度分 1855'],
    code='''
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        w = [[inf] * n for _ in range(n)]
        for x, y, wt in edges:
            w[x][y] = w[y][x] = wt

        f = w
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # f[i][j] = min(f[i][j], f[i][k] + f[k][j])
                    # 手动 if 比大小更快
                    s = f[i][k] + f[k][j]
                    if s < f[i][j]:
                        f[i][j] = s

        ans = 0
        min_cnt = inf
        for i in range(n):
            cnt = 0
            for j in range(n):
                if j != i and f[i][j] <= distanceThreshold:
                    cnt += 1
            if cnt <= min_cnt:  # 相等时取最大的 i
                min_cnt = cnt
                ans = i
        return ans
''',
    call=f'Solution().findTheCity({N}, {EDGES}, {TH})',
    expect=3,
    skip=['for x, y, wt in edges', 'for i in range(n)', 'for j in range(n)', 's = f[i][k]', 'if s < f[i][j]', 'cnt = 0',
          'ans = 0', 'min_cnt = inf', 'if j != i and'],
    views=[
        dict(type='text', fn=_counts, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]：i 到 j 的最短路（∞ = 暂时没路；蓝 = 中转 k 的两段，绿 = 阈值内）', h=420, cell=84,
             rows=lambda S: list(range(N)), cols=lambda S: list(range(N)), color=_color,
             cursors=[(lambda S: S.get('i') if S.get('_line', 0) >= 15 else None, lambda S: S.get('j'), 'yellow')]),
    ],
    watch=[('k', 'k', 'blue'), ('i', 'i', 'cyan'), ('cnt', 'cnt', 'green'), ('min_cnt', 'min_cnt', 'orange'), ('ans', 'ans', 'pink')],
    captions={
        'w = [[inf]': '`w[i][j]` 是 i、j 之间的直接边权：先全设成 ∞（没有边）',
        'w[x][y] = w[y][x] = wt': '双向边：`w[x][y]` 和 `w[y][x]` 都写成边权 `{wt}`',
        'f = w': '`f = w`：`f[i][j]` 初始是直接边权，之后原地改成最短路',
        'for k in range': lambda S, B, r: (f'`k = {S.k}`：允许把城市 `{S.k}` 当中转点（中间点编号 <= {S.k}）' if S.get('k') != B.get('k') or 'k' not in B
                                           else '所有中转点都试过了：`f` 就是任意两城市的最短路'),
        'f[i][j] = s': _cap_upd,
        'if cnt <= min_cnt': _cap_cmp,
        'min_cnt = cnt': _cap_min,
        'ans = i': '`ans = {i}`：当前最优城市',
        'cnt += 1': '`f[{i}][{j}] = {f[i][j]} <= {distanceThreshold}`：城市 `{j}` 在阈值内 → `cnt` = {cnt}',
        'return ans': '邻居最少的城市里编号最大的是 =={ret}==',
    },
    cards=dict(
        one_liner='先 Floyd 求任意两城最短路，再数阈值内的邻居',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['`n` 个城市，双向带权边，给定距离阈值 `distanceThreshold`',
                 '数每个城市在阈值内能到的城市个数，返回个数最少的城市；并列取编号最大',
                 '本视频：`n=4`，阈值 `4` → `3`'],
        quote='定义 dfs(k,i,j) 表示从 i 到 j 的最短路长度，并且这条最短路的中间节点编号都 ≤ k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k` 是==最外层==：先把「中间点 ≤ k-1」的最短路算完，再考虑经过 `k` 与否',
              '选 `k`：`f[i][k] + f[k][j]`；不选：`f[i][j]`，取更小',
              '`i→k`、`k→j` 的最短路不会经过 `k` 本身，所以可以==去掉第一个维度，原地更新==',
              '视频里只展示发生更新的那几步，其余比较被折叠了'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`（递归/记忆化/递推版本空间是 `O(n^3)`）',
                 '循环顺序必须是 `k, i, j`，`k` 在最外层',
                 '`cnt <= min_cnt` 的等号：并列时取编号最大的城市',
                 '`j != i`：自己不算自己的邻居',
                 '灵神题解还讲了递归 → 记忆化 → 递推 → 空间优化的完整推导，本视频演示最终版'],
    ),
)
