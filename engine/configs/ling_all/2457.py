def _digs(S):
    return [int(c) for c in str(S['m'])] if 'm' in S else []

CONFIG = dict(
    num=2457, title='美丽整数的最小增量', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举进位位置', tags=['难度分 1680'],
    code='''
class Solution:
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        tail = 1
        while True:
            m = x = n + (tail - n % tail) % tail  # 进位后的数字
            s = 0
            while x:
                s += x % 10
                x //= 10
            if s <= target: return m - n
            tail *= 10
''',
    call='Solution().makeIntegerBeautiful(467, 6)',
    expect=33,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`tail = {S['tail']}`：把 {S['n']} 进位到 ==10^k 的倍数== → `m = {S['m']}`" if 'm' in S else f"`n = {S['n']}`，`target = {S['target']}`"),
        dict(type='array', var=_digs, h=200, label='m 的各位数字', cell=110),
        dict(type='text', size=34, fn=lambda S: f"数位和 `s = {S['s']}`，目标 `≤ {S['target']}`，增量 `m − n = {S['m'] - S['n']}`" if 'm' in S and 's' in S else ''),
    ],
    watch=['tail', 'm', 'x', 's', ('n', 'n', 'blue'), ('target', 'target', 'green')],
    captions={
        'tail = 1': '`tail = 1`：先试“不进位”，也就是 `m = n` 本身',
        'm = x =': '把 `n` 向上进位到 `tail = {tail}` 的倍数：`m = {m}`，需要加 `{m - n}`',
        's = 0': '从 0 开始累加 `m` 的数位和',
        's += x % 10': '取个位 `{x % 10 if False else (B.x % 10)}` 加进去：`s = {s}`',
        'x //= 10': '去掉个位，`x` → {x}',
        'if s <= target': '数位和 `{s}` 与 `target = {target}` 比：=={"满足，返回 m − n = " + str(m - n) if s <= target else "还是太大，继续进位"}==',
        'tail *= 10': '这一位的进位不够，再往高一位：`tail` → ==`{tail}`==',
    },
    cards=dict(
        one_liner='不断 +1 直到进位，进位才可能让数位和变小',
        complexity='时间 `O(log^2 n)`，空间 `O(1)`',
        problem=['数字各位之和 `≤ target` 就是美丽整数',
                 '求最小非负 `x`，使 `n + x` 是美丽整数',
                 '示例：`n = 467, target = 6` → `33`（变成 500）'],
        quote='基本思路是，不断 +1 直到产生进位，就可能让数位和变小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只有进位才会让数位和变小，所以只看“进位后的数”',
              '直接算出进位到 10^k 的倍数的结果：467 → 470 → 500 → 1000',
              '从低位到高位试，第一个数位和达标的就是最小增量'],
        summary=['时间 `O(log^2 n)`：最多 log n 轮，每轮数位和 `O(log n)`',
                 '`(tail - n % tail) % tail`：外层取模让已是倍数时增量为 0',
                 '最高位也要能进位：target = 1 时需要进到 1000 这样的数'],
    ),
)
