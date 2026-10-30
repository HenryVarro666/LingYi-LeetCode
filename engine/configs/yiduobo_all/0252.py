def _txt(S):
    if 'max_end' not in S:
        return ''
    if 'start' in S and 'end' in S:
        return f"`max_end = {S['max_end']}`，当前区间 `[{S['start']}, {S['end']}]`：`start {S['start']} {'<' if S['start'] < S['max_end'] else '≥'} max_end {S['max_end']}`"
    return f"`max_end = {S['max_end']}`（排序后第一个区间的右端点）"


CONFIG = dict(
    num=252, title='会议室', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按 start 排序 · 维护 max_end',
    code='''
class Solution(object):
    def canAttendMeetings(self, intervals):

        if not intervals:
            return True

        intervals.sort(key=lambda d:d[0])
        max_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start < max_end:
                return False
            max_end = max(end, max_end)
        
        return True
''',
    call='Solution().canAttendMeetings([[9, 12], [0, 3], [4, 6], [5, 8]])',
    expect=False,
    views=[
        dict(type='intervals', var='intervals', pointer="intervals.index([start, end]) if 'start' in dir() else None", h=330),
        dict(type='text', fn=_txt, size=30, h=70),
    ],
    watch=[('max_end', 'max_end', 'cyan'), ('start', 'start', 'blue'), ('end', 'end', 'pink')],
    captions={
        'if not intervals': '没有会议，当然能参加：先排除空输入',
        'intervals.sort': '按 `start` 从小到大排序：这样只需和前面的会议比较',
        'max_end = intervals[0][1]': '`max_end` = 前面所有区间里最大的 `end` = =={max_end}==',
        'for start, end': '取下一个区间 `[{start}, {end}]`',
        'if start < max_end': lambda S, B, ret: (f"`start = {S.start} < max_end = {S.max_end}`：前面有会议还没结束，这个就开始了 → ==相交=="
                                                  if S.start < S.max_end else f"`start = {S.start} ≥ max_end = {S.max_end}`：前面的会议都结束了 → 不相交"),
        'return False': '有两场会议重叠 → 返回 `False`',
        'max_end = max(end, max_end)': '用当前区间更新：`max_end = max({end}, {B.max_end}) = {max_end}`',
        'return True': '全部不相交 → `True`',
    },
    cards=dict(
        one_liner='排序后只看当前开始时间有没有早于之前最大的结束时间',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['给定会议时间区间 `[start, end]`，问一个人能否参加全部会议',
                 '也就是==任意两个区间都不相交==',
                 '示例：`[[0,30],[5,10],[15,20]]` → `False`'],
        quote='对于区间i和区间j，不妨设start[i] >= start[j]，那么当end[j] > start[i]时，这两个区间才会相交。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按 `start` 排序，区间 `i` 只需要和排在前面的 `j` 比',
              '前面所有 `end` 里最大的是 `max_end`；`start < max_end` 就必然和某个前面的区间相交',
              '不相交就用当前 `end` 更新 `max_end`，继续向后'],
        summary=['排序 `O(n log n)`，遍历 `O(n)`',
                 '易错：比较的是 ==start < max_end==；`start == max_end` 首尾相接不算相交',
                 '`max_end` 要取 `max`，不能直接用上一个区间的 `end`',
                 '原文为 Python 3 可运行写法，代码未改动',
                 '延伸：253 会议室 II 求最少需要几间'],
    ),
)
