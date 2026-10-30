CONFIG = dict(
    num=1507, title='转变日期格式', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字符串拆分 + 月份映射', tags=[],
    code='''
class Solution(object):
    def reformatDate(self, date):

        day, month, year = date.split(' ')
        
        month_dict = {'Jan': 1,
                      'Feb': 2,
                      'Mar': 3,
                      'Apr': 4,
                      'May': 5,
                      'Jun': 6,
                      'Jul': 7,
                      'Aug': 8,
                      'Sep': 9,
                      'Oct': 10,
                      'Nov': 11,
                      'Dec': 12}

        if day[1] >= '0' and day[1] <= '9':
            day = int(day[:2])
        else:
            day = int(day[0])

        month = month_dict[month]
        
        return '%s-%02d-%02d' % (year, month, day)
''',
    call="Solution().reformatDate('6th Jun 1933')",
    expect='1933-06-06',
    views=[
        dict(type='string', var='date', h=130, label='date'),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"day=`{S['day']}`　month=`{S['month']}`　year=`{S['year']}`" if 'year' in S else '')),
        dict(type='map', var='month_dict', h=330, font=22),
    ],
    skip=["'Feb'","'Mar'","'Apr'","'May'","'Jun'","'Jul'","'Aug'","'Sep'","'Oct'","'Nov'","'Dec'"],
    watch=['day', 'month', 'year'],
    captions={
        'date.split': '按空格拆成三段：`day = {day}`，`month = {month}`，`year = {year}`',
        'month_dict = {': '建月份表：英文缩写 → 数字',
        'day[1] >=': lambda S, B, r: (f"看 `day[1] = '{S.day[1]}'`：" + ('是数字 → 日期是两位，如 `12th`' if '0' <= S.day[1] <= '9'
                                      else '是字母 → 日期只有一位，如 `6th`')),
        'day = int(day[:2])': '两位日期：取前两位转整数 → `{day}`',
        'day = int(day[0])': '一位日期：只取第一个字符转整数 → `{day}`（去掉 `th`）',
        'month = month_dict': '查表：`{B.month}` → `{month}`',
        'return': lambda S, B, r: f'`%02d` ==补前导 0==：月 `{S.month}` → `{S.month:02d}`，日 `{S.day}` → `{S.day:02d}`，拼成 `{r}`',
    },
    cards=dict(
        one_liner='拆开、查月份、补前导零，再按年-月-日拼起来',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['日期形如 `"20th Oct 2052"`：日带 `st/nd/rd/th`，月是英文缩写',
                 '转成 `YYYY-MM-DD` 格式',
                 '示例：`"20th Oct 2052"` → `"2052-10-20"`；本视频 `"6th Jun 1933"` → `"1933-06-06"`'],
        quote='比较基础的题目，直接按对应的月份和日期转换即可。需要注意个位数月份和天数的前导0不要丢了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split(\' \')` 得到日、月、年三段',
              '日期字符串第二个字符是数字就取两位，否则取一位',
              '月份用字典换成数字，最后用 `%02d` 补零'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：==个位数的月和日要补 0==，`%02d` 搞定',
                 '判断日期位数看 `day[1]`：`6th` 的第二个字符是字母',
                 '原文为 Python 2 写法，在 Python 3 下无需改动'],
    ),
)
