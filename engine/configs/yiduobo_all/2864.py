CONFIG = dict(
    num=2864, title='最大二进制奇数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='统计 1 的个数再拼接',
    tags=[],
    code='''
class Solution(object):
    def maximumOddBinaryNumber(self, s):

        one = sum([int(x) for x in s])
        n = len(s)
        
        return '1' * (one - 1) + '0' * (n - one) + '1'
''',
    call="Solution().maximumOddBinaryNumber('0101101')",
    expect='1110001',
    views=[
        dict(type='text', fn=lambda S: ('`1` 的个数 `one = %d`，总长 `n = %d`' % (S['one'], S['n'])) if 'n' in S else ('统计 `1` 的个数 `one = %d`' % S['one'] if 'one' in S else ''), size=28),
        dict(type='string', var='s', label='s（绿 = 1，其余 = 0）', cell=84,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='text', fn=lambda S: ('最后 = `%s` ＋ `%s` ＋ `1`' % ('1' * (S['one'] - 1), '0' * (S['n'] - S['one']))) if 'n' in S else '', size=28),
    ],
    watch=[('one', 'one', 'green'), ('n', 'n')],
    captions={
        'one = sum': '各位数字求和 = `1` 的个数：`one = {one}`',
        'n = len': '总长度 `n = {n}`，所以 `0` 有 `{n - one}` 个',
        'return': '末位必须是 `1`，剩下 `{one - 1}` 个 `1` 集中放高位、再接 `{n - one}` 个 `0`、最后一个 `1` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='最低位放 1 保证奇数，其余 1 靠高位保证最大',
        complexity='时间 `O(n)`，空间 `O(n)`（列表推导）',
        problem=['二进制串 `s`，至少含一个 `1`', '重排各位，使得到的数是最大的奇数（可含前导零）', '示例：`"010"` → `"001"`'],
        quote='为了使得答案为奇数，那么二进制的最低位必须是1，而为了使得答案最大，那么就应该将剩下的1集中在答案的高位。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计一遍 `1` 的个数 `one`', '答案 = `one-1` 个 `1` ＋ 所有 `0` ＋ 最低位的 `1`', '三段拼起来，不用真的排序'],
        before=[dict(heading='先看一个小例子', lines=['`s = "0101101"`：7 位，其中 4 个 `1`', '最低位放 `1` → 剩 3 个 `1` 靠左', '`111` ＋ `000` ＋ `1` → `1110001`'])],
        after=[dict(heading='为什么这样最大', lines=['最低位必须是 `1`（奇数）', '高位权重大，`1` 越靠左数越大', '所以高位全 `1`，其后全 `0`，末位 `1`'])],
        summary=['一趟遍历统计 `1`，时间 `O(n)`',
                 '易错：别忘了给最低位留一个 `1`，所以前面是 `one - 1`',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神用 `s.count(\'1\')` 数个数，yiduobo 用 `sum` 对数字求和'],
    ),
)
