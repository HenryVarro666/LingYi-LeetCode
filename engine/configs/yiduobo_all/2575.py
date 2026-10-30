CONFIG = dict(
    num=2575, title='找出字符串的可整除数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='递推前缀余数',
    tags=[],
    code='''
class Solution(object):
    def divisibilityArray(self, word, m):

        now = 0
        res = []
        for char in word:
            now = now * 10 + int(char)
            now %= m
            if now == 0:
                res.append(1)
            else:
                res.append(0)
        
        return res
''',
    call='Solution().divisibilityArray("998244353", 3)',
    expect=[1, 1, 0, 0, 0, 1, 1, 0, 0],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符）', color=lambda S, i, v: 'blue' if 'char' in S and i == len(S['res']) - (1 if S['_line'] in (10, 12) else 0) else None, h=170),
        dict(type='array', var='res', label='res（1 = 前缀能整除 m）', h=170,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', fn=lambda S: f"上一个前缀余数 ×10 + 当前数字，再 % {S['m']}；now = =={S['now']}==" if 'now' in S else '', h=70),
    ],
    watch=['char', ('now', 'now', 'yellow'), 'm'],
    captions={
        'now = 0': '`now` 记录「上一个前缀对 m 的余数」，开始时为 0',
        'now = now * 10': '后一个前缀 = 前一个前缀 ×10 + `{char}`，余数也这样推：`{B.now}×10+{char} = {now}`',
        'now %= m': '对 `m = {m}` 取模：`now = {now}`，数字不会越变越大',
        'if now == 0': lambda S, B, r: ('余数为 0 → 这个前缀能被 m 整除' if S.now == 0 else f'余数 `{S.now}` ≠ 0 → 不能整除'),
        'res.append(1)': '记 `1`',
        'res.append(0)': '记 `0`',
        'return res': '遍历完，返回 `res`',
    },
    cards=dict(
        one_liner='相邻前缀相差「乘 10 加一位」，余数也能这样递推',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['字符串 `word` 与正整数 `m`，判断每个前缀表示的数能否被 `m` 整除',
                 '能整除记 `1`，否则记 `0`',
                 '示例：`"998244353"`，`m=3` → `[1,1,0,0,0,1,1,0,0]`'],
        quote='后者就相当于前者乘以10再加上word[p]。根据取模的性质，就可以利用每个前缀左侧相邻前缀对m取模的结果，推算出当前前缀对m取模的结果',
        quote_src='—— yiduobo 题解原文',
        idea=['`r[i] = (r[i-1]×10 + word[i]) % m`',
              '一趟遍历，只保留上一个余数 `now`',
              '`now == 0` 填 `1`，否则填 `0`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：直接把前缀转整数会非常大，必须每步取模',
                 '代码未改，原文已是 Python 3 可运行的写法'],
    ),
)
