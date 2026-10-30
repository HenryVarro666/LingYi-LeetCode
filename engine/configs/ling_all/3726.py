CONFIG = dict(
    num=3726, title='移除十进制表示中的所有零', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位拆数 · 就地拼接',
    tags=[],
    code='''
class Solution:
    def removeZeros(self, n: int) -> int:
        ans = 0
        pow10 = 1
        while n:
            n, d = divmod(n, 10)
            if d > 0:
                ans += d * pow10
                pow10 *= 10
        return ans
''',
    call='Solution().removeZeros(1020030)',
    expect=123,
    views=[
        dict(type='text', fn=lambda S: f"剩下的 n = `{S['n']}`" + (f"，刚取出的数位 d = =={S['d']}==" if 'd' in S else ''), size=30),
        dict(type='string', var=lambda S: str(S['n']) if S.get('n') else '', label='n 还没处理的高位（每次砍掉最低位）', cell=84),
        dict(type='text', fn=lambda S: f"ans = `{S['ans']}`，下一个非零数位放在 10^k 位：pow10 = ==`{S['pow10']}`==" if 'pow10' in S else '', size=28),
    ],
    watch=['n', 'd', 'pow10', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 是移除零之后的结果，从空（0）开始拼',
        'pow10 = 1': '`pow10` 是下一个非零数位应该乘的 10^k，k 是 ans 当前的位数',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，还有数位没处理' if S.n else '`n = 0`：所有数位都处理完了，退出循环'),
        'divmod': '`divmod(n, 10)`：商 `n = {n}` 是去掉最低位的数，余数 `d = {d}` 就是被取出的最低位',
        'if d > 0': lambda S, B, r: (f'`d = {S.d} > 0` → 保留这个数位' if S.d > 0 else '`d = 0` → ==零直接丢掉==，ans 和 pow10 都不动'),
        'ans += d': '把 `{d}` 放到 ans 的下一位：`ans += {d} × {B.pow10} = {ans}`',
        'pow10 *= 10': '又多了一位，`pow10` → {pow10}，下一个数位放得更高',
        'return ans': '`n` 的非零数位按原顺序拼好了，返回 `{ans}`',
    },
    cards=dict(
        one_liner='从低位到高位取数位，非零的按 10^k 拼回去',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给正整数 `n`，删掉十进制表示里的所有 0，返回得到的整数',
                 '示例：`1020030` → `123`；`1` → `1`',
                 '本视频：`n = 1020030`'],
        quote='不断地把 n 除以 10（下取整）直到 0，例如 123→12→1→0。在这个过程中的 n mod 10，即为每个数位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(n, 10)` 一步得到去掉最低位的 `n` 和最低位 `d`',
              '`d` 不为零就用 `d × 10^k` 加进答案，`k` 是答案当前的长度',
              '每加一个数位 `pow10` 乘 10；遇到 0 什么都不做，零就消失了'],
        result='`1020030` 去掉三个 0 → `123` ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '低位先出来，所以按 `d * pow10` 往高位放，不需要反转',
                 '易错：`pow10` 只在 `d > 0` 时才乘 10，否则零会占位',
                 '同类：按位拆数的题都可以用 `divmod(n, 10)`'],
    ),
)
