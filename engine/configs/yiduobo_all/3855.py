CONFIG = dict(
    num=3855, title='给定范围内 K 位数字之和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按位求和 + 快速幂 + 费马小定理求逆元',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def sumOfNumbers(self, l, r, k):
        
        mod = 10 ** 9 + 7

        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res

        n = r - l + 1
        s = n * (l + r) // 2
        c = quick_pow(n, k - 1)
        all9 = (quick_pow(10, k) - 1 + mod) % mod
        rev9 = quick_pow(9, mod - 2)
        all1 = all9 * rev9
        
        return s * all1 % mod * c % mod
''',
    call='Solution().sumOfNumbers(1, 2, 3)',
    expect=1332,
    views=[
        dict(type='text', size=26, fn=lambda S: ('把每一位的贡献拆开：个位 / 十位 / 百位 …' if 'n' not in S else
             f"`n = {S['n']}`" + (f"，`s = n·(l+r)/2 = {S['s']}`" if 's' in S else '') +
             (f"，`c = n^(k-1) = {S['c']}`" if 'c' in S else '') + (f"，`all9 = 10^k − 1 = {S['all9']}`" if 'all9' in S else '') +
             (f"，`rev9 = 9^(mod−2)`" if 'rev9' in S else ''))),
        dict(type='calls', h=400, hide=()),
        dict(type='text', size=26, fn=lambda S: '答案 = `全1数 × s × c`，全1数 = `all9 × rev9`（111…1 共 k 个）' if 'all1' in S else '快速幂：`p` 每次减半，递归深度 `log p`'),
    ],
    watch=['l', 'r', 'k', ('n', 'n', 'blue'), ('s', 's', 'green'), ('c', 'c', 'cyan'), ('all9', 'all9', 'orange')],
    max_steps=60,
    captions={
        'mod = ': '答案对 `10^9+7` 取模',
        'def quick_pow': '定义快速幂 `quick_pow(base, p)`：算 `base^p mod mod`',
        'if p == 0': '`p = {p}` → 是 0 吗？{"是，返回 1" if p == 0 else "不是"}',
        'if p == 1': '`p = {p}` → 是 1 吗？{"是，返回 base" if p == 1 else "不是，继续折半"}',
        'return 1': '`base^0 = 1`',
        'return base': '`base^1 = {base}`',
        'res = quick_pow(base, p // 2)': '`p = {B.p}`，先递归算一半：`quick_pow(base, {B.p} // 2)`，即 `p = {B.p // 2}`',
        'res = res * res': '一半的平方：`res = res × res % mod` = =={res}==',
        'if p & 1': '`p = {p}` 是{"奇数" if p & 1 else "偶数"}',
        'res = res * base': 'p 是奇数，再补乘一个 `base`：=={res}==',
        'return res': '`quick_pow` 返回 `{res}`',
        'n = r - l + 1': '`n = r - l + 1 = {n}`：每一位有 n 个数字可选',
        's = n * (l + r) // 2': '某一位上，`x` 取 `l..r`，每个 x 对应 `n^(k-1)` 个数：数字之和 `s = n·(l+r)/2 = {s}`（先乘整除，保证整除）',
        'c = quick_pow(n, k - 1)': '`c = n^(k-1) mod mod = {c}`',
        'all9 = ': '`111…1 = (10^k − 1) / 9`，先算分子：`all9 = 10^k − 1 = {all9}`',
        'rev9 = ': '除以 9 要用逆元：费马小定理 `9^(mod−2)` 就是 9 的逆元 `rev9`',
        'all1 = ': '`all1 = all9 × rev9`（模意义下的 111…1，共 k 个 1）',
        'return s': '最后：`s × all1 × c` 再取模 = =={ret}==',
    },
    cards=dict(
        one_liner='先算每一位上的和，再把 111…1 用快速幂和逆元算出来',
        complexity='时间 `O(log k)`，空间 `O(log k)`（递归深度）',
        problem=['从 `[l, r]` 里为 `k` 位数的每一位独立选数，含 0 则允许前导 0',
                 '求所有这样的数之和，对 `10^9+7` 取模，`k` 可达 `10^9`',
                 '本视频演示：`l=1, r=2, k=3` → `1332`'],
        quote='这些数的个位都是x，因此累加起来就是x * n^(k - 1)。……最终结果为(1 + 10 + 100 + ... + 10^(k - 1)) * s * n^(k - 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看个位：`x` 在 `l..r` 之间，以 `x` 为个位的数有 `n^(k-1)` 个，所有个位之和 `s·n^(k-1)`，`s = (l+r)·n/2`',
              '十位同理，只是再乘 10，所以总和 = `(1+10+…+10^(k-1)) × s × n^(k-1)`',
              '括号里是 k 个 1：看成 `(10^k−1)/9`，用快速幂 + 9 的逆元（费马小定理）算'],
        summary=['时间 `O(log k)`，空间 `O(log k)`',
                 '易错点：`all9 = (10^k − 1 + mod) % mod`，加 `mod` 防止减出负数',
                 '`s = n * (l + r) // 2` 先乘后除，保证整除',
                 '原文已写 `//`，无需修改',
                 '对比灵神：灵神用内置 `pow` 和 `pow(18,-1,MOD)`，yiduobo 手写递归快速幂和费马逆元'],
    ),
)
