def _tars(S):
    t = S.get('tar')
    return t if t is not None else ''


CONFIG = dict(
    num=1864, title='构成交替字符串需要的最小交换次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='枚举两种目标串，数错位的 1（Go 原文转写）',
    tags=['灵神题单', '贪心算法', '难度分 1601'],
    code='''
class Solution:
    def minSwaps(self, s: str) -> int:
        ans = int(1e9)
        def f(tar: str) -> None:
            nonlocal ans
            if tar.count("0") != s.count("0"):
                return
            c = 0
            for i in range(len(s)):
                if s[i] == '1' and tar[i] == '0':
                    c += 1
            if c < ans:
                ans = c
        n = len(s)
        f(("10" * n)[:n])
        f(("01" * n)[:n])
        if ans == int(1e9):
            return -1
        return ans
''',
    call='Solution().minSwaps("111000")',
    expect=1,
    views=[
        dict(type='string', var='s', label='s（当前字符串）',
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('red' if (v == '1' and 'tar' in S and S['tar'][i] == '0' and 'c' in S and 'i' in S and i <= S['i']) else None), h=170),
        dict(type='string', var=_tars, label='tar（目标交替串）', index=False, h=150),
        dict(type='text', fn=lambda S: f"和目标串 `{S['tar']}` 比：s 里是 1、目标是 0 的位置共 ==%d== 个（红色）" % S['c'] if 'c' in S and 'tar' in S else '最终串只可能是 `1010…` 或 `0101…`', size=30),
    ],
    watch=['n', 'c', ('ans', 'ans', 'green')],
    captions={
        'ans = int(1e9)': '`ans` 先设成一个很大的数：后面用它判断是否有可行目标',
        'if tar.count': lambda S, B, ret: (f'目标串里 0 的个数 `{S.tar.count("0")}`，s 里 0 的个数 `{S.s.count("0")}`：' + ('==相等==，换位置能凑出它' if S.tar.count("0") == S.s.count("0") else '==不等==，凑不出，直接返回')),
        'c = 0': '`c` 统计「s 是 1、目标是 0」的位置：这些位置要和别处的 0 交换',
        'if s[i] == ': lambda S, B, ret: (f'位置 {S.i}：`s[{S.i}] = {S.s[S.i]}`，`tar[{S.i}] = {S.tar[S.i]}` → ' + ('==错位的 1=='  if (S.s[S.i] == '1' and S.tar[S.i] == '0') else '不用动')),
        'c += 1': '多一个错位的 1：`c` = {c}。每次交换能同时修好一个错位的 1 和一个错位的 0',
        'if c < ans': '`c = {c}` 与当前最小 `{ans}` 比较',
        'ans = c': '更新答案：`ans` = {ans}',
        'f(("10"': '先试目标 `1010…`',
        'f(("01"': '再试目标 `0101…`',
        'if ans == int': lambda S, B, ret: ('`ans` 还是初始值 → 两个目标都凑不出，返回 `-1`' if S.ans == int(1e9) else f'`ans` = {S.ans}，至少有一个目标可行'),
        'return ans': '最少交换 `{ans}` 次',
    },
    skip=['n = len(s)', 'def f', 'nonlocal'],
    cards=dict(
        one_liner='最终串只有两种，各数一下错位的 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，任意两个字符可交换，求变成交替串的最少交换次数，不行返回 `-1`',
                 '示例：`"111000"` → `1`；`"1110"` → `-1`'],
        quote='最终得到的字符串一定是 1010⋯ 或者 0101⋯，直接比较 s 与这两个字符串的不同值即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先看 0 的个数：和目标串不同就不可能，直接跳过',
              '可行时，s 与目标有 `c` 个位置是「1 要变 0」，同样有 `c` 个「0 要变 1」',
              '一次交换修好一对，所以答案就是 `c`；两个目标取较小'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(n)`（构造目标串）',
                 '易错：必须先比较 0 的个数，不相等的目标要排除',
                 '两个目标都不可行时返回 `-1`'],
    ),
)
