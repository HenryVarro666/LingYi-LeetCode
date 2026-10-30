CONFIG = dict(
    num=1185, title='一周中的第几天', difficulty='Easy', category='模拟',
    author='yiduobo', technique='累加天数 mod 7',
    code='''
class Solution(object):
    def dayOfTheWeek(self, day, month, year):

        date = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        d = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        num = 4
        for y in range(1971, year):
            num += 365
            if y % 400 == 0 or (y % 100 != 0 and y % 4 == 0):
                num += 1
        
        if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
            d[1] += 1

        for m in range(1, month):
            num += d[m - 1]
        
        num += day - 1

        num %= 7

        return date[num]
''',
    call='Solution().dayOfTheWeek(15, 3, 1973)',
    expect='Thursday',
    views=[
        dict(type='text', h=170, size=30, lines=3, fn=lambda S: ('星期表：周一 周二 周三 周四 周五 周六 周日（下标 0–6）' + (f"　当前下标 `{S['num']}` → =={S['date'][S['num']]}==" if S['num'] < 7 else '')) if 'date' in S else ''),
        dict(type='array', var='d', label='d（每月天数）', cell=70, h=170, pointers={'m': 'pink'}),
        dict(type='text', h=110, size=32, fn=lambda S: f"从 1971-01-01 起累计 `num = {S['num']}`" if 'num' in S else ''),
    ],
    watch=[('y', 'y', 'blue'), ('m', 'm', 'pink'), ('num', 'num', 'green')],
    captions={
        'date = [': '星期表，下标 0 对应周一',
        'd = [': '平年每月天数；闰年再把二月加 1',
        'num = 4': '1971-01-01 是周五，在表里下标为 `4`，所以 `num` 从 4 起步',
        'for y in range': lambda S, B, r: (f'累加整年：`y = {S.y}`' if S.get('y', 0) < S.year - 1 or 'y' not in B or B.y != S.y else f'整年累加完，共算到 `{S.year - 1}` 年'),
        'num += 365': '过完 `{y}` 年，加 365 天 → `num = {num}`',
        'if y % 400': lambda S, B, r: (f'`{S.y}` 是闰年（被 400 整除，或被 4 整除但不被 100 整除）' if (S.y % 400 == 0 or (S.y % 100 != 0 and S.y % 4 == 0)) else f'`{S.y}` 是平年，不用多加'),
        'num += 1': '闰年多一天 → `num = {num}`',
        'if year % 400': lambda S, B, r: (f'今年 `{S.year}` 是闰年 → 二月要 29 天' if (S.year % 400 == 0 or (S.year % 100 != 0 and S.year % 4 == 0)) else f'今年 `{S.year}` 是平年，二月 28 天'),
        'd[1] += 1': '二月改成 29 天：`d[1] = {d[1]}`',
        'for m in range': lambda S, B, r: ('整月累加完，剩下本月的天数' if 'm' in B and B.m == S.m and S.m == S.month - 1 else f'累加整月：`m = {S.m}`' if 'm' in S else '本年没有整月要加'),
        'num += d[m - 1]': '加上 `{m}` 月的 `{d[m-1]}` 天 → `num = {num}`',
        'num += day - 1': '本月已过 `day - 1 = {day-1}` 天 → `num = {num}`（当天本身不算）',
        'num %= 7': '一周 7 天循环，取余 → `num = {num}`，下标即星期',
        'return date[num]': '`date[{num}]` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='数出距 1971-01-01 过了几天，再对 7 取余',
        complexity='时间 `O(年数)`，空间 `O(1)`',
        problem=['给定日、月、年，返回这一天是星期几（英文全名）',
                 '已知 1971-01-01 是星期五，日期在 1971–2100 年之间',
                 '本视频：`15, 3, 1973` → `"Thursday"`'],
        quote='比较基础的题目，注意判断闰年的情况即可。另外，查日历可知1997年的元旦是星期五。',
        quote_src='—— yiduobo 题解原文（文中“1997”应为 1971）',
        idea=['星期表从周一开始，周五下标为 4，作为 `num` 初值',
              '逐年累加 365（闰年 366），再逐月累加本年已过的月份',
              '最后加 `day - 1`，对 7 取余当下标'],
        summary=['时间 `O(year - 1971)`，空间 `O(1)`',
                 '闰年：能被 400 整除，或能被 4 整除但不能被 100 整除',
                 '易错：只累加到 `year - 1`，当年用月份累加；当天要 `day - 1`',
                 '本题范围内 2100 年不是闰年，规则要写全',
                 '代码与原文一致，无需改动（Python 2/3 通用）'],
    ),
)
