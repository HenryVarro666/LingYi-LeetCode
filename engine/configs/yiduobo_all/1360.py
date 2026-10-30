def _txt(S):
    if 'year' not in S:
        return '把两个日期都换算成「距 1971-01-01 过了多少天」，再相减取绝对值'
    y, mo, d = S['year'], S['month'], S['day']
    cnt = S.get('cnt')
    if cnt is None:
        return f'日期 `{y}-{mo:02d}-{d:02d}` → 年 `{y}`，月 `{mo}`，日 `{d}`'
    line = S.get('_line')
    if 'm_cnt' not in S:
        if 'y' in S and line in (8, 9, 10):
            leap = S['y'] % 400 == 0 or (S['y'] % 4 == 0 and S['y'] % 100 != 0)
            return f'累加整年：`{S["y"]}` 年有 `{366 if leap else 365}` 天，当前 `cnt = {cnt}`'
        return f'先累加 `1971 ~ {y - 1}` 年的整年天数，当前 `cnt = {cnt}`'
    return f'`{y}` 年{"==是闰年==，二月 29 天" if S["m_cnt"][2] == 29 else "不是闰年，二月 28 天"}；已累计 `cnt = {cnt}`'


def _leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)


CONFIG = dict(
    num=1360, title='日期之间隔几天', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='换算成距 1971-01-01 的天数',
    tags=[],
    code='''
class Solution(object):
    def daysBetweenDates(self, date1, date2):

        return abs(self.get_cnt(date1) - self.get_cnt(date2))
    
    def get_cnt(self, date):
        year, month, day = [int(x) for x in date.split('-')]
        cnt = 0
        for y in range(1971, year):
            cnt += 365
            if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
                cnt += 1
        
        m_cnt = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            m_cnt[2] += 1
        
        for m in range(1, month):
            cnt += m_cnt[m]
        
        cnt += day
        return cnt
''',
    call="Solution().daysBetweenDates('1972-03-01', '1971-01-15')",
    expect=411,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='m_cnt', label='每月天数 m_cnt（下标 = 月份，m_cnt[0] 占位）',
             pointers={'m': 'blue'},
             color=lambda S, i, v: 'orange' if i == 2 and v == 29 else None,
             dim=lambda S, i, v: i == 0, cell=64, h=200),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('year', 'year', 'blue'), ('month', 'month', 'pink'), ('day', 'day', 'yellow'), ('cnt', 'cnt', 'green')],
    captions={
        'return abs(': '分别算 `{date1}` 和 `{date2}` 的天数（调用 `get_cnt`），算完相减取绝对值',
        'year, month, day = ': '拆开 `{date}`：`{year}` 年 `{month}` 月 `{day}` 日',
        'cnt = 0': '`cnt` = 这个日期是 1971-01-01 起算的第几天，先从 0 开始',
        'for y in range(1971, year)': lambda S, B, r: (f'整年部分处理完：`1971 ~ {S.year - 1}` 年共 `{S.cnt}` 天' if 'y' in B and S.y == B.y and S.cnt == B.cnt
                                                       else (f'`y = {S.y}`：这一整年要计入' if 'y' in S and S.y < S.year else '年份不到 `year`，没有整年要计')),
        'cnt += 365': '`{y}` 年至少 365 天：`cnt` = {cnt}',
        'if y % 400 == 0': lambda S, B, r: (f'`{S.y}` 是闰年（能被 4 整除且不被 100 整除，或被 400 整除）→ 多一天'
                                            if (S.y % 400 == 0 or (S.y % 4 == 0 and S.y % 100 != 0)) else f'`{S.y}` 不是闰年'),
        'cnt += 1': '闰年多一天：`cnt` = {cnt}',
        'm_cnt = [0': '平年每月天数，`m_cnt[月份]`，下标 0 不用',
        'if year % 400 == 0': lambda S, B, r: (f'`{S.year}` 年是闰年 → 二月要加一天' if (S.year % 400 == 0 or (S.year % 4 == 0 and S.year % 100 != 0))
                                               else f'`{S.year}` 年不是闰年，二月保持 28 天'),
        'm_cnt[2] += 1': '闰年二月 29 天：`m_cnt[2] = {m_cnt[2]}`',
        'for m in range(1, month)': lambda S, B, r: (f'前面的整月处理完：`cnt = {S.cnt}`' if 'm' in B and S.m == B.m and S.cnt == B.cnt
                                                      else (f'`m = {S.m}`：这个月已经过完，整月计入' if 'm' in S and S.m < S.month else f'`month = {S.month}`，没有整月要计')),
        'cnt += m_cnt[m]': '加上 {m} 月的 `{m_cnt[m]}` 天：`cnt` = =={cnt}==',
        'cnt += day': '再加本月已过的 `{day}` 天：`cnt` = =={cnt}==',
        'return cnt': '`{date}` 是 1971-01-01 起算的第 =={ret}== 天',
    },
    cards=dict(
        one_liner='都数成「距 1971-01-01 的天数」，两数一减',
        complexity='时间 `O(年数 + 12)`，空间 `O(1)`',
        problem=['给两个 `YYYY-MM-DD` 格式的日期（都晚于 1971-01-01），返回相隔多少天',
                 '例：`2019-06-29` 与 `2019-06-30` → `1`',
                 '本视频：`1972-03-01` 与 `1971-01-15` → `411`'],
        quote='注意到题目给出的两个日期都大于1971年1月1日，因此我选择分别计算两个日期到1971年1月1日的间隔日期数目，然后相减得出答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`get_cnt`：先累加 `1971` 到上一年的整年天数，闰年 366',
              '再加本年已经过完的整月天数（闰年二月 29 天）',
              '最后加上日；两个日期的 `cnt` 相减取绝对值'],
        summary=['时间 `O(年数)`，空间 `O(1)`',
                 '易错：闰年判断是「被 400 整除，或被 4 整除但不被 100 整除」',
                 '月份循环只加「前 month−1 个月」，再单独加 `day`',
                 '两个日期不保证谁先谁后，所以最后要 `abs`'],
    ),
)
