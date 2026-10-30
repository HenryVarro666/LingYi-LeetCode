CONFIG = dict(
    num=731, title='我的日程安排表 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='端点扫描计数 · 起点×2、终点×2−1',
    tags=['设计'],
    code='''
class MyCalendarTwo(object):

    def __init__(self):
        self.time_list = []

    def book(self, start, end):
        self.time_list.append(start * 2)
        self.time_list.append(end * 2 - 1)

        cnt = 0
        for time_point in sorted(self.time_list):
            if time_point & 1:
                cnt -= 1
            else:
                cnt += 1
                if cnt > 2:
                    self.time_list.pop()
                    self.time_list.pop()
                    return False

        return True
''',
    call='''c = MyCalendarTwo()
res = [c.book(10, 20), c.book(50, 60), c.book(10, 40), c.book(5, 15)]
res''',
    expect=[True, True, True, False],
    views=[
        dict(type='text', h=60, fn=lambda S: (f"本次预定 [{S['start']}, {S['end']})，端点 ==`{S['start']*2}`== 和 ==`{S['end']*2-1}`==" if 'start' in S and 'end' in S else '')),
        dict(type='array', var='self.time_list', label='time_list（奇数 = 终点，偶数 = 起点）', h=170,
             color=lambda S, i, v: 'pink' if v % 2 else 'blue'),
        dict(type='array', var=lambda S: sorted(S['self.time_list']) if 'self.time_list' in S else [], label='sorted(time_list)：按时间轴从左到右扫描', h=170,
             color=lambda S, i, v: ('yellow' if S.get('time_point') == v and S.get('cnt', 0) > 2 else ('pink' if v % 2 else 'blue'))),
        dict(type='text', h=70, fn=lambda S: (f"计数器 cnt = ==`{S['cnt']}`==（同时进行的预定数）" + ('，超过 2 → 三重预定！' if S['cnt'] > 2 else '')) if 'cnt' in S else ''),
        dict(type='calls', h=100),
    ],
    watch=['start', 'end', 'time_point', ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    skip=['self.time_list = []'],
    captions={
        'self.time_list.append(start * 2)': '起点放 `{start}*2 = {start*2}`（偶数 = 起点）',
        'self.time_list.append(end * 2 - 1)': '终点放 `{end}*2-1 = {end*2-1}`（奇数）：[x,y) 的 y 不含，所以比 y 的起点早一格',
        'cnt = 0': '把所有端点排序，从左往右数：==遇到起点 +1，遇到终点 −1==',
        'for time_point in sorted': '处理时间点 `{time_point}`',
        'if time_point & 1': lambda S, B, ret: ('`{}` 是奇数 → 终点'.format(S.time_point) if S.time_point & 1 else '`{}` 是偶数 → 起点'.format(S.time_point)),
        'cnt -= 1': '一个预定结束，`cnt` = {cnt}',
        'cnt += 1': '一个预定开始，`cnt` = {cnt}',
        'if cnt > 2': lambda S, B, ret: ('`cnt = {}` > 2 → 同时有三个预定，==非法=='.format(S.cnt) if S.cnt > 2 else '`cnt = {}` ≤ 2，还没有三重预定'.format(S.cnt)),
        'self.time_list.pop()': '撤销刚加入的端点（先删终点，再删起点）',
        'return False': '这次预定会造成三重预定 → 返回 ==False==，time_list 恢复原样',
        'return True': '扫完 `cnt` 从未超过 2 → 预定成功，返回 ==True==',
    },
    max_steps=110,
    cards=dict(
        one_liner='每次预定是时间轴上的两个点，扫一遍数同时有几个',
        complexity='每次 `book` 排序 `O(n log n)`，总计 `O(n^2 log n)`；空间 `O(n)`',
        problem=['`book(start, end)` 预定半开区间 `[start, end)`',
                 '若这次预定会让某个时刻==有三个预定重叠==，返回 `False` 且不加入',
                 '示例：`[10,20) [50,60) [10,40)` 成功，`[5,15)` 失败'],
        quote='我们假想出一条时间轴，那么每次预定就是在这个时间轴上设置了两个点。……若某个时刻计数器超过了2，说明此时有三个预定同时发生，是非法情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个预定拆成起点（+1）和终点（−1）两个事件，排序后从左扫到右',
              '计数器超过 2 就说明三重预定，把刚加的两个点 `pop` 掉',
              '小技巧：起点 ×2、终点 ×2−1，让 `[x,y)` 和 `[y,z)` 在 y 处不会误判相交（终点排在同值起点之前）'],
        summary=['每次 `book` 排序 `O(n log n)`，共 n 次 → `O(n^2 log n)`；作者说用二分插入可做到 `O(n^2)`',
                 '易错：终点用 `end*2-1`，否则 `[10,20)` 与 `[20,30)` 在 20 处会被误判重叠',
                 '失败时要把两个端点都 `pop`，否则会污染之后的判断',
                 '对比 729（日程 I，不许重叠）、732（日程 III，求最大重叠数）'],
    ),
)
