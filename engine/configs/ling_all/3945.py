CONFIG = dict(
    num=3945, title='计算数字频率得分', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取模求数位和',
    code='''
class Solution:
    def digitFrequencyScore(self, n: int) -> int:
        ans = 0
        while n > 0:
            ans += n % 10
            n //= 10
        return ans
''',
    call='Solution().digitFrequencyScore(1223)',
    expect=8,
    views=[
        dict(type='text', h=120, size=40, fn=lambda S: (f"剩下的 n = ==`{S['n']}`==；已累加的数位和 ans = ==`{S['ans']}`==" if 'n' in S else '')),
        dict(type='text', h=120, size=30, fn=lambda S: '每个数字 d 出现 freq 次，贡献 `d × freq` = 把 d 加 freq 次' if 'ans' in S else ''),
        dict(type='text', h=120, size=30, fn=lambda S: '所以得分 = ==所有数位之和==' if 'ans' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加所有数位',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`，还有数位没取' if S.n > 0 else '`n = 0`：数位取完了 → 结束循环'),
        'ans += n % 10': '`n % 10 = {n % 10}` 是个位数字 → `ans` = {B.ans} + {n % 10} = =={ans}==',
        'n //= 10': '去掉个位：`n` = {B.n} // 10 = =={n}==',
        'return ans': '得分就是数位和 `{ans}`',
    },
    cards=dict(
        one_liner='d × 出现次数 的总和，本质就是数位和',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['得分 = 对每个不同数字 `d`，累加 `d * freq(d)`',
                 '示例：`n = 122` → `1×1 + 2×2 = 5`',
                 '本视频：`n = 1223` → `8`'],
        quote='本质就是计算 n 的数位和。不用字符串做。不断地把 n 除以 10（下取整）直到 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数字 `d` 出现 `freq` 次，贡献 `d × freq`，等于把 `d` 加 `freq` 次',
              '所以不必统计频率，直接把每个数位加起来',
              '`n % 10` 取个位，`n //= 10` 去掉个位'],
        summary=['时间 `O(log n)`：`n` 的十进制位数', '空间 `O(1)`，不用哈希表也不用字符串',
                 '易错点：循环条件 `n > 0`，`n` 至少为 1 所以不会漏',
                 '同类题：数位和、各位相乘等逐位处理题'],
    ),
)
