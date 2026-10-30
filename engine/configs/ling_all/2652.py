_M = lambda S: S['_inner'].get('m')


def _mult(S):
    m = _M(S)
    if not m:
        return '容斥：`s(3)+s(5)+s(7) − s(15)−s(21)−s(35) + s(105)`'
    n = S['n']
    k = n // m
    ms = [m * i for i in range(1, k + 1)]
    body = '+'.join(map(str, ms)) if ms else '（没有倍数）'
    sign = '加' if m in (3, 5, 7, 105) else '减'
    return f'`s({m})` = {body} = =={n // m * (n // m + 1) // 2 * m}==　（本项要{sign}）'


CONFIG = dict(
    num=2652, title='倍数求和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='容斥原理 + 等差数列求和',
    tags=[],
    code='''
class Solution:
    def sumOfMultiples(self, n: int) -> int:
        def s(m: int) -> int:
            return n // m * (n // m + 1) // 2 * m
        return s(3) + s(5) + s(7) - s(15) - s(21) - s(35) + s(105)
''',
    call='Solution().sumOfMultiples(16)',
    expect=81,
    views=[
        dict(type='text', fn=_mult, size=26, h=70),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='1..n（黄 = 当前 m 的倍数）', cell=60, h=190, index=False,
             color=lambda S, i, v: 'yellow' if _M(S) and v % _M(S) == 0 else None),
    ],
    watch=['n', ('m', _M, 'yellow')],
    captions={
        'def s': '先定义 `s(m)`：[1, n] 里 `m` 的所有倍数之和',
        'return n // m': lambda S, B, ret: (f'`m = {S.m}`：倍数个数 `k = n // m = {S.n // S.m}`，和 = `k(k+1)/2 × m` = =={ret}==，这一项要' + ('加' if S.m in (3, 5, 7, 105) else '减')),
        'return s(3)': lambda S, B, ret: (f'三个质数各算一次，重叠的 15、21、35 倍数被多算了 → 减掉；105 的倍数被减过头 → 补回。结果 =={ret}=='
                                          if ret is not None else '按容斥原理逐项计算 `s(3)+s(5)+s(7)-s(15)-s(21)-s(35)+s(105)`'),
    },
    max_steps=60,
    cards=dict(
        result='81 = 45 + 30 + 21 − 15 − 0 − 0 + 0',
        one_liner='倍数之和用等差数列，重叠部分用容斥原理',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['求 `[1, n]` 内能被 `3`、`5`、`7` 之一整除的所有整数之和',
                 '示例：`n = 10` → `40`（3+5+6+7+9+10）',
                 '本视频取 `n = 16`，答案 `81`'],
        quote='在 $[1,n]$ 中，$m$ 的倍数有 $k = \\lfloor n/m \\rfloor$ 个，结合等差数列求和公式，这些数的和为 $s(m) = k(k+1)/2 \\cdot m$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m` 的倍数是 `m, 2m, …, km`，用等差数列公式一步算出',
              '3 或 5 或 7 的倍数之和 = 单个相加 − 两两重叠 + 三者重叠',
              '两两重叠是 `lcm`：15、21、35；三者重叠是 105'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：符号别写反，`-s(15)-s(21)-s(35)+s(105)`',
                 '`k(k+1)/2` 用整除 `//`，乘积一定是偶数，不会丢精度',
                 '同类题：1201. 丑数 III'],
    ),
)
