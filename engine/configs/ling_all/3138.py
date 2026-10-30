def _col(S, i, v):
    if 'k' not in S:
        return None
    b = i // S['k']
    if 't' in S:
        ok = sorted(S['s'][b * S['k']: (b + 1) * S['k']]) == S['t']
        return 'green' if ok else 'red'
    return 'blue' if b % 2 == 0 else 'cyan'


def _txt(S):
    if 'g' not in S:
        return 't 的每种字母个数必须整除 s 里该字母的个数 → 次数只能是它们的公约数的因子'
    if 'k' not in S:
        return f"各字母个数的 gcd `g = {S['g']}` → `times` 只用从 g 往下试"
    return f"`times = {S['times']}`，每块长 `k = {S['n']} // {S['times']} = {S['k']}`"


CONFIG = dict(
    num=3138, title='同位字符串连接的最小长度', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='字母个数 GCD + 枚举块数',
    tags=[],
    code='''
class Solution:
    def minAnagramLength(self, s: str) -> int:
        n = len(s)
        g = gcd(*Counter(s).values())
        for times in range(g, 1, -1):
            if g % times:
                continue
            k = n // times
            t = sorted(s[:k])
            if all(sorted(s[i - k: i]) == t for i in range(k * 2, n + 1, k)):
                return k
        return n
''',
    call='Solution().minAnagramLength("aabbaabb")',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（按块着色；绿 = 与第一块同位，红 = 不同位）', cell=84, color=_col, h=230),
        dict(type='array', var=lambda S: S.get('t'), label='t = 第一块排序后的字母', cell=70, h=170),
        dict(type='text', fn=_txt, size=28, h=120),
    ],
    watch=['n', 'g', 'times', 'k'],
    captions={
        'n = len': '`n = len(s) = {n}`',
        'g = gcd': lambda S, B, r: f"各字母个数 `{dict(Counter(S.s))}` 的 gcd = =={S.g}==：t 里每种字母的个数必须整除它们，块数 `times` 只能是 g 的因子",
        'for times in range': '从大到小试块数 `times = {times}`：块越多 t 越短，先找到的就是最短',
        'if g % times': lambda S, B, r: (f"`{S.g} % {S.times} = {S.g % S.times}` ≠ 0 → times 不是 g 的因子，==跳过==" if S.g % S.times else f"`{S.g} % {S.times} = 0` → 可能成立，继续检查"),
        'k = n // times': '分成 `times = {times}` 块，每块长 `k = {n} // {times} = {k}`',
        't = sorted': '第一块排序得到 `t = {t}`，当作「字母个数模板」',
        'if all(': lambda S, B, r: (lambda bl: f"其余 {len(bl)} 块排序后是否都等于 `{S.t}`？" + ('都相同 → ==成立==' if all(x == S.t for x in bl) else f"`{''.join(next(x for x in bl if x != S.t))}` 不同 → ==不成立，换下一个 times=="))([sorted(S.s[i - S.k: i]) for i in range(S.k * 2, S.n + 1, S.k)]),
        'return k': '块数 `{times}` 成立，==t 的长度 k = {k}==',
        'return n': '所有可行块数都失败，只能 `t = s` 本身，返回 {ret}',
    },
    cards=dict(
        one_liner='先用 gcd 缩小块数范围，再逐个试：每块排序后都相同就是答案',
        complexity='时间 `O(A·n)`（A 为 n 的因子个数），空间 `O(|Σ|)`',
        problem=['`s` 由某个字符串 `t` 和若干个 `t` 的同位字符串（重排）连接而成',
                 '求 `t` 的最小可能长度；`t` 可以等于 `s`',
                 '示例：`"abba"` → `2`；`"cdef"` → `4`',
                 '演示用 `"aabbaabb"`：试 4 块失败，试 2 块成功 → `4`'],
        quote='所以 times 必须是 6 和 4 的公因数，也就是 g=GCD(6,4)=2 的因子。从大到小枚举 g 的因子，那么方法一中的 k = n/times。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`t` 里每种字母的个数，都得整除 `s` 里该字母的总个数',
              '所以块数 `times` 必是各字母个数的公约数 → 只枚举 `gcd` 的因子',
              '每块排序后相同 = 同位字符串；`times` 越大 `k` 越小，从大往小试'],
        summary=['时间 `O(A·n)`，空间 `O(|Σ|)`',
                 '方法一直接枚举 n 的因子 k，思路一样但枚举更多；写法二用 `Counter` 代替 `sorted`',
                 '易错：`range(g, 1, -1)` 不含 1，次数 1 就是 `t = s`，直接 `return n`',
                 '易错：比较范围是 `range(k*2, n+1, k)`，第一块已作模板'],
    ),
)
