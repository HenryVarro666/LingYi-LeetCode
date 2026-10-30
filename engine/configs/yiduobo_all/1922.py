def _fmt(S):
    inner = S.get('_inner', {})
    if 'p' in inner and 'tmp' in inner:
        return f"`quickPow(20, {inner['p']})`：`tmp = {inner['tmp']}`"
    if 'p' in inner:
        return f"`quickPow(20, {inner['p']})`：还在往下拆 p"
    if 'res' in S:
        return f"`20^{S['n'] // 2}` = {S['res']}"
    return f"n = {S['n']}：每两位 20 种，共 {S['n'] // 2} 对"


CONFIG = dict(
    num=1922, title='统计好数字的数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='每两位 20 种 · 递归快速幂',
    tags=['灵神题单·数学算法', '难度分 1675'],
    code='''
class Solution(object):
    def countGoodNumbers(self, n):

        if n == 1:
            return 5

        mod = 10 ** 9 + 7

        res = self.quickPow(20, n // 2, mod)
        if n & 1:
            res = res * 5 % mod
        
        return res
    
    def quickPow(self, base, p, mod):
        if p == 1:
            return base
        
        tmp = self.quickPow(base, p // 2, mod)
        tmp = tmp * tmp % mod
        if p & 1:
            tmp = tmp * base % mod
        
        return tmp
''',
    call='Solution().countGoodNumbers(11)',
    expect=16000000,
    views=[
        dict(type='text', fn=_fmt, size=34, h=90),
        dict(type='calls', h=330),
    ],
    watch=['n', 'mod', ('res', 'res', 'green')],
    captions={
        'if n == 1': lambda S, B, r: ('`n = 1`：只有偶数下标 0 一位，5 种，直接返回 5' if S.n == 1 else f'`n = {S.n} != 1`：不是只有一位，走正常流程（n 为 1 时特判返回 5）'),
        'mod = ': '答案取模：`mod = 10^9 + 7`',
        'res = self.quickPow': '每两位（偶数位 5 种 × 奇数位 4 种）= 20 种，`n // 2 = {n // 2}` 对 → 算 `20^{n // 2}`',
        'if n & 1': lambda S, B, r: ('`n & 1 = 1`：n 是奇数，最后落单的一位是偶数位 → 还要再乘 5' if S.n & 1 else '`n & 1 = 0`：n 是偶数，刚好配成整对，不用再乘'),
        'res = res * 5': '`res = res × 5 % mod = {res}`',
        'return res': '答案 ==`{res}`==',
        'if p == 1': lambda S, B, r: (f'`p = {S.p}`：指数降到 1，递归出口，返回 `base = {S.base}`' if S.p == 1 else f'`p = {S.p} != 1`，继续往下拆'),
        'return base': '`20^1 = {base}`，开始往回算',
        'tmp = self.quickPow': '进入下一层，指数折半：`p // 2 = {B.p // 2}`',
        'tmp = tmp * tmp': '半个指数的结果平方：`tmp = tmp × tmp % mod = {tmp}`',
        'if p & 1': lambda S, B, r: (f'`p = {S.p}` 是奇数：平方后少了一个 base，还要补乘一次' if S.p & 1 else f'`p = {S.p}` 是偶数：平方正好够，不用补'),
        'tmp = tmp * base': '补乘一个 `base = {base}`：`tmp = {tmp}`',
        'return tmp': '这一层返回 `20^{p} = {tmp}`',
    },
    cards=dict(
        one_liner='相邻两位组成一对，一对 20 种；n 为奇数再乘 5',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['偶数下标要填偶数，奇数下标要填质数 `2 3 5 7`，可以有前导 0',
                 '求长为 `n` 的好数字串个数，对 `10^9+7` 取模',
                 '示例：`n = 4` → `400`；本视频 `n = 11` → `16000000`'],
        quote='每两位可以提供20种可能性，于是最终一共有20^(n / 2)种可能性。另外，若n位奇数，那么答案还需要再乘以5。',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数位 5 种、奇数位 4 种，==每两位凑成 20 种==',
              '`n` 位共 `n // 2` 对，奇数时多出一个偶数位，再乘 5',
              '`n` 高达 10^15，用递归快速幂：`p` 折半，平方，奇数补乘 `base`'],
        summary=['时间 `O(log n)`，递归深度约 `log n`',
                 '`n == 1` 要单独返回 5：此时 `n // 2 = 0`，`quickPow` 的 `p == 1` 出口接不住 0',
                 '每次乘法都取模，`p` 为奇数时别忘了补乘 `base`',
                 '原文为 Python 2 写法，`/` 为整数除法，已改为 `//`',
                 '对比灵神：灵神直接 `pow(5, a) * pow(4, b)`，这里是合成 20 再快速幂'],
    ),
)
