CONFIG = dict(
    num=3700, title='锯齿形数组的总数 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='奇偶两个转移矩阵 × 快速幂',
    tags=['难度分 2435'],
    code='''
class Solution(object):
    def zigZagArrays(self, n, l, r):
        
        r -= l
        base1 = [[0] * (r + 1) for _ in range(r + 1)]
        base2 = [[0] * (r + 1) for _ in range(r + 1)]
        for i in range(r + 1):
            for j in range(i + 1, r + 1):
                base1[i][j] = 1
            for j in range(i):
                base2[i][j] = 1

        mod = 10 ** 9 + 7

        def mul(a, b):
            m = len(a)
            n = len(a[0])
            t = len(b[0])
            c = [[0] * t for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(t):
                        c[i][k] = (c[i][k] + a[i][j] * b[j][k]) % mod
            return c
        
        merge = mul(base1, base2)

        def quick_pow(base, p):
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = mul(res, res)
            if p % 2 == 1:
                res = mul(res, base)
            
            return res
        
        ori = [[1] * (r + 1)]
        ori = mul(ori, quick_pow(merge, (n - 1) // 2))
        if n % 2 == 0:
            ori = mul(ori, base1)
        return sum(ori[0]) * 2 % mod
''',
    call='Solution().zigZagArrays(6, 1, 4)',
    expect=314,
    skip=['for i in range(r + 1)', 'for j in range(i', 'base1[i][j] = 1', 'base2[i][j] = 1', 'm = len(a)', 'n = len(a[0])', 't = len(b[0])',
          'c = [[0] * t', 'for i in range(m)', 'for j in range(n)', 'for k in range(t)', 'c[i][k] =', 'return c'],
    max_steps=60,
    views=[
        dict(type='text', size=22, h=100, fn=lambda S: '`f[n] = ori × (base1 × base2)^k`，答案 = `sum(f[n]) × 2`'),
        dict(type='table', var='base1', label='base1：右上三角为 1（奇数→偶数位，下一个更大）', h=240, cell=56),
        dict(type='table', var='base2', label='base2：左下三角为 1（下一个更小）', h=240, cell=56),
        dict(type='table', var=lambda S: S.get('ori') or [[0] * 4], label='ori（行向量，初值全 1 = f[1]）', h=130, cell=56),
    ],
    watch=[('n', 'n', 'blue'), ('r', 'r', 'pink'), ('ori', 'ori', 'green')],
    captions={
        'r -= l': '把取值平移到 `[0, r - l]`，之后 `r = {r}`，共 `r + 1` 个值',
        'base1 = ': '`base1`：`(r+1)×(r+1)`，右上三角（`j > i`）置 1，对应偶数位的转移',
        'base2 = ': '`base2`：左下三角（`j < i`）置 1，对应奇数位的转移，两者互为转置',
        'mod = ': '答案对 `10^9 + 7` 取模',
        'merge = mul': '`merge = base1 × base2`：奇偶两步合成一步。==矩阵乘法没有交换律，顺序不能换==',
        'if p == 1': lambda S, B, r: ('`p = 1`：递归到底，`merge^1` 就是它自己' if S.p == 1 else f'`p = {S.p}`：继续对半拆'),
        'return base': '返回 `merge`',
        'res = quick_pow': '先递归求 `merge^(p//2)`',
        'res = mul(res, res)': '平方：得到 `merge^(2·(p//2))`',
        'if p % 2 == 1': lambda S, B, r: ('`p` 是奇数 → 还差一个 `merge`' if S.p % 2 else '`p` 是偶数 → 已经够了'),
        'res = mul(res, base)': '补乘一个 `merge`',
        'return res': '返回 `merge^p`',
        'ori = [[1]': '`ori = f[1]`：长度为 1 的数组，以每个值结尾各 1 种',
        'ori = mul(ori, quick_pow': '`ori × merge^((n-1)//2)`：每个 `merge` 走两步，一共走 `2·((n-1)//2)` 步',
        'if n % 2 == 0': lambda S, B, r: ('`n` 是偶数 → 还差一步，再乘一个 `base1`' if S.n % 2 == 0 else '`n` 是奇数 → 步数刚好'),
        'ori = mul(ori, base1)': '补上最后一步：`ori × base1`',
        'return sum(ori[0])': '`sum(ori[0])` = 一种起伏形态（^ 形）的个数，另一种（v 形）对称，所以 ×2，答案 = =={ret}==',
    },
    cards=dict(
        one_liner='奇偶位转移矩阵不同，先合并成一个再快速幂',
        complexity='时间 `O(m^3 log n)`（m = r-l+1），空间 `O(m^2)`',
        problem=['长为 `n`、取值 `[l, r]`，相邻不等且任意三个连续元素不单调的数组个数，对 `10^9+7` 取模',
                 '`n` 最大 `10^9`，`l, r` 在 1 到 75',
                 '本视频：`n = 6, l = 1, r = 4` → `314`'],
        quote='需要注意的是，矩阵乘法满足结合律，但是不满足交换律，因此在这里还需要先计算base1 \\* base2的结果，记为merge。',
        quote_src='—— yiduobo 题解原文',
        idea=['只算 `^` 形：`f[index][v]` 为长度 index、以 v 结尾的个数，奇偶位的转移不同',
              '偶数位 `f = 前一位更小的和`（base1，右上三角），奇数位相反（base2，左下三角）',
              '`ori × merge^((n-1)//2)`，`n` 为偶数再补一个 `base1`，最后求和 ×2'],
        summary=['时间 `O(m^3 log n)`，空间 `O(m^2)`',
                 '易错：先 `merge = base1 × base2` 再取幂，顺序不能反；`n` 偶数要多乘 `base1`',
                 '`quick_pow` 里 `p == 1` 就返回，所以幂不能为 0，`n >= 3` 保证了这点',
                 '原文本身是 Python 3 兼容的写法，代码没有改动',
                 '对比灵神：灵神利用对称性只用一个 `k×k` 矩阵，yiduobo 用奇偶两个矩阵']
    ),
)
