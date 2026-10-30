CONFIG = dict(
    num=4073, title='统计好字符串数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='推导出斐波那契 · 矩阵快速幂',
    tags=[],
    code='''
class Solution(object):
    def countGoodStrings(self, n):
        
        def mul(a, b, mod):
            c = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= mod
            return c

        def quick_pow(base, p, mod):
            if p == 0:
                return [[1, 0], [0, 1]]
            
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2, mod)
            res = mul(res, res, mod)
            if p % 2 == 1:
                res = mul(res, base, mod)
            return res

        mod = 10 ** 9 + 7
        base = [[0, 1], [1, 1]]
        f = quick_pow(base, n - 1, mod)
        return f[1][1] * 2 % mod
''',
    call='Solution().countGoodStrings(5)',
    expect=10,
    views=[
        dict(type='grid', var='a', label='a（mul 的左因子）', h=130, cell=64),
        dict(type='grid', var='b', label='b（mul 的右因子）', h=130, cell=64),
        dict(type='grid', var='c', label='c = a × b（逐格累加后取模）',
             cursors=[('i', 'j', 'yellow', '(i,j)')], h=130, cell=64),
        dict(type='calls', h=170),
        dict(type='text', h=80, size=28,
             fn=lambda S: 'f[k] = f[k-1] + f[k-2]，f[1]=2：答案 = ==2 × Fib(n)==，用矩阵 `[[0,1],[1,1]]` 的 n−1 次幂求第 n 项'),
    ],
    watch=['n', 'p', 'i', 'j', 'k', ('mod', 'mod')],
    skip=['c = [[0, 0]', 'for i in range', 'for j in range', 'for k in range', 'c[i][j] %= mod',
          'mod = 10', 'base = [['],
    captions={
        'def countGoodStrings': '长度为 `n = {n}` 的好字符串数量，先推公式再算',
        'def mul': '先定义 2×2 矩阵乘法（对 `mod` 取模）',
        'def quick_pow': '再定义矩阵快速幂：`base^p`',
        'c[i][j] += a[i][k] * b[k][j]': '`c[{i}][{j}] += a[{i}][{k}] × b[{k}][{j}]` = `{a[i][k]} × {b[k][j]}` → `{c[i][j]}`',
        'return c': '乘完了，得到 `{c}`',
        'f = quick_pow': '算 `base^(n−1)`，即 `base^{n-1}`',
        'if p == 0': '`p = {p}`，`p == 0` 吗？不是则往下',
        'if p == 1': lambda S, B, r: ('`p = 1`：幂就是 `base` 本身，递归到底' if S.p == 1
                                      else f'`p = {S.p} ≠ 1`，继续二分'),
        'return base': '递归到底，返回 `base = {base}`',
        'res = quick_pow(base, p // 2': '先算一半：`base^{B.p // 2}`（进入新的一层）',
        'res = mul(res, res, mod)': '两个一半相乘 → `base^{p - p % 2}`，`res = {res}`',
        'if p % 2 == 1': lambda S, B, r: (f'`p = {S.p}` 是奇数 → 还要再乘一个 `base`' if S.p % 2 == 1
                                          else f'`p = {S.p}` 是偶数 → 不用再乘'),
        'res = mul(res, base, mod)': '补乘一个 `base` → `base^{p}`，`res = {res}`',
        'return res': '返回 `base^{p}` = `{res}`',
        'return f[1][1] * 2 % mod': '`f[1][1]` 是第 n 项斐波那契；长度 1 有 a、b 两种 → ==乘 2==：`{f[1][1]} × 2` = `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='好字符串数 = 2×斐波那契：递推 + 矩阵快速幂',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['字符串只含 `a`、`b`，满足下列之一就是好字符串：',
                 '① 只有一种字符且长度为奇数；② 拆成两个非空好字符串，且前一个末字符 ≠ 后一个首字符',
                 '给 `n`（最大 `10^15`），求长度为 n 的好字符串数，对 `10^9+7` 取模。本视频：`n = 5` → `10`'],
        quote='f[k] = f[k - 1] + f[k - 2]，可以发现，这就是斐波那契数列的递推式……不过需要特别注意的是，这里的数列的起始项f[0] = 0不变，但是f[1]应该是2而不是1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[k]` 必以一段奇数长度的同字符串结尾：`f[k-1] + f[k-3] + f[k-5] + …`',
              '再减去 `f[k-2]` 的展开，化简成 `f[k] = f[k-1] + f[k-2]`',
              'n 太大，用 `[[0,1],[1,1]]` 的快速幂 `O(log n)` 求第 n 项，最后乘 2'],
        summary=['时间 `O(log n)`，每次乘法只有 2×2 共 8 次乘加',
                 '易错：起始是 `f[1] = 2`（a 和 b），所以结果要 ×2',
                 '每次乘完都取模，避免大数；`p == 0` 时返回单位矩阵',
                 '原文已是 Python 3 可运行写法，`/` 已是 `//`，代码未改动',
                 '同类题：斐波那契型递推 + 矩阵快速幂（如 70 爬楼梯加强版）'],
    ),
)
