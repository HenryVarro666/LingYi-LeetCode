LAB = ['0', '1', '2', '3', '4', '5']
N = 5


def _base(S):
    I = S['_inner']
    v = I.get('base')
    return v if isinstance(v, list) else I.get('X', S.get('X'))


def _tmp(S):
    v = S['_inner'].get('tmp')
    return v if isinstance(v, list) else None


def _res(S):
    v = S['_inner'].get('res')
    return v if isinstance(v, list) and v and isinstance(v[0], list) else None


CONFIG = dict(
    num=552, title='学生出勤记录 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='6 状态 DP → 矩阵 + 递归快速幂',
    tags=['动态规划'],
    code='''
class Solution(object):
    def checkRecord(self, n):

        X = [[1, 1, 0, 1, 0, 0],
             [1, 0, 1, 1, 0, 0],
             [1, 0, 0, 1, 0, 0],
             [0, 0, 0, 1, 1, 0],
             [0, 0, 0, 1, 0, 1],
             [0, 0, 0, 1, 0, 0]]
        mod = 10 ** 9 + 7
        return sum(self.quick_pow(X, n, mod)[0]) % mod

    def quick_pow(self, base, p, mod):
        if p == 1:
            return base
        
        tmp = self.quick_pow(base, p // 2, mod)
        res = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod

        if p % 2 == 0:
            return res
        
        tmp = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
''',
    call=f'Solution().checkRecord({N})',
    expect=94,
    skip=[5, 6, 7, 8, 9, 'for i in range(6)', 'for j in range(6)', 'for k in range(6)', 'res[i][j] +=', 'res[i][j] %=',
          'tmp[i][j] +=', 'tmp[i][j] %='],
    views=[
        dict(type='calls', h=130, hide=('base', 'mod', 'X')),
        dict(type='table', var=_base, label='base（= X，行 = 昨天的状态，列 = 今天的状态）', h=200, cell=70, rows=LAB, cols=LAB),
        dict(type='table', var=_tmp, label='tmp（递归回来的 X^(p//2)；奇数时被换成 res × base）', h=200, cell=70, rows=LAB, cols=LAB),
        dict(type='table', var=_res, label='res = tmp × tmp', h=200, cell=70, rows=LAB, cols=LAB),
        dict(type='text', size=20, h=40, fn=lambda S: '状态 0 无A无L｜1 无A末1L｜2 无A末2L｜3 一A无L｜4 一A末1L｜5 一A末2L'),
    ],
    watch=[('p', lambda S: S['_inner'].get('p'), 'blue'), ('mod', lambda S: S['_inner'].get('mod'))],
    captions={
        4: lambda S, B, r: ('转移矩阵 `X`（`A × X = B`）：`X[k][j] = 1` 表示昨天状态 k ==能变成==今天状态 j'
                            if 'X' not in S else '例如第 0 列 `[1,1,1,0,0,0]`：`f[i][0] = f[i-1][0] + f[i-1][1] + f[i-1][2]`（今天到场，清零迟到）'),
        10: '`mod = {mod}`：矩阵里每次乘加都要取模',
        11: lambda S, B, r: ('`sum(quick_pow(X, n, mod)[0])`：初始 `A = [1,0,0,0,0,0]`，所以答案是 `X^n` ==第 0 行==的和'),
        14: lambda S, B, r: (f'`p = {S.p}`：不是 1，先求一半' if S.p != 1 else '`p = 1`：递归到底，`X^1` 就是 ==base 本身=='),
        15: '返回 `base`',
        17: lambda S, B, r: (f'`p = {B.p}`：先递归求 `X^{B.p // 2}`（一半）' if 'tmp' not in S
                             else f'递归回来：`tmp` = ==X^{S.p // 2}=='),
        18: '`res = tmp × tmp`：三重循环做矩阵乘法并取模，得到 ==X^{p // 2 * 2}==',
        25: lambda S, B, r: (f'`p = {S.p}` 是偶数：`tmp²` 恰好是 `X^{S.p}`，直接返回' if S.p % 2 == 0
                             else f'`p = {S.p}` 是奇数：平方只得到 `X^{S.p - 1}`，还差一个 X'),
        26: '偶数：返回 `res`',
        28: '奇数：把 `tmp` 重新开成零矩阵，下面用它存 `res × base`',
        35: '返回 `X^{p}`（`tmp = res × base`）',
    },
    cards=dict(
        one_liner='把「状态 DP」写成 1×6 行向量乘 6×6 矩阵，再用快速幂',
        complexity='时间 `O(6^3 · log n)`，空间 `O(log n)`',
        problem=['出勤记录只含 `A`（缺勤）`L`（迟到）`P`（到场）',
                 '可奖励：==A 少于 2 天==，且==不能连续 3 天 L==；求长为 `n` 的可奖励记录数，对 `10^9+7` 取模',
                 '示例：`n = 2` → `8`；本视频 `n = 5` → `94`'],
        quote='到了这里，就有一个递推的做法了。……不过注意到n最大可以到100000，那么这里采用矩阵乘法加快速幂的做法是更好的。',
        quote_src='—— yiduobo 题解原文',
        idea=['6 个状态：有没有缺席过（0/1 次）× 末尾累积迟到几天（0/1/2）',
              '`f[i][0] = f[i-1][0]+f[i-1][1]+f[i-1][2]`：今天 P，迟到清零；缺席、迟到各有对应的转移',
              '每天只依赖昨天 → 行向量 `A × X = B`；`A` 只有第 0 个元素是 1，答案 = `X^n` 第 0 行之和'],
        summary=['时间 `O(log n)`（矩阵阶数是常数 6），空间 `O(log n)` 递归栈',
                 '易错：缺席那天会把迟到累积清零，所以 `f[i][3]` 要加上 `f[i-1][0..5]`',
                 '`quick_pow` 奇数时平方后==还要再乘一次 base==；`p == 1` 是递归出口',
                 '原文为 Python 2 写法，`quick_pow` 里的 `p / 2` 已改为 `p // 2`',
                 '对比灵神：灵神从右往左填字母定义 `(j,k)` 状态；yiduobo 按“昨天→今天”列 6 个状态，矩阵相同'],
    ),
)
