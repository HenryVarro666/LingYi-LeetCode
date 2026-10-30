_N = 52143
_D = [int(c) for c in str(_N)]

CONFIG = dict(
    num=2544, title='交替数字和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='分离数位 · 翻转后按下标奇偶加减',
    tags=[],
    code='''
class Solution(object):
    def alternateDigitSum(self, n):

        digit_list = []
        while n:
            digit_list.append(n % 10)
            n //= 10
        
        digit_list.reverse()

        res = 0
        for index in range(len(digit_list)):
            if index % 2 == 0:
                delta = 1
            else:
                delta = -1
            
            res += delta * digit_list[index]
        
        return res
''',
    call='Solution().alternateDigitSum(52143)',
    expect=3,
    views=[
        dict(type='array', var='digit_list', label='digit_list（低位在前，反转后高位在前）', h=240,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if 'delta' in S and S.get('delta') == 1 else 'pink') if 'index' in S and i == S['index'] and 'delta' in S else None),
        dict(type='text', fn=lambda S: (f"第 `{S['index']}` 位：下标{'偶' if S['index'] % 2 == 0 else '奇'}，符号 `{'+' if S['delta'] > 0 else '-'}`" if 'index' in S and 'delta' in S else '先把数位分离出来'), size=30, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('index', 'index', 'pink'), ('delta', 'delta', 'orange'), ('res', 'res', 'green')],
    captions={
        'digit_list = []': '准备 `digit_list` 存放分离出的数位',
        'while n': '`n = {n}`：还有数位，继续分离',
        'digit_list.append': '`n % 10` 取个位 `{digit_list[-1]}` 放入列表 → `{digit_list}`',
        'n //= 10': '`n //= 10`，去掉个位，`n` 变成 `{n}`',
        'digit_list.reverse()': '分离出来是低位在前，==翻转==成高位在前：`{digit_list}`',
        'res = 0': '`res = 0` 累计答案',
        'for index': lambda S, B, r: ('每一位都处理完，`for` 循环结束' if 'index' in B and B.index == S.index else f"处理下标 `{S.index}` 的数位 `{S.digit_list[S.index]}`"),
        'if index % 2 == 0': '`{index} % 2 == 0` → {index % 2 == 0}：偶数下标取正，奇数下标取负',
        'delta = 1': '偶数下标，符号 `delta = 1`',
        'delta = -1': '奇数下标，符号 `delta = -1`',
        'res += delta': '`res += {delta} × {digit_list[index]}` → `res = {res}`',
        'return res': '全部加完，答案 `{res}`',
    },
    cards=dict(
        one_liner='先把数位拆出来翻转，再按下标奇偶加减',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['最高位取正号，之后每位符号与前一位相反，求带符号数位和',
                 '示例：`n = 521` → `4`',
                 '本视频：`n = 52143` → `3`'],
        quote='首先通过模10除以10的操作将n的数位分离出来，翻转后一趟遍历，按照当前下标对其进行加法或者减法即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % 10`、`n //= 10` 反复执行，数位按从低到高存进列表',
              '翻转后最高位在下标 0：==偶数下标加，奇数下标减==',
              '分成两步，不用考虑总位数，思路最直接'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（存数位列表）',
                 '易错：不翻转的话，奇偶要从最高位算起，位数为偶数时符号会反',
                 '原文为 Python 2 写法，`n /= 10` 已改为 `n //= 10`',
                 '对比灵神：灵神不开列表，用 `sign` 翻转并在最后修正'],
    ),
)
