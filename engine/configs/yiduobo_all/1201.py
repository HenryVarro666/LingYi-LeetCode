def _ugly(S):
    x = S.get('mid')
    if x is None:
        x = S.get('labc')
    if x is None:
        return []
    return [v for v in range(1, x + 1) if v % S['a'] == 0 or v % S['b'] == 0 or v % S['c'] == 0]


def _color(S, i, v):
    if 'mid' in S and i + 1 == S['n']:
        return 'green'
    return 'blue' if 'mid' in S else None


def _cntf(S, x):
    a, b, c = S['a'], S['b'], S['c']
    return x // a + x // b + x // c - x // S['lab'] - x // S['lac'] - x // S['lbc']


def _txt(S):
    if 'labc' not in S:
        return f"第 `{S['n']}` 个能被 `{S['a']}`、`{S['b']}` 或 `{S['c']}` 整除的数"
    if 'k' not in S:
        return f"周期 `labc = {S['labc']}`：三者最小公倍数"
    if 'mid' not in S:
        return f"每 `labc = {S['labc']}` 个数里有 `k = {S['k']}` 个丑数；还要找周期里第 `n = {S['n']}` 个"
    m = S['mid']
    return (f"`mid = {m}`：`{m//S['a']}+{m//S['b']}+{m//S['c']}−{m//S['lab']}−{m//S['lac']}−{m//S['lbc']}` = =={_cntf(S, m)}== 个丑数，"
            f"要 `≥ n = {S['n']}`")


CONFIG = dict(
    num=1201, title='丑数 III', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='容斥原理 + 二分答案',
    tags=[],
    code='''
class Solution(object):
    def nthUglyNumber(self, n, a, b, c):

        lab = a // self.gcd(a, b) * b
        lac = a // self.gcd(a, c) * c
        lbc = b // self.gcd(b, c) * c
        labc = lab // self.gcd(lab, lac) * lac

        k = labc // a + labc // b + labc // c - labc // lab - labc // lac - labc // lbc + 1
        p = n // k
        n %= k
        offset = labc * p
        if n == 0:
            return offset
        l = min(a, b, c)
        r = labc
        while l < r:
            mid = (l + r) >> 1
            k = mid // a + mid // b + mid // c - mid // lab - mid // lac - mid // lbc
            if k < n:
                l = mid + 1
            else:
                r = mid
        
        return offset + l

    
    def gcd(self, x, y):
        if y == 0:
            return x
        return self.gcd(y, x % y)
''',
    call='Solution().nthUglyNumber(7, 2, 3, 5)',
    expect=9,
    skip=['if y == 0', 'return x', 'return self.gcd(y'],
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=_ugly, label='1..mid 中的丑数（蓝 = 已数入）', color=_color, h=260),
    ],
    watch=['labc', 'k', 'n', 'l', 'r', 'mid', ('offset', 'offset', 'green')],
    captions={
        'lab = a': '`lab`：`a` 和 `b` 的最小公倍数 = `a // gcd(a, b) * b`（先除后乘，调用 `gcd`）',
        'lac = a': '`lac`：`a` 和 `c` 的最小公倍数',
        'lbc = b': '`lbc`：`b` 和 `c` 的最小公倍数',
        'labc = lab': '`labc`：三者最小公倍数，每过 `labc` 个数，整除情况完全重复',
        'k = labc // a': '容斥：`{labc//a}+{labc//b}+{labc//c} − {labc//lab} − {labc//lac} − {labc//lbc} + 1` = =={k}== 个丑数 / 周期（`labc` 被减了三次，要加回 1）',
        'p = n // k': '前面有 `p = n // k = {p}` 个完整周期',
        'n %= k': '周期内还要找第 `n = {n}` 个',
        'offset = ': '整周期占掉的数值 `offset = labc × p = {offset}`',
        'if n == 0': lambda S, B, r: ('`n == 0`：正好是某个周期的最后一个丑数 `labc` 的倍数 → 直接返回 `offset`' if S.n == 0
                                      else f'`n = {S.n}` ≠ 0：还要在周期内二分'),
        'l = min': '下界：最小的丑数 `min(a,b,c) = {l}`',
        'r = labc': '上界：周期末 `labc = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l}` < `r = {S.r}`：答案在 `[l, r]` → 继续' if S.l < S.r else f'`l = r = {S.l}`：定位完成'),
        'mid = (': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'k = mid': '`≤ {mid}` 的丑数：容斥 `{mid//a}+{mid//b}+{mid//c}−{mid//lab}−{mid//lac}−{mid//lbc}` = =={k}==（此处 `mid < labc`，不用加 1）',
        'if k < n': lambda S, B, r: (f'`k = {S.k}` < `n = {S.n}`：丑数不够 → 答案在右边' if S.k < S.n else f'`k = {S.k}` ≥ `n = {S.n}`：够了 → 答案 ≤ mid'),
        'l = mid + 1': '`mid` 排除：`l = mid + 1 = {l}`',
        'r = mid': '`mid` 可能就是答案：`r = mid = {r}`',
        'return offset + l': '`offset + l` = `{offset} + {l}` = =={ret}=='
    },
    cards=dict(
        one_liner='容斥算出一个周期里的丑数个数，再在周期内二分',
        complexity='时间 `O(log labc)`，空间 `O(log)`（递归 gcd）',
        problem=['能被 `a`、`b` 或 `c` 整除的正整数是丑数，求第 `n` 个丑数',
                 '示例：`n=3, a=2, b=3, c=5` → `4`',
                 '本视频：`n=7, a=2, b=3, c=5` → `9`（2,3,4,5,6,8,9）'],
        quote='这样计算的理由是在计算可以被a整除和可以被b整除的数时，可以同时被a和b整除的数被计算了两次。……但是，这其中有个特例就是labc，其被计算了三次，也被减去了三次，因此最后需要加上一个1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`labc` 是三者最小公倍数：每 `labc` 个数，丑数的分布完全重复',
              '一个周期里的个数用容斥：加单个，减两两公倍数，周期末 `labc` 本身再加回 1',
              '`p = n // k` 个整周期直接跳过，剩下 `n % k` 个在 `[min, labc)` 里二分'],
        summary=['时间 `O(log(labc))`，空间 `O(log)`（`gcd` 递归）',
                 '周期内二分时 `mid < labc`，容斥式==不加 1==',
                 '`n % k == 0` 时答案恰为 `offset`，要提前返回',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '同类题 878 神奇数字；和 878 一样：先 lcm 求周期，再计数'],
    ),
)
