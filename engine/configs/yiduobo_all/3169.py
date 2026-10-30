def _cur(S):
    m = S.get('meetings')
    if 'start' not in S or 'end' not in S or not m:
        return None
    for k, p in enumerate(m):
        if p[0] == S['start'] and p[1] == S['end']:
            return k
    return None


def _cmp(S):
    if 'y' not in S:
        return ''
    return f"当前考察区间 `[{S['x']}, {S['y']}]`　　已累计空闲天数 `res = {S['res']}`"


def _if_cap(S, B, ret):
    if S.start <= S.y:
        return f'`start = {S.start}` ≤ `y = {S.y}`：==重叠==，只需看终点能否延长'
    return f'`start = {S.start}` > `y = {S.y}`：不重叠，后面的起点更大，`[x, y]` 不会再被碰到'


CONFIG = dict(
    num=3169, title='无需开会的工作日', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 累加区间间隔', tags=['贪心算法', '区间贪心', '难度分 1483'],
    code='''
class Solution(object):
    def countDays(self, days, meetings):

        meetings.sort()
        x, y = meetings[0]
        res = x - 1
        for start, end in meetings[1:]:
            if start <= y:
                y = max(y, end)
            else:
                res += start - y - 1
                x, y = start, end

        res += days - y
    
        return res
''',
    call='Solution().countDays(12, [[5, 7], [1, 3], [9, 10], [2, 4], [11, 11]])',
    expect=2,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='meetings', pointer=_cur, label='数轴：会议（黄 = 当前 start,end）', h=420),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('start', 'start', 'yellow'), ('end', 'end', 'yellow'), ('res', 'res', 'green')],
    captions={
        'meetings.sort': '按起点从小到大排序：`{meetings}`',
        'x, y = meetings[0]': '第一个会议作为当前区间 `[x, y] = [{x}, {y}]`',
        'res = x - 1': '第一场会议前的 `{x - 1}` 天都空闲 → `res = {res}`',
        'for start, end': lambda S, B, r: ('所有会议都看完了，退出循环' if B.get('start') == S.start and B.get('end') == S.end else f'看下一个会议 `[{S.start}, {S.end}]`'),
        'if start <= y': _if_cap,
        'y = max': '终点取 `max({B.y}, {end}) = {y}`',
        'res += start - y - 1': '两段之间的空档 `start - y - 1 = {start - B.y - 1}` 天加入答案 → `res = {res}`',
        'x, y = start, end': '`[x, y]` 换成新区间 `[{x}, {y}]`',
        'res += days - y': '最后一场会议后还有 `days - y = {days - y}` 天 → `res = {res}`',
        'return res': '没有会议的天数是 `{ret}`',
    },
    cards=dict(
        one_liner='排序合并区间，把相邻区间之间的空档累加起来',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给出 `days` 和若干会议区间 `[start, end]`（闭区间，可重叠）',
                 '问第 1 天到第 `days` 天里，有几天没有会议',
                 '示例：`days = 5, meetings = [[2,4],[1,3]]` → `1`',
                 '本视频：`days = 12`，5 个会议 → `2`'],
        quote='非常标准的区间合并问题，先将meeting按start从小到达排序，然后一趟遍历。过程中使用一组变量[x, y]记录当前考察的区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`y >= start`：区间重叠，终点更新为 `max(y, end)`',
              '`y < start`：不重叠，间隔 `start - y - 1` 天直接计入答案，`[x, y]` 换成新区间',
              '头尾也别漏：第一场前 `x - 1` 天，最后一场后 `days - y` 天'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '空档是 `start - y - 1`，两端的天数不能算进去',
                 '循环外要补上最后一场会议之后的 `days - y`',
                 '`meetings.sort()` 默认按 `(start, end)` 排序，起点相同也没问题',
                 '同类题：56. 合并区间'],
    ),
)
