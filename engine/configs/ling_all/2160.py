CONFIG = dict(
    num=2160, title='拆分数位后四位数字的最小和', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='数位排序，小的放十位（Go 原文转写）',
    tags=['贪心与思维', '难度分 1314'],
    code='''
class Solution:
    def minimumSum(self, num: int) -> int:
        s = list(str(num).encode())
        s.sort()
        return ((s[0] & 15) + (s[1] & 15)) * 10 + (s[2] & 15) + (s[3] & 15)
''',
    call='Solution().minimumSum(2932)',
    expect=52,
    views=[
        dict(type='text', fn=lambda S: f"num = `{S['num']}`", size=30),
        dict(type='array', var='s', label='s 的四个数位（ASCII 码，低 4 位就是数字）', cell=110),
        dict(type='text', fn=lambda S: (f"`(({S['s'][0] & 15} + {S['s'][1] & 15}) × 10) + {S['s'][2] & 15} + {S['s'][3] & 15}` = =={((S['s'][0] & 15) + (S['s'][1] & 15)) * 10 + (S['s'][2] & 15) + (S['s'][3] & 15)}=="
                                        if 's' in S and S['_line'] >= 5 else ''), size=26),
    ],
    watch=[('num', 'num')],
    captions={
        's = list': '把 `{num}` 转成字符串再取每个字符的 ASCII 码 → `{s}`',
        's.sort()': '从小到大排序 → `{s}`，数字顺序为 `{[c & 15 for c in s]}`',
        'return': '前两个小数字当十位：`({s[0] & 15} + {s[1] & 15}) × 10`；后两个当个位：`{s[2] & 15} + {s[3] & 15}`；和 = =={ret}==',
    },
    cards=dict(
        one_liner='拆成两个两位数，最小的两个数字放十位',
        complexity='时间 `O(1)`（只有 4 位），空间 `O(1)`',
        problem=['把四位数 `num` 的数位拆成两个新整数 `new1`、`new2`，所有数位都要用，可有前导 0',
                 '求 `new1 + new2` 的最小值',
                 '示例：`2932` → `52`（`29 + 23`）'],
        quote='通过比对可以发现，拆分成两位数 + 两位数是最优的。因此要使 new1+new2 最小，应当最小化十位数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个两位数最优：高位数越少，和越小',
              '十位权重 10，个位权重 1 → 最小的两个数字放十位',
              '把数字从小到大排序，前两个当十位，后两个当个位'],
        after=[dict(heading='为什么两位 + 两位最优', lines=['拆成 3 位 + 1 位：百位权重 100，太大', '`2932` → `[223, 9]` = 232，远大于 52', '两位 + 两位：权重只有 10 和 1，最小']) ],
        result='`2932` 排序后 `2,2,3,9` → `(2+2)×10 + 3 + 9 = 52` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Go 里 `[]byte` 的元素用 `&15` 取数字，Python 用 `str(num).encode()` 得到同样的字节整数；Go 里 `&` 优先级高于 `+`，Python 要加括号',
                 '两个十位数字和为 `a + b`，答案 `(a + b) × 10 + c + d`',
                 '时间 `O(1)`，空间 `O(1)`'],
    ),
)
