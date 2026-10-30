def _layer(k):
    return lambda S: [[c[k] for c in row] for row in S['f']] if 'f' in S else None


def _col(k):
    """k=0 画 f[.][.][0]，k=1 画 f[.][.][1]"""
    def fn(S, r, c, v):
        if S.get('_line') not in (11, 12) or 'i' not in S or 'j' not in S:
            return None
        i, j, lim = S['i'], S['j'], S['limit']
        if S['_line'] == 11:          # 正在算 f[i][j][0]
            if k == 0 and (r, c) == (i, j):
                return 'yellow'
            if (r, c) == (i - 1, j):
                return 'blue'
            if k == 1 and i > lim and (r, c) == (i - lim - 1, j):
                return 'pink'
        else:                          # 正在算 f[i][j][1]
            if k == 1 and (r, c) == (i, j):
                return 'yellow'
            if (r, c) == (i, j - 1):
                return 'blue'
            if k == 0 and j > lim and (r, c) == (i, j - lim - 1):
                return 'pink'
        return None
    return fn


def _txt(S):
    if S.get('_line') == 11 and 'i' in S and 'j' in S:
        i, j, lim = S['i'], S['j'], S['limit']
        f = S['f']
        sub = f[i - lim - 1][j][1] if i > lim else 0
        return (f"`f[{i}][{j}][0] = f[{i-1}][{j}][0] + f[{i-1}][{j}][1] − {sub}` "
                f"= {f[i-1][j][0]} + {f[i-1][j][1]} − {sub}")
    if S.get('_line') == 12 and 'i' in S and 'j' in S:
        i, j, lim = S['i'], S['j'], S['limit']
        f = S['f']
        sub = f[i][j - lim - 1][0] if j > lim else 0
        return (f"`f[{i}][{j}][1] = f[{i}][{j-1}][0] + f[{i}][{j-1}][1] − {sub}` "
                f"= {f[i][j-1][0]} + {f[i][j-1][1]} − {sub}")
    return '`f[i][j][k]`：用 i 个 0、j 个 1，最后一位填 k 的稳定数组数；蓝 = 来源，粉 = 要减掉的'


CONFIG = dict(
    num=3130, title='找出所有稳定的二进制数组 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='三维状态 DP（记忆化搜索 1:1 翻译成递推）',
    tags=['灵神题单·动态规划', '难度分 2825'],
    code='''
class Solution:
    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:
        MOD = 1_000_000_007
        f = [[[0, 0] for _ in range(one + 1)] for _ in range(zero + 1)]
        for i in range(1, min(limit, zero) + 1):
            f[i][0][0] = 1
        for j in range(1, min(limit, one) + 1):
            f[0][j][1] = 1
        for i in range(1, zero + 1):
            for j in range(1, one + 1):
                f[i][j][0] = (f[i - 1][j][0] + f[i - 1][j][1] - (f[i - limit - 1][j][1] if i > limit else 0)) % MOD
                f[i][j][1] = (f[i][j - 1][0] + f[i][j - 1][1] - (f[i][j - limit - 1][0] if j > limit else 0)) % MOD
        return sum(f[-1][-1]) % MOD
''',
    call='Solution().numberOfStableArrays(3, 3, 2)',
    expect=14,
    skip=['MOD = ', 'for i in range(1, zero + 1)', 'for j in range(1, one + 1)'],
    views=[
        dict(type='table', var=_layer(0), label='f[i][j][0]（最后一位是 0）：行 i = 0 的个数，列 j = 1 的个数',
             h=300, cell=64, rows=lambda S: list(range(4)), cols=lambda S: list(range(4)), color=_col(0)),
        dict(type='table', var=_layer(1), label='f[i][j][1]（最后一位是 1）',
             h=300, cell=64, rows=lambda S: list(range(4)), cols=lambda S: list(range(4)), color=_col(1)),
        dict(type='text', fn=_txt, size=23, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'limit'],
    captions={
        'f = [[[0, 0]': '`f[i][j][k]`：`i` 个 0、`j` 个 1，==最后一位填 k==；先全置 0',
        'f[i][0][0] = 1': '边界：只有 0（`j=0`）且 `i ≤ limit`：全是 0 的数组只有 1 种 → `f[{i}][0][0] = 1`',
        'f[0][j][1] = 1': '边界：只有 1（`i=0`）且 `j ≤ limit`：全是 1 的数组只有 1 种 → `f[0][{j}][1] = 1`',
        'f[i][j][0] = (': lambda S, B, r: (
            f'最后一位是 0：前面最后一位 0 或 1 都行 → 相加；但 `i = {S.i} > limit`，会多出 {S.f[S.i - S.limit - 1][S.j][1]} 个末尾 {S.limit + 1} 个 0 的非法数组 → ==减掉== `f[{S.i - S.limit - 1}][{S.j}][1]`'
            if S.i > S.limit else
            f'最后一位是 0：去掉它，前面以 0 或 1 结尾都行 → `f[{S.i}][{S.j}][0]` = =={S.f[S.i][S.j][0]}==（`i ≤ limit`，不会超限，不用减）'),
        'f[i][j][1] = (': lambda S, B, r: (
            f'最后一位是 1：相加后再减掉末尾 {S.limit + 1} 个 1 的非法数：`f[{S.i}][{S.j - S.limit - 1}][0]` → `f[{S.i}][{S.j}][1]` = =={S.f[S.i][S.j][1]}=='
            if S.j > S.limit else
            f'最后一位是 1：`f[{S.i}][{S.j}][1]` = =={S.f[S.i][S.j][1]}==（`j ≤ limit`，不用减）'),
        'return sum': '答案 = 最后一位是 0 的 + 最后一位是 1 的 = `{f[-1][-1][0]} + {f[-1][-1][1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='记住最后一位是 0 还是 1，超限的数量用差减掉',
        complexity='时间 `O(zero·one)`，空间 `O(zero·one)`',
        problem=['用 `zero` 个 0 和 `one` 个 1 排成数组，每个长度超过 `limit` 的子数组必须同时含 0 和 1',
                 '等价于：连续相同的数字最多 `limit` 个',
                 '示例：`zero=3, one=3, limit=2` → `14`'],
        quote='在 dfs(i-1,j,0) 个稳定数组的末尾添加一个 0，会得到 dfs(i-limit-1,j,1) 个不合法的数组。从上文的状态转移方程中减掉它。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只记 `i`、`j` 不够，要知道==最后一位==是 0 还是 1，才能处理 `limit`',
              '`f[i][j][0] = f[i-1][j][0] + f[i-1][j][1]`，但末尾会凑出 `limit+1` 个 0',
              '这种非法数组恰好有 `f[i-limit-1][j][1]` 个（前面是 1，后面全是 0），减掉即可'],
        summary=['时间、空间都是 `O(zero·one)`，每个状态 `O(1)` 转移',
                 '易错：只有 `i > limit` 才减，否则下标会变成负数；减法后可能为负，Python 的 `%` 会自动变回非负',
                 '边界：`f[i][0][0] = 1`（`i ≤ limit`），`f[0][j][1] = 1`（`j ≤ limit`）',
                 '灵神另给了记忆化搜索写法，以及隔板法 + 容斥的组合数学做法 `O(zero·one/limit)`'],
    ),
)
