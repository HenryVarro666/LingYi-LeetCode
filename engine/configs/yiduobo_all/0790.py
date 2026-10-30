CONFIG = dict(
    num=790, title='多米诺和托米诺平铺', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三状态 DP → 4×4 矩阵快速幂',
    tags=[],
    code='''
class Solution(object):
    def numTilings(self, N):

        if N == 1:
            return 1
            
        base = [[0, 1, 1, 1],
                [1, 1, 0, 0],
                [0, 1, 0, 1],
                [0 ,1, 1, 0]]
        
        mod = (10 ** 9 + 7)

        tmp = self.q_pow(N - 1, base, mod)
        return (tmp[0][1] + tmp[1][1]) % mod
        

    def q_pow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        tmp = self.q_pow(n // 2, base, mod)
        ret = []
        for i in range(4):
            ret.append([])
            for j in range(4):
                ret[-1].append(0)
                for k in range(4):
                    ret[-1][-1] += tmp[i][k] * tmp[k][j]
                    ret[-1][-1] %= mod

        if n & 1:
            tmp = []
            for i in range(4):
                tmp.append([])
                for j in range(4):
                    tmp[-1].append(0)
                    for k in range(4):
                        tmp[-1][-1] += ret[i][k] * base[k][j]
                        tmp[-1][-1] %= mod
            return tmp
        
        return ret
''',
    call='Solution().numTilings(7)',
    expect=117,
    skip=['for i in range(4)', 'for j in range(4)', 'for k in range(4)', 'ret.append', 'ret[-1]', 'tmp.append', 'tmp[-1]', 'base = [[0', '[1, 1, 0, 0],', '[0, 1, 0, 1],'],
    max_steps=60,
    views=[
        dict(type='text', size=22, h=90, fn=lambda S: '`X[N] = X[1] × A^(N-1)`，`T = A^(N-1)`，答案 = `T[0][1] + T[1][1]`'),
        dict(type='table', var='base', label='base = 转移矩阵 A', h=290, cell=66),
        dict(type='table', var=lambda S: S.get('tmp') if S.get('tmp') and len(S['tmp']) == 4 and all(len(r) == 4 for r in S['tmp']) else [[0] * 4] * 4,
             label='tmp = 上一层返回的 A^(n//2)（回溯时最终是 A^(N-1)）', h=290, cell=66),
    ],
    watch=[('N', 'N', 'blue'), ('n', 'n', 'pink'), ('n & 1', 'n & 1', 'green')],
    captions={
        'if N == 1': '`N = 1` 时只有一种（一个竖放多米诺），直接返回 1',
        '[0 ,1, 1, 0]]': '转移矩阵 `A`，由 `f/g/h` 的三个转移方程解出',
        'mod = ': '答案对 `10^9 + 7` 取模',
        'tmp = self.q_pow(N - 1': '`T = A^(N - 1)`，用递归快速幂求',
        'return (tmp[0][1]': '`X[N][1] = T[0][1] + T[1][1]` = =={ret}==',
        'if n == 1': lambda S, B, r: ('`n = 1`：递归到底，`A^1` 就是 `base` 本身，返回' if S.n == 1 else f'`n = {S.n}`：还没到 1，继续对半拆'),
        'return base[:]': '递归边界：返回 `A` 的拷贝',
        'tmp = self.q_pow(n // 2': '先递归求 `A^(n//2)`，参数是 `n // 2`',
        'ret = []': '`ret = tmp × tmp`（4×4 矩阵相乘，每个元素边乘边取模）= `A^(2·(n//2))`',
        'if n & 1': lambda S, B, r: (f'`n = {S.n}` 是奇数 → 平方后还差一个 `A`，再乘一次 `base`' if S.n & 1
                                     else f'`n = {S.n}` 是偶数 → 平方刚好，不用再乘'),
        'tmp = []': '奇数时：`tmp = ret × base`，补上少乘的那个 `A`',
        'return tmp': '返回 `A^{n}`',
        'return ret': '返回 `A^{n}`',
    },
    cards=dict(
        one_liner='按列划分三种状态，转移写成 4×4 矩阵再快速幂',
        complexity='时间 `O(m^3 log N)`（m=4），空间 `O(log N)`',
        problem=['用 `2×1` 多米诺和 L 形托米诺铺满 `2×N`，求方案数（对 `10^9+7` 取模）',
                 '示例：`N = 3` → `5`，`N = 1` → `1`',
                 '本视频：`N = 7` → `117`'],
        quote='如果按列来划分状态，那么每一列可能出现的合法状态有三种，分别是该列填满，该列覆盖了第1行的格子，以及该列覆盖了第2行的格子。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f/g/h` 分别是「列填满 / 只盖上格 / 只盖下格」的方案数',
              '`f[i] = f[i-1] + f[i-2] + g[i-1] + h[i-1]`，`h[i] = f[i-2] + g[i-1]`，`g` 对称',
              '把 `[f[i-2], f[i-1], g[i-1], h[i-1]]` 当行向量乘 4×4 的 `A`，`A^(N-1)` 用递归快速幂'],
        summary=['时间 `O(log N)`（矩阵大小固定为 4），空间 `O(log N)` 递归栈',
                 '易错：矩阵乘法不满足交换律，奇数时是 `ret × base`，顺序别乱',
                 '`N == 1` 要单独返回，否则 `q_pow(0)` 会无限递归',
                 '原文为 Python 2 写法，`q_pow` 里的 `n / 2` 已改为 `n // 2`',
                 '对比灵神：灵神把三项合并成 `f[i]=2f[i-1]+f[i-3]`，只要 3×3 矩阵'],
    ),
)
