def _txt(S):
    I = S.get('_inner', S)
    ln = S.get('_line', 0)
    if 'ori' in I and ln >= 38:
        return f"初始向量 `ori` = {I['ori'][0]}，对应 `[f, g, h, t]`：两不沾 / 同行 / 同列 / 在目标"
    return '状态 `[f, g, h, t]`：两不沾 / 与目标同行 / 与目标同列 / 就在目标点'


BASE_LBL = ['f', 'g', 'h', 't']

CONFIG = dict(
    num=2912, title='在网格上移动到目的地的方法数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按位置分 4 类的状态转移 + 矩阵快速幂',
    tags=['动态规划'],
    code='''
class Solution(object):
    def numberOfWays(self, n, m, k, source, dest):

        \'\'\'
        f[0] = f[0] * (m + n - 4) + f[1] * (n - 1) + f[2] * (m - 1)
        f[1] = f[0] + f[1] * (m - 2) + f[4] * (n - 1)
        f[2] = f[0] + f[2] * (n - 2) + f[4] * (m - 1)
        f[3] = f[1] + f[2]
        \'\'\'

        mod = 10 ** 9 + 7

        base = [[m + n - 4, 1, 1, 0],
                [n - 1, m - 2, 0, 1],
                [m - 1, 0, n - 2, 1],
                [0, m - 1, n - 1, 0]]

        def mul(a, b):
            c = [[0] * len(b[0]) for _ in range(len(a))]
            for i in range(len(a)):
                for j in range(len(b[0])):
                    for k in range(len(a[0])):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= mod
            return c

        def quick_pow(p):
            if p == 1:
                return base[:]

            res = quick_pow(p // 2)

            res = mul(res, res)
            if p % 2 == 1:
                res = mul(res, base)

            return res


        if source[0] == dest[0]:
            if source[1] == dest[1]:
                ori = [[0, 0, 0, 1]]
            else:
                ori = [[0, 1, 0, 0]]
        elif source[1] == dest[1]:
            ori = [[0, 0, 1, 0]]
        else:
            ori = [[1, 0, 0, 0]]

        return mul(ori, quick_pow(k))[0][3]
''',
    call='Solution().numberOfWays(3, 3, 3, [0, 0], [1, 1])',
    expect=6,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='grid', var='base', label='base（转移矩阵，行 = 来源状态，列 = 目标状态）', h=300, cell=70,
             rows=BASE_LBL, cols=BASE_LBL),
        dict(type='grid', var='res', label='res = base^(…)', h=300, cell=70, rows=BASE_LBL, cols=BASE_LBL),
        dict(type='calls', h=130),
    ],
    watch=['p', ('k', 'k', 'blue')],
    skip=["'''", 'f[0] = f[0]', 'f[1] = f[0]', 'f[2] = f[0]', 'f[3] = f[1]', 'mod = ', 'def mul', 'def quick_pow',
          'c = [[0]', 'for i in range', 'for j in range', 'for k in range', 'c[i][j]', '[n - 1, m - 2', '[m - 1, 0, n - 2', '[0, m - 1, n - 1, 0]]'],
    captions={
        'base = [[': '把 4 类位置之间的转移写成矩阵 `base`：第 i 个转移方程的第 j 项系数，填到第 j 行第 i 列。`n = m = 3`',
        'return base[:]': '`p == 1`：一步转移就是 `base` 本身',
        'res = quick_pow(p // 2)': '快速幂：先求 `base^({p}//2)`（原文 `p / 2` 是 Python 2 整数除法，已改 `//`）',
        'res = mul(res, res)': '`res` 自乘：`base^{p//2}` × `base^{p//2}` = `base^{p - p % 2}`，所有数对 `1e9+7` 取模',
        'res = mul(res, base)': '`p = {p}` 是奇数：再乘一个 `base`，凑成 `base^{p}`',
        'return res': '返回 `base^{p}`',
        'return c': '`mul` 返回乘积矩阵（三重循环逐项累加并取模，这里快进）',
        'ori = [[0, 0, 0, 1]]': '起点就是终点 → 初始向量只有 `t = 1`',
        'ori = [[0, 1, 0, 0]]': '起点与终点同行不同列 → 初始向量只有 `g = 1`',
        'ori = [[0, 0, 1, 0]]': '起点与终点同列不同行 → 初始向量只有 `h = 1`',
        'ori = [[1, 0, 0, 0]]': '行列都不同 → 初始向量只有 `f = 1`（起点是「两不沾」）',
        'return mul(ori': '`[f,g,h,t]_k = ori × base^k`，答案取结果向量里的 `t`（下标 3，即「恰好落在目标点」）',
    },
    cards=dict(
        one_liner='按「和目标点的行列关系」分成 4 类，走一步就是乘一个 4×4 矩阵',
        complexity='时间 `O(log k · 4³)`，空间 `O(1)`',
        problem=['`n×m` 网格，每步只能沿行或列移动到==同行/同列的另一格==（不能原地不动）',
                 '求从 `source` 恰好走 `k` 步到 `dest` 的方案数，模 `10^9+7`',
                 '本视频：`n=m=3`，`k=3`，`source=[0,0]`，`dest=[1,1]` → `6`'],
        quote='直接令f[i]表示i步操作后横纵坐标都不等于目标值的方案数，g[i]表示横坐标在目标值但纵坐标不在的方案数，h[i]与g[i]对称，而t[i]则表示位于目标位置的方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试过「横纵拆开 + 组合数」，要用逆元和快速幂，太复杂，放弃',
              '改成直接建模：`f` 两不沾、`g` 同行、`h` 同列、`t` 目标，四个转移方程 → 4×4 矩阵 `base`',
              '`[f,g,h,t]_k = [f,g,h,t]_0 × base^k`，用快速幂算 `base^k`'],
        summary=['时间 `O(log k)`（矩阵固定 4×4），空间 `O(1)`',
                 '易错：起点所属的类别决定初始向量；答案是 `t` 那一项（下标 3）',
                 '`m + n - 4`：从两不沾的点出发，能走的格子要扣掉同行同列各 1 个再扣原地',
                 '原文为 Python 2 写法，`quick_pow` 里的 `p / 2` 已改为 `p // 2`；其余未改'],
    ),
)
