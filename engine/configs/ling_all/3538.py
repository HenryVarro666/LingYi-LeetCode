def _tbl(S):
    f = S.get('f')
    if f is None:
        return None
    return [[v for row in fj for v in row] for fj in f]


def _cols(S):
    K = S['K']
    return [f'{a},{b}' for a in range(K + 1) for b in range(K + 1)]


def _rows(S):
    return [f'j={j}' for j in range(S['n'])]


def _color(S, r, c, v):
    if 'j' not in S or 'sz' not in S:
        return None
    K = S['K']
    if S.get('_line') == 12 and 'left_k' in S and (r, c) == (S['j'], S['sz'] * (K + 1) + S['left_k']):
        return 'yellow'
    if S.get('_line') == 12 and 'left_k' in S:
        j, lk, sz = S['j'], S['left_k'], S['sz']
        for k in range(j + 1, j + 2 + lk):
            if r == k and c == (k - j - 1) * (K + 1) + lk - (k - j - 1):
                return 'blue'
    return None


def _w0(S):
    if 'j' in S and 'sz' in S and S.get('_line', 0) >= 9:
        return S['j'] - S['sz']
    return None


def _cap_f(S, B, ret):
    j, sz, lk = S.j, S.sz, S.left_k
    if S.f == B.f:
        return (f'`f[{j}][{sz}][{lk}]`：当前子数组 `[{j - sz}, {j}]`，还要合并 `{lk}` 次。'
                f'枚举下一个子数组 `[{j + 1}, k]`，`k = {j + 1} .. {j + 1 + lk}`（蓝格是候选来源）')
    t = S.t
    parts = []
    for k in range(j + 1, j + 2 + lk):
        a = S.f[k][k - j - 1][lk - (k - j - 1)]
        d = (S.position[k] - S.position[j]) * t
        parts.append(f'k={k}：`{a}` + `{d}` = {a + d}')
    return (f'下一个子数组 `[{j + 1}, k]`，路程 × 本段时间 `{t}`；' + '；'.join(parts)
            + f' → 取最小，`f[{j}][{sz}][{lk}]` = =={S.f[j][sz][lk]}==')


CONFIG = dict(
    num=3538, title='合并得到最小旅行时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='相邻相关划分型 DP · 递推',
    tags=['灵神题单·动态规划', '难度分 2461'],
    code='''
class Solution:
    def minTravelTime(self, _, n: int, K: int, position: List[int], time: List[int]) -> int:
        s = list(accumulate(time, initial=0))  # 计算 time 的前缀和
        f = [[[inf] * (K + 1) for _ in range(K + 1)] for _ in range(n)]
        for sz in range(K + 1):
            f[-1][sz][0] = 0
        for j in range(n - 2, -1, -1):  # 转移来源 k 比 j 大，所以要倒序
            for sz in range(min(K, j) + 1):
                t = s[j + 1] - s[j - sz]  # 合并到 time[j] 的时间
                for left_k in range(min(K, n - 2 - j) + 1):
                    # 枚举下一个子数组 [j+1, k]
                    f[j][sz][left_k] = min(f[k][k - j - 1][left_k - (k - j - 1)] + (position[k] - position[j]) * t
                                          for k in range(j + 1, j + 2 + left_k))
        return f[0][0][K]  # 第一个子数组是 [0, 0]
''',
    call='Solution().minTravelTime(10, 4, 1, [0, 3, 8, 10], [5, 8, 3, 6])',
    expect=62,
    views=[
        dict(type='text', fn=lambda S: ('`f[j][sz][left_k]`：当前子数组 `[j-sz, j]`，还要合并 `left_k` 次，走完剩余路程的最短时间'), size=21, h=50),
        dict(type='array', var='time', label='time（蓝框 = 当前子数组 [j-sz, j]）', window=(_w0, 'j'), pointers={'j': 'blue'}, h=150, cell=70),
        dict(type='array', var='position', label='position', h=110, cell=70, index=False),
        dict(type='table', var=_tbl, label='f[j][sz][left_k]（列 = sz,left_k；inf = 不合法）', cols=_cols, rows=_rows, color=_color, h=290, cell=70),
    ],
    watch=[('j', 'j', 'blue'), 'sz', 'left_k', 't'],
    skip=[5, 7, 8, 10, 13],
    captions={
        3: '先算 `time` 的前缀和 `s = {s}`：子数组 `[a, b]` 的时间和 = `s[b+1] − s[a]`',
        4: '建 `f[j][sz][left_k]`，全部先填 `inf`（不合法）',
        6: '终点 `j = n−1`，子数组长度 `sz = {sz}`：路走完了，`left_k = 0` 合法，费用 ==0==',
        9: '`j = {j}, sz = {sz}`：当前子数组 `[{j - sz}, {j}]`，每公里 `t = s[{j + 1}] − s[{j - sz}]` = =={t}== 分钟',
        12: _cap_f,
        14: '`f[0][0][K]`：第一个子数组固定是 `[0,0]`，还要合并 `K` 次 → 总时间 =={ret}==',
    },
    cards=dict(
        one_liner='把 time 切成 n−k 段，相邻两段的路程乘前一段的时间和',
        complexity='时间 `O(nk³)`，空间 `O(nk²)`',
        problem=['直路上有 `n` 个路标 `position`，`time[i]` 是 `position[i]` 到下一个路标每公里的时间',
                 '必须恰好合并 `k` 次：删掉路标 `i`（`i > 0`），把 `time[i]` 加到 `time[i+1]`',
                 '示例：`l=10, k=1, position=[0,3,8,10], time=[5,8,3,6]` → `62`'],
        quote='题意相当于把 time 数组切 n−k−1 刀，划分成恰好 n−k 个连续子数组。特别地，在 0 和 1 之间一定要切一刀，把 time[0] 单独作为一个子数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻两个子数组 `[i,j]`、`[j+1,k]`：从 `position[j]` 走到 `position[k]`，每公里时间 = 前一段的 time 之和',
              '这是==相邻相关==的划分型 DP：状态要带上当前子数组的左端，所以是 `(j, sz, left_k)`',
              '子数组长度不超过 `k+1`，用 `sz`（长度减一）代替左端点，状态数更小'],
        summary=['时间 `O(nk³)`，空间 `O(nk²)`',
                 '第一个子数组必须是 `[0,0]`，所以答案是 `f[0][0][K]`',
                 '终点 `j = n-1` 时必须 `left_k = 0`，其余状态为 `inf`',
                 '题解还有写法一：记忆化搜索，递推就是它的 1:1 翻译（转移来源更大，所以 `j` 倒序）'],
    ),
)
