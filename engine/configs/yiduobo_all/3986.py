CONFIG = dict(
    num=3986, title='统计起止时间经过的秒数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='split 分离再换算',
    tags=[],
    code='''
class Solution(object):
    def secondsBetweenTimes(self, startTime, endTime):
        
        def calc(t):
            h, m, s = t.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)

        return calc(endTime) - calc(startTime)
''',
    call='Solution().secondsBetweenTimes("12:34:56", "13:00:00")',
    expect=1504,
    views=[
        dict(type='string', var='startTime', label='startTime', cell=70, h=150),
        dict(type='string', var='endTime', label='endTime', cell=70, h=150),
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"`{S['h']}` 时 `{S['m']}` 分 `{S['s']}` 秒 → =={int(S['h'])*3600+int(S['m'])*60+int(S['s'])}== 秒"
            if 'h' in S and 'm' in S and 's' in S else '')),
    ],
    watch=['h', 'm', 's'],
    captions={
        'h, m, s = t.split': '按 `:` 切开：时 `{h}`、分 `{m}`、秒 `{s}`（都还是字符串）',
        'return int(h)': '`{h}×3600 + {m}×60 + {s}` = =={ret}==：这个时刻是当天的第 {ret} 秒',
        'return calc(endTime)': '结束 `{calc(endTime)}` 秒 − 开始 `{calc(startTime)}` 秒 = =={ret}==',
    },
    cards=dict(
        one_liner='算出两个时刻各是当天第几秒，二者相减',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两个有效时间 `startTime`、`endTime`，格式 `"HH:MM:SS"`，保证 end 不早于 start',
                 '返回从 start 到 end 经过的秒数',
                 '示例：`"12:34:56"`、`"13:00:00"` → `1504`'],
        quote='先将小时、分钟、秒数分离出来，然后计算出这个时间是当天的第几秒，最后将二者相减即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `split(\':\')` 把字符串拆成时、分、秒三段',
              '`int()` 转成整数后按 3600、60、1 加权',
              '内部函数 `calc` 复用两次，减法得答案'],
        summary=['时间、空间都是 `O(1)`',
                 '`split` 得到的是字符串，别忘了 `int()` 转换',
                 '原文为 Python 2 风格（继承 object），本题无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用切片取时分秒，yiduobo 用 `split`'],
    ),
)
