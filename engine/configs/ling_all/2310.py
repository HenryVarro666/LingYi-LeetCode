def _digits(S):
    k = S['k']
    return [(m * k) % 10 for m in range(11)]


def _col(S, i, v):
    if i == 0:
        return 'dim'
    return 'green' if v == S['num'] % 10 else None


def _text(S):
    num, k = S['num'], S['k']
    if 'n' not in S:
        return f'`num = {num}`，`k = {k}`：要选 `n` 个以 `{k}` 结尾的数，`num - n*k` 必须是 10 的倍数；目标个位 `{num % 10}`'
    n = S['n']
    return f'`n = {n}`：`{n}×{k}` 的个位是 `{(n * k) % 10}`，目标个位是 `{num % 10}`；`num - n*k = {num - n * k}`'


CONFIG = dict(
    num=2310, title='个位数字为 K 的整数之和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举个数 n',
    tags=['灵神题单', '难度分 1559'],
    code='''
class Solution:
    def minimumNumbers(self, num: int, k: int) -> int:
        if num == 0: return 0
        for n in range(1, num + 1):
            if num - n * k < 0: break
            if (num - n * k) % 10 == 0: return n
        return -1
''',
    call='Solution().minimumNumbers(58, 9)',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=90, lines=2),
        dict(type='array', var=_digits, label='n × k 的个位数（下标 = n；绿 = 等于 num 的个位）',
             pointers={'n': 'blue'}, color=_col, h=200),
    ],
    watch=[('num', 'num', 'blue'), ('k', 'k', 'pink'), ('n', 'n', 'orange'), ('num-n*k', 'num - n * k if "n" in dir() else None', 'green')],
    captions={
        'if num == 0': '`num = 0` 时空多重集的和就是 0，答案 0：先特判',
        'for n in': '枚举数的个数 `n`，从小到大：第一个可行的就是最小的 → `n = {n}`',
        'if num - n * k < 0': lambda S, B, r: (f'`{S.num} - {S.n}×{S.k} = {S.num - S.n * S.k}` < 0：`n` 个 `{S.k}` 已经超过 `num`，再大更不行 → break'
                                               if S.num - S.n * S.k < 0 else f'`{S.num} - {S.n}×{S.k} = {S.num - S.n * S.k}` ≥ 0，还没超过'),
        '% 10 == 0': lambda S, B, r: (f'`{S.num - S.n * S.k} % 10 = {(S.num - S.n * S.k) % 10}`：是 10 的倍数 → 剩下的可以==补到十位以上== → 答案 `n = {S.n}`'
                                      if (S.num - S.n * S.k) % 10 == 0 else f'`{S.num - S.n * S.k} % 10 = {(S.num - S.n * S.k) % 10}`：不是 10 的倍数，个位对不上 → 试下一个 `n`'),
        'return -1': '枚举完都不行 → `-1`',
    },
    cards=dict(
        one_liner='枚举个数 n：个位是 k，所以 num − n·k 必须是 10 的倍数',
        complexity='时间 `O(1)`（至多枚举 10 次），空间 `O(1)`',
        problem=['多重集里每个正整数的个位数字都是 `k`，总和为 `num`',
                 '求这个多重集最少有几个数，不存在返回 `-1`',
                 '示例：`num = 58, k = 9` → `2`（`9 + 49`）'],
        quote='把个位数单独拆开看，每个数可以表示成 10 的倍数加上 k 的形式。由于这 n 个数都以 k 结尾，那么 num−nk 必须是 10 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案范围小（`n ≤ num`），直接枚举个数 `n`',
              '每个数 = 10 的倍数 + `k`，`n` 个数的个位部分共 `n·k`',
              '`num − n·k` 非负且是 10 的倍数，多出来的十位以上随便分给某个数'],
        summary=['时间 `O(num)`；`n·k` 模 10 以 10 为周期，实际只需枚举到 `n = 10`，`O(1)`',
                 '易错：`num = 0` 要特判返回 0；`num - n*k < 0` 要及时 break',
                 '`k = 0` 时只能是 `num` 本身以 0 结尾（答案 1）或 -1',
                 '题解还给了 `k=0` 特判 + `next(...)` 的简写，以及 `@cache` 记忆化写法'],
    ),
)
