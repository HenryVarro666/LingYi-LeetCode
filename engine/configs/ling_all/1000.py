def _cand(S):
    i, j, f, k = S['i'], S['j'], S['f'], S['k']
    return [(m, f[i][m] + f[m + 1][j]) for m in range(i, j, k - 1)]


def _active(S):
    return S.get('_line') in (10, 11, 12) and 'j' in S and 'i' in S and S['j'] > S['i']


def _color(S, r, c, v):
    if not _active(S):
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if S.get('_line') == 12:
        return None
    k = S['k']
    cand = [(m, S['f'][i][m] + S['f'][m + 1][j]) for m in range(i, j, k - 1)]
    best = min(cand, key=lambda t: t[1])[0]
    if (r, c) in ((i, best), (best + 1, j)):
        return 'green'
    if any((r, c) in ((i, m), (m + 1, j)) for m, _ in cand):
        return 'blue'
    return None


def _formula(S):
    if not _active(S):
        return '`f[i][j]` = 把 `stones[i..j]` 尽可能合并的最小成本；`i` 倒序、`j` 正序'
    i, j, k, s = S['i'], S['j'], S['k'], S['s']
    cand = _cand(S)
    best = min(x for _, x in cand)
    txt = '，'.join(f'm={m}: {x}' for m, x in cand)
    L = j - i + 1
    can = (j - i) % (k - 1) == 0
    tail = f'；长度 {L}，==能合并成一堆==，再加 `s[{j + 1}] − s[{i}]` = {s[j + 1] - s[i]}' if can else f'；长度 {L}，不能合成一堆，不加区间和'
    return f'分成 `[i..m]` + `[m+1..j]`，成本 `f[i][m] + f[m+1][j]`：{txt} → 最小 {best}{tail}'


CONFIG = dict(
    num=1000, title='合并石头的最低成本', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP（分出 1 堆 + p-1 堆）',
    tags=['灵神题单', '动态规划', '难度分 2423'],
    code='''
class Solution:
    def mergeStones(self, stones: List[int], k: int) -> int:
        n = len(stones)
        if (n - 1) % (k - 1):  # 无法合并成一堆
            return -1
        s = list(accumulate(stones, initial=0))  # 前缀和
        f = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                f[i][j] = min(f[i][m] + f[m + 1][j] for m in range(i, j, k - 1))
                if (j - i) % (k - 1) == 0:  # 可以合并成一堆
                    f[i][j] += s[j + 1] - s[i]
        return f[0][-1]
''',
    call='Solution().mergeStones([3,5,1,2,6], 3)',
    expect=25,
    skip=['for j in range'],
    views=[
        dict(type='array', var='stones', label='stones', h=215, cell=80, pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j')),
        dict(type='text', fn=_formula, size=22, h=110),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 候选，绿 = 最优的分割点 m）', h=330, cell=64,
             rows=lambda S: [str(k_) for k_ in range(len(S['stones']))], cols=lambda S: [str(k_) for k_ in range(len(S['stones']))],
             color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k'), ('s', 's')],
    captions={
        'n = len': '`n = {n}` 堆石头，每次合并 `k = {k}` 堆',
        'if (n - 1)': '每次合并堆数减少 `k − 1`，从 `n` 堆到 1 堆要减少 `n − 1`：`({n} − 1) % ({k} − 1) = {(n - 1) % (k - 1)}` → ==能合并==，不返回 -1',
        's = list': '前缀和 `s = {s}`：`s[j+1] − s[i]` 就是 `stones[i..j]` 的石头总数',
        'f = [[0]': '`f[i][j]`：尽可能合并 `stones[i..j]` 的最小成本；单堆 `f[i][i] = 0`',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：`f[i][j]` 要用 `f[m+1][j]`（m+1 > i）→ ==i 从大到小== 枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][j] = min': lambda S, B, r: (f'`j = {S.j}`：分出一个能合成 1 堆的 `[i..m]`（`m` 每次跳 `k−1`），剩下 `[m+1..j]`，取最小 → `f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'if (j - i)': lambda S, B, r: ((f'`({S.j} − {S.i}) % ({S.k} − 1) = 0`：这段 {S.j - S.i + 1} 堆最后能合成 1 堆 → ==要加上这次合并的成本==') if (S.j - S.i) % (S.k - 1) == 0
                                       else f'`({S.j} − {S.i}) % ({S.k} − 1) = {(S.j - S.i) % (S.k - 1)}`：这段合不成 1 堆，只是「尽量合并」，不加区间和'),
        'f[i][j] += s': '加上区间和 `s[{j+1}] − s[{i}]` = {s[j+1] - s[i]} → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][-1]': '整排石头合成一堆的最低成本 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='区间里先分出 1 堆，剩下 p-1 堆继续分，合并成本用前缀和',
        complexity='时间 `O(n^3 / k)`，空间 `O(n^2)`',
        problem=['`n` 堆石头排成一排，每次把 ==连续的 `k` 堆== 合成一堆，成本 = 这 `k` 堆石头总数',
                 '求合成一堆的最低成本，做不到返回 `-1`',
                 '示例：`stones = [3,5,1,2,6], k = 3` → `25`'],
        quote='从 n 堆变成 1 堆，需要减少 n−1 堆。而每次合并都会减少 k−1 堆，所以 n−1 必须是 k−1 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['无解条件：`(n − 1) % (k − 1) != 0`',
              '`dfs(i,j)`：只分出 1 堆和 p−1 堆；`m` 从 `i` 起每次跳 `k−1`，保证左边恰好能合成一堆',
              '如果 `[i..j]` 长度满足 `(j−i) % (k−1) == 0`，最后再合成一堆，加上区间和'],
        summary=['时间 `O(n^3/k)`：状态 `O(n^2)` × 单状态枚举 `O(n/k)`',
                 '易错：先判 `-1`；`m` 的步长是 `k−1`，不是 1',
                 '灵神先讲带第三维 `p` 的记忆化搜索，再优化成两个参数的 `dfs(i,j)`，这里演示 1:1 翻译的递推',
                 '同类区间 DP：1547 切棍子的最小成本、1039 多边形三角剖分'],
    ),
)
