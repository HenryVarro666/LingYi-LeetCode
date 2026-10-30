from math import sqrt as _sqrt

JMAX = 14
G2 = [j * (j + 1) // 2 for j in range(JMAX + 1)]  # g[2][j] = 1 + 2 + … + j


def _table(S):
    return [list(range(1, JMAX + 1)), G2[1:]]


def _table_color(S, r, c, v):
    n, res = S.get('n'), S.get('res')
    j = c + 1
    if res is not None and j == res:
        return 'yellow'
    if n is not None and G2[j] >= n:
        return 'green'
    return None


def _formula(S):
    n = S.get('n')
    if n is None:
        return ''
    x = _sqrt(n * 2 + 0.25) - 0.5
    s = f'`sqrt({n}×2 + 0.25) − 0.5 = {x:.3f}`'
    if 'res' in S:
        r = S['res']
        s += f'；检查 `res·(res+1) = {r}×{r + 1} = {r * (r + 1)}` vs `2n = {2 * n}`'
    return s


def _res_cap(S, B, ret):
    n, r = S.n, S.res
    x = _sqrt(n * 2 + 0.25) - 0.5
    return f'`n = {n}`：解 `(1+j)·j/2 ≥ {n}` 得 `j ≥ {x:.3f}`；`int()` 向下取整 → `res = {r}`'


def _if_cap(S, B, ret):
    n, r = S.n, B.res
    g = r * (r + 1) // 2
    if r * (r + 1) < n + n:
        return f'`{r}×{r + 1} = {r * (r + 1)} < {2 * n}`：扔 {r} 次最多确定 `{g}` 层 < {n} → ==不够==，要 +1'
    return f'`{r}×{r + 1} = {r * (r + 1)} ≥ {2 * n}`：扔 {r} 次能确定 `{g}` 层 ≥ {n} → ==够了=='


CONFIG = dict(
    num=1884, title='鸡蛋掉落-两枚鸡蛋', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='反向 DP：g[i][j] = 扔 j 次能确定的最大高度',
    tags=['字节30天'],
    code='''
class Solution(object):
    def twoEggDrop(self, n):
        res = int(sqrt((n * 2 + 0.25)) - 0.5)
        if res * (res + 1) < n + n:
            res += 1

        return res
''',
    setup='from math import sqrt  # LeetCode 环境预置',
    call='[Solution().twoEggDrop(n) for n in (2, 6, 100)]',
    expect=[2, 3, 14],
    views=[
        dict(type='text', fn=lambda S: f"询问 `n = {S['n']}`" if 'n' in S else '', size=26, h=56),
        dict(type='grid', var=_table, label='g[2][j]：扔 j 次最多能确定的楼层数（绿 = 已 ≥ n，第一个绿格就是答案；黄 = res）',
             rows=['j', 'g'], cell=68, h=230, color=_table_color),
        dict(type='text', fn=_formula, size=25, h=90, lines=2),
        dict(type='text', fn=lambda S: '`g[2][j] = g[1][j−1] + 1 + g[2][j−1] = g[2][j−1] + j` → `g[2][j] = (1+j)·j/2`',
             size=24, h=60),
    ],
    watch=[('n', 'n'), ('res', 'res', 'yellow')],
    captions={
        'res = int(sqrt': _res_cap,
        'if res * (res + 1) < n + n': _if_cap,
        'res += 1': '向下取整少了一次 → `res = {res}`',
        'return res': '`n = {n}` 层楼最少要扔 =={ret}== 次',
    },
    cards=dict(
        one_liner='反过来想：两枚蛋扔 j 次最多能确定 (1+j)·j/2 层，找最小的 j',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两枚相同的鸡蛋，`n` 层楼；存在楼层 `f`：高于 `f` 扔下会碎，不高于则不碎',
                 '每次可以扔一枚没碎的蛋，求==确定 f 的最少操作次数==（最坏情况）',
                 '示例：`n = 2` → `2`；`n = 100` → `14`'],
        quote='不考虑确定f的最小操作次数，而是==令g[i][j]表示i枚鸡蛋，丢j次可以确定的最大高度==，然后通过g[i][j]与n的大小确定j的最小值，即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 j 次在第 `g[i−1][j−1] + 1` 层扔：碎了回到 `g[i−1][j−1]`，没碎还能往上确认 `g[i][j−1]` 层',
              '`g[i][j] = g[i−1][j−1] + 1 + g[i][j−1]`，边界 `g[1][j] = j`、`g[i][1] = 1`',
              '两枚蛋：`g[2][j] = 1 + 2 + … + j = (1+j)·j/2`，解出最小的 j'],
        after=[dict(heading='为什么还要检查一次？', lines=[
            '`(1+j)·j/2 ≥ n` ⟺ `j ≥ sqrt(2n + 0.25) − 0.5`，答案是它的==上取整==',
            '代码先用 `int()` 向下取整，再检查 `res·(res+1) < 2n`：不够就 `+1`',
            '`n = 6`：`sqrt(12.25) − 0.5 = 3` 恰好是整数，不用 +1'])],
        summary=['时间、空间都是 `O(1)`',
                 '核心：把“最少扔几次”转成“扔 j 次最多确定几层”',
                 '`k` 枚蛋时同一个 `g[i][j]` 递推就是 887 题的高效解法',
                 '原文为 Python 2 风格：只删去文档字符串，代码未改',
                 '`sqrt` 是 LeetCode 预置的 `math.sqrt`（本视频在 setup 里导入）'],
    ),
)
