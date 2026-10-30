def _b(x, w=4):
    return list(format(x, '0%db' % w))

CONFIG = dict(
    num=2220, title='转换数字的最少位翻转次数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='异或 + bit_count',
    tags=['位运算', '基础题', '难度分 1282'],
    code='''
class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        return (start ^ goal).bit_count()
''',
    call='Solution().minBitFlips(10, 7)',
    expect=3,
    views=[
        dict(type='string', var=lambda S: _b(S['start']), label='start = 10', h=150),
        dict(type='string', var=lambda S: _b(S['goal']), label='goal = 7', h=150),
        dict(type='string', var=lambda S: _b(S['start'] ^ S['goal']), label='start ^ goal（1 = 这一位不同）',
             color=lambda S, i, v: 'yellow' if v == '1' else None, h=150),
        dict(type='text', fn=lambda S: f"异或后有 =={bin(S['start'] ^ S['goal']).count('1')}== 个 1，就要翻转 =={bin(S['start'] ^ S['goal']).count('1')}== 次", size=34),
    ],
    watch=['start', 'goal', ('start ^ goal', 'start ^ goal', 'yellow')],
    captions={
        'return': '`start ^ goal` = `{start ^ goal}`，二进制 `{start ^ goal:04b}`；数里面 1 的个数 → =={ret}==，每个 1 就是必须翻转的一位',
    },
    cards=dict(
        one_liner='异或后 1 的个数，就是要翻转的位数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['一次操作翻转 `x` 二进制中的一位（含前导 0）',
                 '求把 `start` 变成 `goal` 的最少翻转次数',
                 '示例：`start=10, goal=7` → `3`'],
        quote='返回两个数异或和的二进制中的 1 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异或的性质：两位相同得 0，不同得 1',
              '所以 `start ^ goal` 里的 1，正是两数不同的位',
              '每个不同的位翻一次就够，也必须翻一次'],
        after=[dict(heading='再看一个例子', lines=['`start=3=011`，`goal=4=100`', '异或得 `111`，三个 1', '三位全不同，所以要翻转 `3` 次，对应示例 2', '翻转的位置可以任意顺序，次数不变']), dict(heading='同类题', lines=['第 461 题「汉明距离」就是同一道题', '数 1 的个数还可以用 `x & (x-1)` 每次去掉最低位 1', 'Python 3.10 起直接用 `bit_count()`', '位运算基础题：先学会异或的「找不同」'])],
        summary=['时间、空间都是 `O(1)`（整数位数固定）',
                 '`int.bit_count()` 需要 Python 3.10+',
                 '与第 461 题（汉明距离）完全相同'],
    ),
)
