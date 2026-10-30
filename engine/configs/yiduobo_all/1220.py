VOW = 'aeiou'


def _base(S):
    I = S['_inner']
    return I['base'] if 'base' in I else S.get('f')


def _mat(name):
    def g(S):
        v = S['_inner'].get(name)
        return v if isinstance(v, list) else None
    return g


def _tmpfin(S):
    I = S['_inner']
    v = I.get('tmp') if isinstance(I.get('tmp'), list) else I.get('final')
    return v if isinstance(v, list) else None


def _row(S):
    p = S.get('p')
    if S.get('n') is None:
        return ''
    return f"这一层：求 `M^{p if p is not None else S.n - 1}`" if p is not None else ''


def _m(name):
    return lambda S: S[name] if name in S else None


CONFIG = dict(
    num=1220, title='统计元音字母序列的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状态转移矩阵 + 快速幂',
    tags=['动态规划'],
    code='''
class Solution(object):
    def countVowelPermutation(self, n):

        if n == 1:
            return 5

        mod = 10 ** 9 + 7

        f = [[0, 1, 0, 0, 0],
             [1, 0, 1, 0, 0],
             [1, 1, 0, 1, 1],
             [0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0]]

        final = self.quick_pow(f, n - 1, mod)
        res = 0
        for line in final:
            for num in line:
                res += num
                res %= mod
        
        return res
    
    def quick_pow(self, base, n, mod):
        if n == 1:
            return base
        
        tmp = self.quick_pow(base, n // 2, mod)
        l = len(base)
        res = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod

        if n % 2 == 0:
            return res

        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
''',
    call='Solution().countVowelPermutation(4)',
    expect=35,
    skip=[10, 11, 12, 13, 'for i in range(l)', 'for j in range(l)', 'for k in range(l)', 'res[i][j] +=', 'res[i][j] %=',
          'tmp[i][j] +=', 'tmp[i][j] %=', 'for line in final', 'for num in line', 'res += num', 'res %= mod', 'l = len(base)'],
    views=[
        dict(type='calls', h=120, hide=('base', 'mod')),
        dict(type='table', var=_base, label='base（= M，行 = 前一个字母，列 = 后一个字母）', h=225, cell=70,
             rows=list(VOW), cols=list(VOW)),
        dict(type='table', var=_tmpfin, label='tmp（递归返回的 M^(n//2)；回到主函数后是 final = M^(n-1)）', h=225, cell=70,
             rows=list(VOW), cols=list(VOW)),
        dict(type='table', var=_mat('res'), label='res = tmp × tmp（平方）', h=225, cell=70,
             rows=list(VOW), cols=list(VOW)),
    ],
    watch=[('n', lambda S: S['_inner'].get('n'), 'blue'), ('mod', 'mod')],
    captions={
        4: '`n = {n}`，不是 1，继续',
        7: '结果可能很大，随时对 `{mod}` 取模',
        9: lambda S, B, r: ('转移矩阵：`f[i][j] = 1` 表示字母 i 后面==可以接==字母 j（行列都是 a e i o u）'
                            if 'f' not in S else '建好了：例如第 e 行 `[1,0,1,0,0]`，e 后面只能接 a、i'),
        15: lambda S, B, r: (f'`final = M^(n-1) = M^{B.n - 1}`：长度 n 的串 = 从长度 1 转移 n−1 次，调用快速幂'),
        16: '`res` 累加 `final` 全部 25 个元素（初始 5 个字母各 1 个）并取模',
        25: lambda S, B, r: (f'`n = {S["n"]}`：不是 1，要继续拆' if S['n'] != 1 else '`n = 1`：递归到底，`M^1` 就是 ==M 本身=='),
        26: '返回 `base`（即 M）',
        28: lambda S, B, r: (f'`n = {B.n}`：先递归求一半 `M^{B.n // 2}`' if 'tmp' not in S
                             else f'递归回来：`tmp` = ==M^{S["n"] // 2}=='),
        30: '`res = tmp × tmp`：三重循环做矩阵乘法并逐项取模，得到 ==M^{n // 2 * 2}==',
        37: lambda S, B, r: (f'`n = {S["n"]}` 是偶数：`tmp²` 正好是 `M^{S["n"]}`，直接返回' if S['n'] % 2 == 0
                             else f'`n = {S["n"]}` 是奇数：平方只得到 `M^{S["n"] - 1}`，还差一个 M'),
        38: '偶数：返回 `res`',
        40: '奇数：再算一次 `res × base`，补上差的那个 M',
        47: '返回 `M^{n}`',
        22: '答案 =={ret}==：`final` 所有元素之和（取模）',
    },
    cards=dict(
        one_liner='转移关系固定 → 写成矩阵 → 快速幂',
        complexity='时间 `O(5^3 · log n)`，空间 `O(log n)`（递归栈）',
        problem=['由小写元音组成的长 `n` 的字符串，规则：a 后只能接 e；e 后只能接 a、i；i 后不能接 i；o 后只能接 i、u；u 后只能接 a',
                 '求合法字符串个数，对 `10^9+7` 取模',
                 '示例：`n = 1` → `5`；`n = 2` → `10`；本视频 `n = 4` → `35`'],
        quote='这里有一个小技巧。当前后的值矩阵的元素系数都是1时，那么可以将每一位对应的转移方程的系数竖着拼起来，就可以得到矩阵M。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j][x]` = 长 j 且最后一个字母是 x 的串数；每个转移系数都是 1',
              '把转移写成 5×5 的矩阵 M，`[a,e,i,o,u] × M` 就走一步',
              '初始 5 个字母各 1 个，所以答案 = `M^(n-1)` 所有元素之和；用快速幂加速'],
        summary=['时间 `O(log n)`（矩阵阶数是常数 5），空间 `O(log n)` 递归栈',
                 '易错：幂是 `n - 1` 不是 `n`；`n = 1` 要单独返回 5',
                 '`quick_pow` 偶数用平方；奇数平方后==再乘一次 base==',
                 '原文为 Python 2 写法，`quick_pow` 里的 `n / 2` 已改为 `n // 2`',
                 '本视频用 n=4 演示（`M^3`：先 `M^1`，平方得 `M^2`，奇数再乘 M）'],
    ),
)
