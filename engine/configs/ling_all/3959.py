CONFIG = dict(
    num=3959, title='判定好整数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取模 · 合并差值',
    code='''
class Solution:
    def checkGoodInteger(self, n: int) -> bool:
        diff = 0
        while n > 0:
            d = n % 10
            diff += d * d - d
            n //= 10
        return diff >= 50
''',
    call='Solution().checkGoodInteger(1934)',
    expect=True,
    views=[
        dict(type='text', h=110, size=38, fn=lambda S: f"剩下的 n = ==`{S['n']}`==" if 'n' in S else '输入 `n = 1934`'),
        dict(type='text', h=110, size=34, fn=lambda S: f"`diff` = squareSum − digitSum = ==`{S['diff']}`==  （目标 ≥ 50）" if 'diff' in S else ''),
        dict(type='text', h=110, size=30, fn=lambda S: '每个数位 `d` 对 `diff` 的贡献：`d² − d`' if 'diff' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'pink'), ('diff', 'diff', 'green')],
    captions={
        'diff = 0': '`diff` 表示 `squareSum − digitSum`，一开始为 0',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`，还有数位' if S.n > 0 else '`n = 0`：数位取完 → 结束循环'),
        'd = n % 10': '`n % 10` 取个位，`d = {d}`',
        'diff += d * d - d': '`d² − d = {d}×{d} − {d}` = {d*d-d} → `diff` = {B.diff} + {d*d-d} = =={diff}==',
        'n //= 10': '去掉个位：`n` = =={n}==',
        'return diff >= 50': '`diff = {diff}`，{"≥ 50 → 好整数" if diff >= 50 else "< 50 → 不是好整数"}：返回 =={ret}==',
    },
    cards=dict(
        one_liner='平方和减数位和，每个数位的贡献合并成 d² − d',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`digitSum` 是各位之和，`squareSum` 是各位平方之和',
                 '`squareSum − digitSum >= 50` 就是好整数',
                 '示例：`19` → `82 − 10 = 72` → `true`；本视频：`1934`'],
        quote='用一个变量 diff 表示 squareSum − digitSum，对于数字 d，把 diff 加上 d² − d。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n % 10` 是个位，`n //= 10` 去掉个位，循环直到 0',
              '不必分开算两个和：每个数位 `d` 直接给 `diff` 加 `d*d - d`',
              '最后只比较 `diff >= 50`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`d*d - d` 对 0 和 1 都是 0，对 9 是 72，一个 9 就够了',
                 '易错点：是 `>= 50`，不是 `> 50`',
                 '同类题：数位和、快乐数等逐位处理'],
    ),
)
