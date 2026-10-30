CONFIG = dict(
    num=1154, title='一年中的第几天', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='库函数 strptime',
    tags=[],
    setup='import datetime',
    code='''
class Solution:
    def dayOfYear(self, date: str) -> int:
        return datetime.datetime.strptime(date, "%Y-%m-%d").timetuple().tm_yday
''',
    call='Solution().dayOfYear("2019-02-10")',
    expect=41,
    views=[
        dict(type='string', var='date', label='date（YYYY-MM-DD）', cell=80, h=200),
        dict(type='text', h=80, size=32,
             fn=lambda S: '`strptime` 按 `%Y-%m-%d` 解析：年 ==2019==，月 ==2==，日 ==10==' if S.get('date') else ''),
        dict(type='text', h=80, size=32,
             fn=lambda S: '`timetuple().tm_yday` = 31 + 10 = ==41==' if S.get('date') else ''),
    ],
    watch=[('date', 'date', 'blue')],
    captions={
        'return datetime': '`strptime` 把 `{date}` 解析成日期对象，`timetuple().tm_yday` 直接给出年内第几天（闰年也会自动处理）→ ==返回 {ret}==',
    },
    cards=dict(
        after=[dict(heading='格式串怎么读', lines=['`%Y` 四位年份，`%m` 两位月份，`%d` 两位日期', '`"2019-02-10"` 对应 `"%Y-%m-%d"`，中间的 `-` 原样匹配', '`tm_yday` 从 1 开始：1 月 1 日是第 1 天', '闰年 2 月多一天，库已经算好，不用自己判断']),
               dict(heading='不用库的写法', lines=['题解只给了库函数这一种写法', '手写要累加每月天数，再判断闰年（4 年一闰、百年不闰、400 年再闰）', '范围内的 1900 年不是闰年，是常见坑'])],
        one_liner='直接调用库：解析日期，再取年内第几天',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定 `YYYY-MM-DD` 格式的日期字符串，返回它是当年的第几天',
                 '范围 1900 到 2019 年，要考虑闰年 2 月',
                 '示例：`"2019-02-10"` → `41`'],
        quote='`datetime.datetime.strptime(date, "%Y-%m-%d").timetuple().tm_yday`',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`strptime` 按格式把字符串变成 `datetime`，非法日期、闰年都由库处理',
              '`timetuple()` 的 `tm_yday` 字段就是一年中的第几天',
              '一行解决，不用自己算每月天数'],
        summary=['时间、空间都是 `O(1)`',
                 '题解只有这一种写法；自己累加每月天数时易错在闰年 2 月',
                 '视频中在 `setup` 里 `import datetime`，作者代码未改'],
    ),
)
