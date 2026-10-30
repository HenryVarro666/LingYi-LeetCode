_WD = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

CONFIG = dict(
    num=1185, title='一周中的第几天', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='直接调库 datetime',
    code='''
class Solution:
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        return datetime.datetime(year, month, day).strftime("%A")
''',
    setup='import datetime',
    call='Solution().dayOfTheWeek(31, 8, 2019)',
    expect='Saturday',
    views=[
        dict(type='text', h=120, size=40, fn=lambda S: f"日期：`{S['year']}-{S['month']:02d}-{S['day']:02d}`" if 'year' in S else ''),
        dict(type='text', h=100, size=32, fn=lambda S: (f"`strftime(\"%A\")` → =={S['_ret']}==" if '_ret' in S else '库函数已经处理好闰年、每月天数')),
    ],
    watch=[('day', 'day'), ('month', 'month'), ('year', 'year')],
    captions={
        'return datetime': '`datetime.datetime({year}, {month}, {day})` 构造出这一天，`strftime("%A")` 取星期全名 → ==`{ret}`==，闰年和每月天数都由库处理',
    },
    cards=dict(
        one_liner='Python 自带 datetime，一行搞定星期几',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定日、月、年，返回这一天是星期几（英文全名）',
                 '已知 1971-01-01 是星期五，日期在 1971–2100 年之间',
                 '示例：`31, 8, 2019` → `"Saturday"`'],
        quote='return datetime.datetime(year, month, day).strftime("%A")',
        quote_src='—— 灵茶山艾府题解代码（整个题解只有这一行）',
        idea=['日期范围内都是合法日期，直接用语言自带的日期库',
              '`strftime("%A")` 的 `%A` 就是星期的完整英文名',
              '库内部已经处理了闰年和每月天数，不用手写'],
        after=[dict(heading='不用库怎么做', lines=['数出这一天距 1971-01-01 过了多少天 `t`',
                    '1971-01-01 是周五，所以星期下标 = `(t + 4) % 7`（周一为 0）',
                    '数天数要处理闰年：能被 400 整除，或被 4 整除但不被 100 整除',
                    '面试若禁止用库，就写这个方案；本题解直接调库']),
               dict(heading='这行代码在做什么', lines=['`datetime.datetime(year, month, day)` 先构造日期对象',
                    '`.strftime("%A")` 再按格式串输出星期的英文全名',
                    '格式符 `%A` 全名，`%a` 缩写，`%w` 数字（周日为 0）'])],
        summary=['时间、空间都是 `O(1)`',
                 '需要 `import datetime`（本视频在 setup 里导入）',
                 '`%A` 是全名（Saturday），`%a` 才是缩写（Sat）',
                 '不允许用库时，可以按「距 1971-01-01 的天数 % 7」手算，注意闰年'],
    ),
)
