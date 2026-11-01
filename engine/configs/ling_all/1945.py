CONFIG = dict(
    num=1945, title='字符串转化后的各位数字之和', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='模拟 · 先拆字母再求数位和（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def getLucky(self, s: str, k: int) -> int:
        sum = 0
        for b in s:
            b = ord(b) - (ord('a') - 1)
            sum += b // 10 + b % 10
        k -= 1
        while k > 0 and sum > 9:  # sum < 10 时可以提前退出
            s = sum
            sum = 0
            while s > 0:
                sum += s % 10
                s //= 10
            k -= 1
        return sum
''',
    call='Solution().getLucky("leetcode", 2)',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"当前字母位置 `b = {S['b']}` → 数位和 `{S['b'] // 10} + {S['b'] % 10}`" if isinstance(S.get('b'), int) and S.get('_line') in (5, 6) else ''), h=80),
        dict(type='text', fn=lambda S: (f"字符串 `s = {S['s']}`" if isinstance(S.get('s'), str) else (f"正在拆的数 `s = {S['s']}`" if 's' in S else '')), h=80),
        dict(type='text', fn=lambda S: f"当前 `sum = {S['sum']}`，剩余次数 `k = {S['k']}`" if 'sum' in S and 'k' in S else '', size=36, h=160),
    ],
    watch=['b', ('sum', 'sum', 'green'), 'k', 's'],
    captions={
        3: '`sum` 累加每个字母位置的数位和',
        'for b in s': '取下一个字母',
        'b = ord(b)': '字母换成它的位置：`b = {b}`',
        'sum += b': '位置 `{b}` 的数位和是 `{b // 10} + {b % 10}`：`sum` {B.sum} → =={sum}==',
        'while k > 0': lambda S, B, ret: (f"`k = {S.k}`，`sum = {S.sum}`：还要转换且 `sum > 9` → ==继续=="
                                          if S.k > 0 and S.sum > 9 else
                                          (f"`k = {S.k}`，已转换够次数，结束" if S.k <= 0 else f"`sum = {S.sum} < 10`：再求数位和也不变 → ==提前退出==")),
        's = sum': '把当前 `sum = {sum}` 存进 `s`，准备拆数位',
        10: '`sum` 清零，重新累加数位',
        'while s > 0': lambda S, B, ret: (f"`s = {S.s}` > 0：还有数位没拆" if S.s > 0 else '`s` 拆完了'),
        'sum += s % 10': '取个位 `{B.s % 10}`：`sum` → =={sum}==',
        's //= 10': '去掉个位：`s` → {s}',
        'return sum': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='先拆字母位置求数位和，再把剩下的 k−1 次做完',
        complexity='时间 `O(n + k log n)`，空间 `O(1)`',
        problem=['字母换成字母表位置 a=1 … z=26，拼成整数',
                 '把它重复替换成各位数字之和 `k` 次，返回结果',
                 '示例：`"leetcode"`，`k = 2` → 33 → `6`'],
        quote='`sum < 10 时可以提前退出`',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['第一次数位和不用真拼大整数：每个字母位置至多两位，直接累加十位+个位',
              '剩下 `k-1` 次对 `sum` 反复拆数位',
              '`sum < 10` 时再求和结果不变，可以提前退出'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n + k log n)`，空间 `O(1)`',
                 '易错：第一次转换要在循环里做完，循环只补 `k-1` 次',
                 '转写时 `s /= 10` 对应整数除法 `s //= 10`'],
    ),
)
