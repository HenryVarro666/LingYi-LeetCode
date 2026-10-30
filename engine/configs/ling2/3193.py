N, REQS = 4, [[3, 3], [1, 1]]


def _gcolor(S, r, c, v):
    i, j, line = S.get('i'), S.get('j'), S.get('_line')
    if i is None or j is None or line not in (19, 22):
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if line == 19 and (r, c) == (i - 1, S['r']):
        return 'blue'
    if line == 22 and r == i - 1 and j - min(i, j) <= c <= j:
        return 'blue'
    return None


def _info(S):
    i, line = S.get('i'), S.get('_line')
    if i is None or 'r' not in S or line not in (17, 18, 19, 20, 21, 22):
        return '`f[i][j]`：`perm[0..i]`（==还剩 i+1 个数==）逆序对恰好为 j 的方案数'
    r, mx = S['r'], S['mx']
    if r >= 0:
        return (f'`req[{i - 1}] = {r}`：前 `{i}` 个数必须恰好 `{r}` 个逆序对 → 只能从 `f[{i - 1}][{r}]` 转移，'
                f'`j` 取 `[{r}, min({i} + {r}, {mx})]`')
    return f'`req[{i - 1}] = -1`（没有要求）→ `f[{i}][j] = Σ f[{i - 1}][j − k]`，`k = 0..min({i}, j)`'


def _cap_sum(S, B, ret):
    i, j = S.i, S.j
    ks = list(range(min(i, j) + 1))
    terms = ' + '.join(str(S.f[i - 1][j - k]) for k in ks)
    return (f'`f[{i}][{j}]` = 枚举 perm[{i}] 和左边组成 `k = 0..{min(i, j)}` 个逆序对：`{terms}` = =={S.f[i][j]}==')


