def _cur(S):
    m = S.get('meetings')
    if 's' not in S or 'e' not in S or not m:
        return None
    for k, p in enumerate(m):
        if p[0] == S['s'] and p[1] == S['e']:
            return k
    return None


def _cmp(S):
    if 'end' not in S or 's' not in S:
        return ''
    return f"当前会议 `[{S['s']}, {S['e']}]`　　合并区间 `[{S['start']}, {S['end']}]`　　剩余 `days = {S['days']}`"


def _if_cap(S, B, ret):
    s, end = S.s, S.end
    if s > end:
        return f'`s = {s}` > 合并区间右端点 `{end}`：==不相交==，中间有空档，先把合并区间长度扣掉'
    return f'`s = {s}` ≤ 合并区间右端点 `{end}`：相交，继续合并'


CONFIG = dict(
    num=3169, title='无需开会的工作日', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='正难则反 · 合并区间', tags=['贪心算法', '区间贪心', '难度分 1483'],
    code='''
class Solution:
    def countDays(self, days: int, meetings: List[List[int]]) -> int:
        meetings.sort(key=lambda p: p[0])  # 按照左端点从小到大排序
        start, end = 1, 0  # 当前合并区间的左右端点
        for s, e in meetings:
            if s > end:  # 不相交
                days -= end - start + 1  # 当前合并区间的长度
                start = s  # 下一个合并区间的左端点
            end = max(end, e)
        days -= end - start + 1  # 最后一个合并区间的长度
        return days
''',
    call='Solution().countDays(12, [[5, 7], [1, 3], [9, 10], [2, 4], [11, 11]])',
    expect=2,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='meetings', pointer=_cur, label='数轴：会议（黄 = 当前 s,e）', h=420),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), ('s', 's', 'yellow'), ('e', 'e', 'yellow'), ('days', 'days', 'green')],
    captions={
        'meetings.sort': '按左端点排序：`{meetings}`。这样合并区间只需看右端点',
        'start, end = 1, 0': '合并区间初始为空：`start = 1, end = 0`，长度 `end - start + 1 = 0`',
        'for s, e in meetings': lambda S, B, r: ('所有会议都看完了，退出循环' if B.get('s') == S.s and B.get('e') == S.e else f'看下一个会议 `[{S.s}, {S.e}]`'),
        'if s > end': _if_cap,
        'days -= end - start + 1': '正难则反：`days` 减去合并区间 `[{B.start}, {B.end}]` 的长度 `{B.end - B.start + 1}` → =={days}==',
        'start = s': '开始新的合并区间，左端点 `start = {start}`',
        'end = max': '右端点 `max({B.end}, {e}) = {end}`（被完全包含时右端点不变）',
        'return days': '剩下的 `{ret}` 天没有会议',
    },
    cards=dict(
        one_liner='正难则反：总天数减去有会议的天数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['员工从第 1 天到第 `days` 天可工作；每个会议 `[start, end]` 占用闭区间，会议可能重叠',
                 '求没有任何会议的天数',
                 '示例：`days = 10, meetings = [[5,7],[1,3],[9,10]]` → `2`（第 4、8 天）',
                 '本视频：`days = 12`，5 个会议 → `2`'],
        quote='正难则反，答案等于 days 减「有会议安排的天数」。……由于本题只需计算合并区间的长度，所以只需记录当前合并区间的左右端点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接数空闲天很麻烦，反过来数==有会议的天数==',
              '会议按左端点排序，同 56 题合并区间：相交就延长右端点',
              '合并区间一旦固定，就把它的长度 `end - start + 1` 从 `days` 里扣掉'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`（不计排序栈）',
                 '`start, end = 1, 0` 让第一个区间前的空段长度为 0，不用特判',
                 '循环结束后别忘了扣最后一个合并区间',
                 '`s > end` 才算不相交：端点相接（`s == end`）仍可合并；同类题：56. 合并区间'],
    ),
)
