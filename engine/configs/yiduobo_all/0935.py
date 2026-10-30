CONFIG = dict(
    num=935, title='骑士拨号器', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='对称合并成 4 类 + 矩阵快速幂（递归）',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def knightDialer(self, n):

        if n == 1:
            return 10

        mod = 10 ** 9 + 7

        #f[i][0] = 2f[i - 1][4]
        #f[i][1] = f[i - 1][4] + f[i - 1][2]
        #f[i][2] = 2f[i - 1][1]
        #f[i][4] = 2f[i - 1][1] + f[i - 1][0]

        x = [[0, 0, 0, 2], [0 ,0, 1, 1], [0, 2, 0, 0], [1, 2, 0, 0]]
        now = self.quickPow(n - 1, x, mod)
        return (sum(now[0]) + 4 * sum(now[1]) + 2 * sum(now[2]) + 2 * sum(now[3])) % mod

    def quickPow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        now = self.quickPow(n // 2, base, mod)
        l = len(base)
        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][j] += now[i][k] * now[k][j]
                tmp[i][j] %= mod
        
        if n % 2 == 0:
            return tmp[:]
        
        now = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    now[i][j] += tmp[i][k] * base[k][j]
                now[i][j] %= mod
        return now[:]
''',
    call='Solution().knightDialer(6)',
    expect=544,
    skip=['for i in range(l)', 'for j in range(l)', 'for k in range(l)', 'tmp[i][j] +=', 'tmp[i][j] %=', 'now[i][j] +=', 'now[i][j] %=', 'l = len(base)', 'mod = 10'],
    views=[
        dict(type='text', h=70, size=24, fn=lambda S: '对称合并：`f1=f3=f7=f9`，`f2=f8`，`f4=f6`，只剩 `f0、f1、f2、f4` 四个变量'),
        dict(type='table', var='base', label='base = 4×4 转移矩阵（行列顺序 f0, f1, f2, f4）', h=300, cell=66,
             rows=['f0', 'f1', 'f2', 'f4'], cols=['f0', 'f1', 'f2', 'f4']),
        dict(type='table', var='now', label='now = 当前层的矩阵幂', h=300, cell=66,
             rows=['f0', 'f1', 'f2', 'f4'], cols=['f0', 'f1', 'f2', 'f4']),
        dict(type='calls', h=200, hide=('base', 'mod')),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'if n == 1:': lambda S, B, r: ('`n = 1`，只走 0 步 → 直接返回 10' if S.n == 1 and S.get('base') is None else
                                       ('`n = 1`：递归边界，返回 `base` 本身（1 次幂）' if S.n == 1 else f'`n = {S.n}` ≠ 1，继续往下分')),
        'x = [[': '`x` 是推导出的 4×4 转移矩阵：每一行是 `f0, f1, f2, f4` 的递推系数',
        'now = self.quickPow(n - 1': '要走 `n-1 = 5` 步 → 求转移矩阵的 5 次方 `x^5`，用递归快速幂',
        'return (sum(now[0])': '`now = x^(n-1)`；初始 `f` 全是 1，所以每行求和就是该变量的值。答案 = `1×f0 + 4×f1 + 2×f2 + 2×f4`，取模 = =={ret}==',
        'now = self.quickPow(n // 2': '先递归求 `base^(n//2)`：`n = {B.n}` → 子问题 `n = {B.n // 2}`',
        'tmp = [[0]': '`tmp` 将保存 `now × now`，即 `base^({n // 2 * 2})`（下面三重循环：矩阵乘法）',
        'if n % 2 == 0': lambda S, B, r: (f'`n = {S.n}` 是偶数：`base^n = tmp`，直接返回' if S.n % 2 == 0
                                          else f'`n = {S.n}` 是奇数：`tmp = base^{S.n - 1}`，还要再乘一次 `base`'),
        'return tmp[:]': '返回 `base^{n}`',
        'now = [[0]': '`now` 将保存 `tmp × base`',
        'return now[:]': '`now = tmp × base = base^{n}` → 返回',
        'return base[:]': '递归边界：`base^1 = base`',
    },
    cards=dict(
        one_liner='键盘左右对称，10 个变量压成 4 个，再套矩阵快速幂',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['骑士只能站在电话键盘的数字格上，按「日」字走',
                 '走 `n-1` 步得到长度为 `n` 的号码，求不同号码个数（对 `1e9+7` 取模）',
                 '示例：`n = 1` → `10`，`n = 2` → `20`',
                 '本视频：`n = 6` → `544`'],
        quote='键盘左右应该是完全对称的，那么就有 f[i][1] = f[i][3]，f[i][4] = f[i][6]，f[i][7] = f[i][9]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：长度 `i+1`、以 `j` 结尾的号码数，每个 `j` 由马能跳来的格子相加',
              '10×10 的矩阵太大；用对称性推出 `f1=f3=f7=f9`、`f2=f8`、`f4=f6`',
              '只剩 4 个变量 → 4×4 转移矩阵，快速幂后各行求和，再按 `1,4,2,2` 加权'],
        before=[dict(heading='推导：4 个变量的转移', lines=[
            '`f[i][0] = 2 f[i-1][4]`', '`f[i][1] = f[i-1][4] + f[i-1][2]`',
            '`f[i][2] = 2 f[i-1][1]`', '`f[i][4] = 2 f[i-1][1] + f[i-1][0]`'])],
        summary=['时间 `O(log n)`，每次矩阵乘法 `4^3 = 64` 次',
                 '原文为 Python 2 写法，`quickPow` 里的 `n / 2` 已改为 `n // 2`',
                 '视频里把矩阵乘法的三重循环折叠成一步，只展示递归和结果',
                 '易错：`n = 1` 要单独返回 10；加权系数是 `1, 4, 2, 2`',
                 '对比灵神：灵神用 A,B,C,D 四类 + 迭代快速幂；yiduobo 用对称推导 + 递归快速幂'],
    ),
)