CONFIG = dict(
    num=3193, title='统计逆序对的数目', difficulty='Hard', category='多维动态规划',
    author='灵茶山艾府', technique='枚举最后一个数和左边组成几个逆序对 · 递推',
    tags=['字节30天'],
    code='''
class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        MOD = 1_000_000_007
        req = [-1] * n
        req[0] = 0
        for end, cnt in requirements:
            req[end] = cnt
        if req[0]:
            return 0

        m = max(req)
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1
        for i in range(1, n):
            mx = m if req[i] < 0 else req[i]
            r = req[i - 1]
            if r >= 0:
                for j in range(r, min(i + r, mx) + 1):
                    f[i][j] = f[i - 1][r]
            else:
                for j in range(mx + 1):
                    f[i][j] = sum(f[i - 1][j - k] for k in range(min(i, j) + 1)) % MOD
        return f[-1][req[-1]]
''',
    call=f'Solution().numberOfPermutations({N}, {REQS})',
    expect=3,
    skip=['MOD = 1_000_000_007', 'for j in range', 'req[0] = 0'],
    views=[
        dict(type='text', h=90, size=24, lines=2, fn=_info),
        dict(type='array', var='req', label='req[i]：perm[0..i] 要求的逆序对数（-1 = 没要求）', cell=90, h=205,
             pointers={'i': 'yellow', 'i - 1': 'blue'}, pointer_labels={'i - 1': 'i−1'}),
        dict(type='grid', var='f', label='f[i][j]（行 i，列 j；黄 = 正在算，蓝 = 用到的上一行）',
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f'][0]))), cell=84, h=335,
             color=_gcolor),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j'), ('r', 'r', 'blue'), ('mx', 'mx'), ('m', 'm')],
    captions={
        'req = [-1] * n': '`req[i]`：`perm[0..i]` 必须有的逆序对数；`-1` 表示没要求；`req[0]` 一定是 0',
        'for end, cnt in requirements': lambda S, B, ret: (f'要求：`perm[0..{S.end}]` 恰好 `{S.cnt}` 个逆序对' if S.get('end') != B.get('end') or 'end' not in B
                                                           else '要求都记好了'),
        'req[end] = cnt': '`req[{end}] = {cnt}`',
        'if req[0]': '`req[0] = 0`：只有一个数，不可能有逆序对，合法',
        'm = max(req)': '逆序对最多 `m = {m}` 个，第二维开到 `m`',
        'f = [[0]': '`f[i][j]`：`perm[0..i]` 的逆序对为 `j` 的排列个数',
        'f[0][0] = 1': '边界：只剩 1 个数，逆序对为 0，方案数 `f[0][0] = 1`',
        'for i in range(1, n)': lambda S, B, ret: (f'计算第 `i = {S.i}` 行（perm[{S.i}] 和左边 `{S.i}` 个数组成 `0..{S.i}` 个逆序对）'
                                                   if S.get('i') != B.get('i') or 'i' not in B else '所有行都算完了'),
        'mx = m if req[i] < 0': lambda S, B, ret: (f'`req[{S.i}] = -1`：本行 j 最多算到 `m = {S.mx}`' if S.req[S.i] < 0
                                                    else f'`req[{S.i}] = {S.req[S.i]}`：本行只需要 j ≤ `{S.mx}`'),
        'r = req[i - 1]': '`r = req[{i - 1}] = {r}`',
        'if r >= 0': lambda S, B, ret: (f'`r = {S.r} ≥ 0`：前 `{S.i}` 个数的逆序对==必须恰好是 {S.r}==，k 只有一种取法 `k = j − {S.r}`' if S.r >= 0
                                        else f'`r = -1`：前 `{S.i}` 个数没要求 → 枚举 k 求和'),
        'f[i][j] = f[i - 1][r]': lambda S, B, ret: (
            f'`f[{S.i}][{S.j}] = f[{S.i - 1}][{S.r}] = {S.f[S.i][S.j]}`：perm[{S.i}] 和左边组成 `{S.j - S.r}` 个逆序对，剩下恰好 `{S.r}`'),
        'f[i][j] = sum(': _cap_sum,
        'return f[-1][req[-1]]': '答案 `f[{n - 1}][req[{n - 1}]]` = `f[{n - 1}][{req[-1]}]` = {ret}',
    },
    max_steps=60,
    cards=dict(
        one_liner='只看最后一个数和左边组成几个逆序对，剩下的是同样的子问题',
        complexity='时间 `O(nm*min(n,m))`，空间 `O(nm)`，`m = max(cnt)`',
        problem=['求 `[0, 1, …, n−1]` 的排列 `perm` 的个数（模 `10^9+7`）',
                 '满足每个要求 `[end, cnt]`：`perm[0..end]` 中==恰好 cnt 个逆序对==',
                 '示例：`n = 3, requirements = [[2,2],[0,0]]` → `2`',
                 f'本视频：`n = {N}, requirements = {REQS}` → `3`'],
        quote='在解决子问题时，无需知道具体还剩下哪些数，只需要知道剩余数字的个数，以及剩余逆序对的个数。用这两个个数去定义状态，就会产生重复的子问题。',
        quote_src='—— 灵茶山艾府题解「寻找子问题」',
        idea=['`perm[i]` 和左边 `i` 个数组成 `k` 个逆序对（`k ≤ min(i, j)`），剩下子问题 `f[i−1][j−k]`',
              '`f[i][j] = Σ f[i−1][j−k]`；若 `req[i−1] = r ≥ 0`，则只能 `k = j − r`：`f[i][j] = f[i−1][r]`',
              '边界 `f[0][0] = 1`，答案 `f[n−1][req[n−1]]`'],
        result='`f[3][3] = 1 + 1 + 1 + 0 = 3` → 返回 `3`',
        summary=['时间 `O(nm*min(n,m))`，空间 `O(nm)`',
                 '关键：子问题只和“剩几个数、剩几个逆序对”有关，与具体是哪些数无关',
                 '易错：`r ≥ 0` 时 `j` 只能在 `[r, i + r]` 内，其余为 0',
                 '题解的终极优化：前缀和把求和降到 `O(1)`，再压成一维，`O(nm)` 时间'],
    ),
)
