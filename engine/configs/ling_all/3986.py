CONFIG = dict(
    num=3986, title='统计起止时间经过的秒数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='换算成当天秒数再相减',
    tags=[],
    code='''
class Solution:
    def parse(self, t: str) -> int:
        return int(t[:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:])

    def secondsBetweenTimes(self, startTime: str, endTime: str) -> int:
        return self.parse(endTime) - self.parse(startTime)
''',
    call='Solution().secondsBetweenTimes("12:34:56", "13:00:00")',
    expect=1504,
    views=[
        dict(type='string', var='startTime', label='startTime', cell=70, h=150),
        dict(type='string', var='endTime', label='endTime', cell=70, h=150),
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"`{S['t'][:2]}`×3600 + `{S['t'][3:5]}`×60 + `{S['t'][6:]}` = =={int(S['t'][:2])*3600+int(S['t'][3:5])*60+int(S['t'][6:])}=="
            if 't' in S else '')),
    ],
    watch=['t', ('start秒', "self.parse(startTime)", 'blue'), ('end秒', "self.parse(endTime)", 'pink')],
    captions={
        'return int(t[:2])': '`t[:2]` 是时、`t[3:5]` 是分、`t[6:]` 是秒：换算成当天第几秒 = =={ret}==',
        'return self.parse(endTime)': '结束时刻的秒数 `{self.parse(endTime)}` 减开始时刻 `{self.parse(startTime)}` = =={ret}==，就是经过的秒数',
    },
    cards=dict(
        one_liner='先把时间都换成当天的第几秒，再相减',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给两个 `"HH:MM:SS"` 格式的时间，`endTime` 不早于 `startTime`',
                 '求从 `startTime` 到 `endTime` 经过的秒数',
                 '示例：`"12:34:56"`、`"13:00:00"` → `1504`'],
        quote='int(t[:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:])',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['格式固定为 8 位，用切片 `t[:2]`、`t[3:5]`、`t[6:]` 取出时分秒',
              '时 ×3600 + 分 ×60 + 秒 = 当天第几秒',
              '两个时刻各算一次，结束减开始即可'],
        summary=['时间、空间都是 `O(1)`（字符串长度固定为 8）',
                 '切片下标易错：冒号在 `[2]`、`[5]`，所以分钟是 `t[3:5]`，秒是 `t[6:]`',
                 '题目保证 `endTime` 不早于 `startTime`，不用处理跨天'],
    ),
)
