CONFIG = dict(
    num=2729, title='判断一个数是否迷人', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='范围剪枝 + 拼接判重', tags=[],
    code='''
class Solution:
    def isFascinating(self, n: int) -> bool:
        if n < 123 or n > 329:
            return False
        s = str(n) + str(n * 2) + str(n * 3)
        return '0' not in s and len(set(s)) == 9
''',
    call='Solution().isFascinating(192)',
    expect=True,
    views=[
        dict(type='string', var='s', h=200, color=lambda S, i, v: 'blue' if i < 3 else 'green' if i < 6 else 'purple'),
        dict(type='text', h=110, fn=lambda S: (f"拼接串 `{S['s']}`：不同数字共 =={len(set(S['s']))}== 种，含 0 吗？{'含' if '0' in S['s'] else '不含'}" if 's' in S else f"`n = {S['n']}`，合法范围 `123 ~ 329`")),
    ],
    watch=[('n', 'n', 'blue'), ('s', 's', 'green')],
    captions={
        'if n < 123': '`n = {n}`：`n < 123` 或 `n > 329` 吗？{"是，必不迷人，直接返回 False" if n < 123 or n > 329 else "否，在 123~329 内，继续拼接"}（3n 必须是三位数，且不能有 0 和重复）',
        's = str(n)': '拼接 `n`、`2n`、`3n` = `{s}`',
        'return': "`'0' not in s` 是 {'0' not in s}；`len(set(s)) == 9` 是 {len(set(s)) == 9}（不同数字有 {len(set(s))} 个，且共 9 位）→ =={ret}==",
    },
    cards=dict(
        one_liner='先用范围剪枝，再拼成字符串看是否恰好 1~9 各一次',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['三位数 `n`，把 `n`、`2n`、`3n` 首尾相接成一个数',
                 '若它恰好包含 1 到 9 各一次且没有 0，则 `n` 是迷人的',
                 '示例：`192` → `192384576` → `true`；`100` → `false`'],
        quote='3n 必须是一个三位数，即 3n≤999，所以 n≤333。同时，由于 n 中不能有 0 和重复数字，所以如果 n<123 或者 n>329，直接返回 false。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拼起来要 9 位：`n`、`2n`、`3n` 都得是三位数，所以 `n <= 333`',
              '`n` 自己不能有 0、不能重复，最小 `123`，再结合上界得 `n <= 329`',
              '剩下的拼接成字符串：不含 `0` 且不同字符数为 9 即可'],
        after=[dict(heading='方法二：打表', lines=['枚举所有三位数，只有 4 个满足：', '`192, 219, 273, 327`', '直接 `return n in (192, 219, 273, 327)`，`O(1)`'])],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '==长度恰为 9 由范围保证==，所以只需判断无 `0` 且 `len(set(s)) == 9`',
                 '易错：只看 `len(set(s)) == 9` 会漏掉含 0 的情况',
                 '也可以用二进制 mask 记录出现过的数字'],
    ),
)
