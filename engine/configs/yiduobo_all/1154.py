CONFIG = dict(
    num=1154, title='一年中的第几天', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟 · 累加月份天数',
    tags=[],
    code='''
class Solution(object):
    def dayOfYear(self, date):

        days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
        y, m, d = date.split('-')
        y = int(y)
        if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
            days[2] += 1
        
        return sum(days[:int(m)]) + int(d)
''',
    call='Solution().dayOfYear("2020-03-05")',
    expect=65,
    views=[
        dict(type='string', var='date', label='date', cell=80, h=150),
        dict(type='array', var='days', label='days（days[i] = 第 i 月的天数，days[0] 占位）', cell=70, h=230,
             window=(lambda S: 0, lambda S: int(S['m']) - 1 if 'm' in S else 0)),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"年 `y = {S['y']}`，月 `m = {S['m']}`，日 `d = {S['d']}`" if 'd' in S else '')),
    ],
    watch=['y', 'm', 'd'],
    captions={
        'days = [': '`days[i]` 是第 i 月的天数，==2 月先按 28 天==，`days[0]` 放 0 占位',
        'date.split': '按 `-` 拆开：年 `{y}`，月 `{m}`，日 `{d}`',
        'y = int': '年份转成整数 `{y}`，用来判断闰年',
        'if y % 400': '闰年条件：能被 400 整除，或者 ==能被 4 整除但不能被 100 整除==；`y = {y}` → {"是闰年" if (y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)) else "不是闰年"}',
        'days[2] += 1': '闰年 2 月有 29 天：`days[2]` 加 1 → {days[2]}',
        'return sum': '`sum(days[:{int(m)}])` 是前 {int(m)-1} 个月的总天数 {sum(days[:int(m)])}，再加上本月第 `{int(d)}` 天 → ==返回 {ret}==',
    },
    cards=dict(
        one_liner='先累加前面整月的天数，再加上本月的日期',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定 `YYYY-MM-DD` 格式的日期，返回它是当年的第几天',
                 '示例：`"2019-02-10"` → `41`',
                 '本视频：`"2020-03-05"`（闰年）→ `65`'],
        quote='比较基础的题目，需要特别注意闰年2月的天数。',
        quote_src='—— yiduobo 题解原文',
        idea=['用数组存每月天数，前 `m-1` 个月的天数相加，再加日 `d`',
              '闰年判断：==被 400 整除，或被 4 整除且不被 100 整除==',
              '闰年把 2 月改成 29 天，其余月份不变'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：1900 年能被 100 整除但不能被 400 整除，不是闰年',
                 '`days[:int(m)]` 取到第 m-1 月，因为 `days[0]` 是占位',
                 '原文已是 Python 3 可运行写法，仅保留代码未改'],
    ),
)
