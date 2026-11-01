CONFIG = dict(
    num=1952, title='三除数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举因子 成对统计（Go 原文转写）',
    tags=['难度分 1204'],
    code='''
class Solution:
    def isThree(self, n: int) -> bool:
        cnt = 0
        d = 1
        while d * d <= n:
            if n % d == 0:
                cnt += 1
                if d * d < n:
                    cnt += 1
            d += 1
        return cnt == 3
''',
    call='Solution().isThree(9)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"枚举 `d = {S['d']}`，`d × d = {S['d']*S['d']}`，`n = {S['n']}`；已找到 =={S['cnt']}== 个除数" if 'd' in S else ''),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='1 到 n（绿色 = n 的除数）', h=260,
             color=lambda S, i, v: ('green' if S['n'] % v == 0 and v * v <= S['n'] and v < S['d'] else ('blue' if v == S['d'] else None)) if 'd' in S else None,
             dim=lambda S, i, v: 'd' in S and v > S['d']),
    ],
    watch=['n', ('d', 'd', 'blue'), ('cnt', 'cnt', 'green')],
    captions={
        'cnt = 0': '`cnt` 统计 `n` 的除数个数，从 0 开始',
        'd = 1': '从 `d = 1` 开始，只枚举到 `d × d <= n` 为止',
        'while d * d <= n': lambda S, B, r: (f'`{S.d} × {S.d} = {S.d*S.d} <= {S.n}`，继续枚举' if S.d * S.d <= S.n else f'`{S.d} × {S.d} > {S.n}`：更大的除数都已经成对数过了，结束'),
        'if n % d == 0': lambda S, B, r: f'`{S.n} % {S.d} = {S.n % S.d}` → ' + ('==整除==，`d` 是除数' if S.n % S.d == 0 else '不整除，跳过'),
        'cnt += 1': '`d = {d}` 是除数，`cnt` → {cnt}',
        'if d * d < n': lambda S, B, r: f'`{S.d} × {S.d} = {S.d*S.d}` ' + (f'< {S.n}：还有配对的除数 `{S.n // S.d}`，要再算一个' if S.d * S.d < S.n else f'= {S.n}：`d` 和 `n/d` 是同一个数，不重复计数'),
        'd += 1': '`d` → {d}',
        'return cnt == 3': '`cnt = {cnt}`，是否恰好 3 个除数：=={ret}==',
    },
    cards=dict(
        one_liner='枚举到根号 n，除数成对出现，恰好 3 个就是答案',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['给一个整数 `n`，判断它是否恰好有 ==三个== 正除数',
                 '示例：`n = 4` → 除数 1、2、4 → `true`',
                 '本视频：`n = 9` → 除数 1、3、9 → `true`'],
        quote='枚举 d 从 1 开始，d*d <= n；若 n%d == 0 则 cnt++，且 d*d < n 时再 cnt++（配对的 n/d）。',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['除数成对：`d` 和 `n / d`，所以只枚举 `d × d <= n`',
              '`d × d == n` 时两者相同，只算一个',
              '最后看 `cnt` 是否等于 3'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for` 循环写成 `while`）',
                 '时间 `O(√n)`，空间 `O(1)`',
                 '易错点：完全平方数 `d × d == n` 只能算一次',
                 '恰好 3 个除数等价于 n 是质数的平方'],
    ),
)
