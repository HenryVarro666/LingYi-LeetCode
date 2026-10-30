from math import gcd as _gcd

MAT = [[2, 3], [4, 6], [3, 5]]


def _cur(S):
    I = S['_inner']
    if 'g' in I and 'i' in I and S.get('_line', 0) >= 11:
        return I['i'] + 1, I['g']
    return None


def _terms(S, B, r):
    i, g, row = S.i, S.g, S.row
    f = S.f
    parts = []
    for x in row:
        d = _gcd(g, x)
        parts.append(f'`f[{i}][gcd({g},{x})={d}]`={f[i][d]}')
    return f'`f[{i + 1}][{g}]` = ' + ' + '.join(parts) + f' → ==`{f[i + 1][g]}`=='


def _txt(S):
    I = S['_inner']
    if 'f' not in S:
        return ''
    if 'g' not in I:
        return '`f[i][g]`：前 `i` 行选完后，==还要再用 GCD 凑成 1== 的方案数（`g` = 已选数的 GCD，初值 0）'
    return f"现在算第 `{I['i'] + 1}` 层：已选数的 GCD 是 `g = {I['g']}`，这一行 `{I['row']}` 逐个选 `x`，新 GCD = `gcd({I['g']}, x)`"


CONFIG = dict(
    num=3725, title='统计每一行选择互质整数的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 1:1 翻译成递推 · f[i][g]',
    tags=['灵神题单', '难度分 1982'],
    code='''
class Solution:
    def countCoprime(self, mat: List[List[int]]) -> int:
        MOD = 1_000_000_007
        m = len(mat)
        mx = max(map(max, mat))
        f = [[0] * (mx + 1) for _ in range(m + 1)]
        f[0][1] = 1
        for i, row in enumerate(mat):
            for g in range(mx + 1):
                f[i + 1][g] = sum(f[i][gcd(g, x)] for x in row) % MOD
        return f[m][0]
''',
    call=f'Solution().countCoprime({MAT})',
    expect=7,
    views=[
        dict(type='table', var='f', label='f[i][g]（行 = 已处理的行数 i，列 = 已选数的 GCD 为 g；黄 = 正在算）',
             rows=lambda S: [f'i={k}' for k in range(len(S['f']))] if 'f' in S else None,
             cols=lambda S: [f'g={k}' for k in range(len(S['f'][0]))] if 'f' in S else None,
             cell=90, h=420,
             cursors=[(lambda S: (_cur(S) or (None, None))[0], lambda S: (_cur(S) or (None, None))[1], 'yellow')],
             color=lambda S, i, j, v: 'green' if (i, j) == (0, 1) else None),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    skip=['for g in range'],
    watch=[('i', 'i', 'blue'), ('g', 'g', 'pink'), ('row', 'row')],
    captions={
        'mx = max': '`mx = {mx}`：所有元素的最大值，GCD 一定落在 `0..mx`',
        'f = [[0]': '`f[i][g]`：对应记忆化搜索里的 `dfs(i-1, g)`，这里 ==从 i=0 往 i=m 递推==',
        'f[0][1] = 1': '边界：`dfs(-1, 1) = 1`，对应 `f[0][1] = 1`，其余都是 0（GCD 不是 1 就失败）',
        'for i, row': '处理第 `{i}` 行 `{row}`',
        'f[i + 1][g] = sum': _terms,
        'return f[m][0]': '`f[m][0]`：从每一行选完、GCD 初值为 0 的方案数 = 答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='dfs(i, g)：已选数的 GCD 为 g，还要凑成 1 的方案数',
        complexity='时间 `O(m·n·U·log U)`，空间 `O(m·U)`',
        problem=['`m × n` 矩阵 `mat`，每行恰好选一个数',
                 '求选出的数 ==最大公约数为 1== 的方案数，对 `10^9+7` 取模',
                 '示例：`[[1,2],[3,4]]` → `3`',
                 '本视频：`[[2,3],[4,6],[3,5]]` → `7`'],
        quote='定义 dfs(i,g) 表示在已选元素的 GCD 为 g 的情况下，从 [0,i] 每行选一个数，最终 GCD 等于 1 的方案数。……g 初始化成 0 是因为 0 和任何数 x 的 GCD 都等于 x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心已选数的 ==GCD==：状态 `(i, g)` 只有 `m × U` 个，不必记住选了哪些数',
              '枚举这一行选 `x`，GCD 变成 `gcd(g, x)`，各选择互斥 → 加法原理求和',
              '记忆化搜索 `dfs(i, g)` 1:1 翻译成递推：`f[i+1][g] = Σ f[i][gcd(g, x)]`，`f[0][1] = 1`'],
        summary=['时间 `O(m·n·U·log U)`，空间 `O(m·U)`，`U` 是矩阵最大值',
                 '易错：`g` 的初值是 0（0 和 x 的 GCD 就是 x），不是 1',
                 '边界只有 `f[0][1] = 1`，其余为 0',
                 '递推会算很多没用的状态，记忆化搜索只算用得到的；本视频演示递推版',
                 '灵神还给了 `@cache` 记忆化搜索写法，以及「倍数容斥」`O(mnU)` 的方法二'],
    ),
)
