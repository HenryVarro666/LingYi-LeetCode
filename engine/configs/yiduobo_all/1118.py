CONFIG = dict(
    num=1118, title='一月有多少天', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='查表 + 闰年判断', tags=[],
    code='''
class Solution(object):
    def numberOfDays(self, year, month):

        d = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        res = d[month]
        if month == 2 and (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)):
            res += 1
        return res
''',
    call='Solution().numberOfDays(2000, 2)',
    expect=29,
    views=[
        dict(type='array', var='d', pointers={'month': 'blue'}, h=200, label='d：每月天数（下标 = 月份）',
             color=lambda S, i, v: 'green' if i == S.get('month') else None),
        dict(type='text', size=34, fn=lambda S: (
            f"`{S['year']}` 年：整除 400 = `{S['year'] % 400 == 0}`，整除 4 = `{S['year'] % 4 == 0}`，整除 100 = `{S['year'] % 100 == 0}`"
            if 'year' in S else '')),
        dict(type='text', size=34, fn=lambda S: f"天数 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('year', 'year', 'blue'), ('month', 'month', 'pink'), ('res', 'res', 'green')],
    captions={
        'd = [0': '`d` 记录平年每月天数，开头补一个 `0`，让下标正好等于月份',
        'res = d[month]': '先按平年查表：`d[{month}] = {res}`',
        'month == 2 and': lambda S, B, r: (
            f"是二月，再看 `{S.year}` 是否闰年：能被 400 整除，或「能被 4 整除且不能被 100 整除」→ =={'是闰年' if (S.year % 400 == 0 or (S.year % 4 == 0 and S.year % 100 != 0)) else '不是闰年'}=="
            if S.month == 2 else f'`month = {S.month}` 不是二月，不用管闰年'),
        'res += 1': '闰年二月多一天：`res` 变成 =={res}==',
        'return res': '这个月有 `{res}` 天',
    },
    cards=dict(
        one_liner='查表得平年天数，二月遇闰年再加一天',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定年份 `year` 和月份 `month`，返回该月的天数',
                 '示例：`year=1992, month=7` → `31`',
                 '本视频：`year=2000, month=2` → `29`'],
        quote='比较基础的题目，注意不要遗漏了闰年二月的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用数组按平年查出每月天数',
              '只有二月会受闰年影响，闰年时加 1',
              '闰年：能被 400 整除，或能被 4 整除但不能被 100 整除'],
        after=[dict(heading='闰年对照', lines=['`2000`：能被 400 整除 → ==闰年==，二月 29 天', '`1900`：能被 100 整除但不能被 400 整除 → ==平年==，二月 28 天', '`2024`：能被 4 整除、不能被 100 整除 → ==闰年==', '`2023`：不能被 4 整除 → 平年'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：1900 年不是闰年，2000 年是闰年',
                 '原文为 Python 2 风格，此题无需改动，直接可运行'],
    ),
)
