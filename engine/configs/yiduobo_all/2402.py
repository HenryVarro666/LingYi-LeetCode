CONFIG = dict(
    num=2402, title='会议室 III', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='三个堆：idle / min_time / pending',
    tags=['灵神题单', '堆', '难度分 2093'],
    code='''
class Solution(object):
    def mostBooked(self, n, meetings):

        meetings.sort(key=lambda d:d[0])
        idle = list(range(n))
        min_time = []
        pending = []

        def start_meeting(idle, cnt, pending, min_time, now):
            room = heapq.heappop(idle)
            cnt[room] += 1
            meeting_info = heapq.heappop(pending)
            heapq.heappush(min_time, [now + meeting_info[1] - meeting_info[0], room])

        cnt = [0] * n
        for start_time, end_time in meetings:
            while min_time and min_time[0][0] <= start_time:
                now, num = heapq.heappop(min_time)
                heapq.heappush(idle, num)
                if pending:
                    start_meeting(idle, cnt, pending, min_time, now)
            
            heapq.heappush(pending, [start_time, end_time])
            if idle:
                start_meeting(idle, cnt, pending, min_time, start_time)

        while pending:
            if not idle:
                now = min_time[0][0]
                while min_time and min_time[0][0] == now:
                    _, num = heapq.heappop(min_time)
                    heapq.heappush(idle, num)
            
            start_meeting(idle, cnt, pending, min_time, now)
        
        res = 0
        for index in range(1, n):
            if cnt[index] > cnt[res]:
                res = index
        
        return res
''',
    call='Solution().mostBooked(2, [[0,5],[1,3],[2,6],[6,9],[7,8]])',
    expect=1,
    views=[
        dict(type='array', var=lambda S: [f'[{a},{b})' for a, b in S['meetings']], label='meetings（已排序）', cell=100, h=190,
             color=lambda S, i, v: 'yellow' if 'start_time' in S and v.startswith(f"[{S['start_time']},") else None),
        dict(type='heap', var='idle', label='idle：空闲房间号', top_color='green', h=110),
        dict(type='heap', var='min_time', fmt=lambda x: f'房{x[1]}·{x[0]}', label='min_time：房间·完结时间', top_color='pink', h=110),
        dict(type='heap', var='pending', fmt=lambda x: f'[{x[0]},{x[1]})', label='pending：延期的会议（原定时间）', top_color='orange', h=110),
        dict(type='array', var='cnt', label='cnt：各房间开会次数', cell=90, h=160,
             color=lambda S, i, v: 'green' if v == max(S['cnt']) and v > 0 else None),
    ],
    watch=[('start_time', 'start_time', 'blue'), ('now', 'now', 'orange'), ('room', 'room', 'pink')],
    skip=['cnt[room] += 1', 'heapq.heappush(idle, num)'],
    captions={
        'meetings.sort': '按起始时间从小到大排序，一趟遍历',
        'idle = list': '`idle`：没被占用的房间，最小堆，堆顶 = 编号最小',
        'min_time = []': '`min_time`：正在开的会（完结时间，房间号），堆顶 = 最早完结',
        'pending = []': '`pending`：延期的会议（原定开始，原定结束），堆顶 = 原定最早',
        'def start_meeting': '把「开会」抽成函数：取最小的空闲房间，安排 `pending` 里原定最早的会议',
        'room = heapq.heappop(idle)': '取编号最小的空闲房间 `{room}`',
                'meeting_info = ': '取出 `pending` 里原定最早的会议 `{meeting_info}`',
        'heapq.heappush(min_time': lambda S, B, r: f'从 `{S.now}` 开始，时长 `{S.meeting_info[1]} − {S.meeting_info[0]}` → 在 `{S.now + S.meeting_info[1] - S.meeting_info[0]}` 完结，房间 `{S.room}` 入 `min_time`',
        'cnt = [0]': '`cnt[i]`：房间 `i` 的开会次数',
        'for start_time, end_time': lambda S, B, r: (f'处理会议 `[{S.start_time}, {S.end_time})`' if B.get('start_time') != S.start_time else '会议都遍历完了'),
        'while min_time and min_time[0][0] <= start_time': lambda S, B, r: (
            f'`min_time` 堆顶 `房{S.min_time[0][1]}` 在 `{S.min_time[0][0]}` 完结，≤ start `{S.start_time}` → 先释放' if S.min_time and S.min_time[0][0] <= S.start_time
            else ('没有已完结的会议' if not S.min_time else f'最早完结 `{S.min_time[0][0]}` > start `{S.start_time}`，没有房间可释放')),
        'now, num = heapq.heappop(min_time)': '会议在 `now = {now}` 完结，房间 `{num}` 空出来，回到 `idle`',
                'if pending:': lambda S, B, r: ('有延期会议在等 → 房间一空出来就给它，开始时间就是 `now`' if S.pending else '没有延期会议，房间留在 `idle`'),
        'start_meeting(idle, cnt, pending, min_time, now)': '立刻在 `now = {now}` 安排 `pending` 里最早的会议',
        'heapq.heappush(pending, [start_time, end_time])': '新会议先进 `pending`：`[{start_time}, {end_time})`（正常开会也走这一条，统一处理）',
        'if idle:': lambda S, B, r: ('有空闲房间 → 让 `pending` 堆顶开会' if S.idle else '没有空闲房间 → 会议留在 `pending` 里等'),
        'start_meeting(idle, cnt, pending, min_time, start_time)': '在 `start_time = {start_time}` 开会',
        'while pending': lambda S, B, r: (f'遍历结束，`pending` 里还剩 `{len(S.pending)}` 场在等' if S.pending else '`pending` 清空了'),
        'if not idle': lambda S, B, r: ('房间全被占 → 等最早完结的那批' if not S.idle else '还有空闲房间，直接安排'),
        'now = min_time[0][0]': '最早完结时间 `now = {now}`',
        'while min_time and min_time[0][0] == now': '同一时刻完结的会议室全部释放',
        '_, num = heapq.heappop(min_time)': '释放房间 `{num}`',
        'res = 0': '`res`：目前开会最多的房间，次数相同保留编号小的',
        'if cnt[index] > cnt[res]': '`cnt[{index}] = {cnt[index]}` 对比 `cnt[{res}] = {cnt[res]}`：==严格大于==才换',
        'res = index': '更新 `res = {res}`',
        'return res': '开会最多的房间 `{res}`',
    },
    cards=dict(
        one_liner='三个堆分工：空闲房间、进行中的会、延期的会',
        complexity='时间 `O(m log m + m log n)`，空间 `O(n + m)`',
        problem=['`n` 个会议室，会议 `[start, end)`：用编号最小的空闲房，没有就延期',
                 '延期会议持续时间不变，空出房间后==原定开始最早==的先开',
                 '示例：`n=2`，`[[0,10],[1,5],[2,7],[3,4]]` → `0`',
                 '本视频：`n=2`，`[[0,5],[1,3],[2,6],[6,9],[7,8]]` → `1`'],
        quote='综合起来，就是三个堆idle，min_time和pending，具体作用如上所述。其中idle初始化为[0, 1, ..., n - 1]，即一开始所有会议室都是空闲的',
        quote_src='—— yiduobo 题解原文',
        idea=['`idle`：空闲房间取最小编号；`min_time`：进行中的会，取最早完结；`pending`：延期的会，取原定最早',
              '房间空出的瞬间，若 `pending` 非空，立刻安排它，开始时间 = 该房间完结时间',
              '遍历完还有等待的会，就逐批释放最早完结的房间，直到清空'],
        summary=['时间 `O(m log m + m log n)`，空间 `O(n + m)`',
                 '延期会议的新完结时间 = `now + 原结束 − 原开始`',
                 '遍历后别忘了清空 `pending`，`idle` 为空时先释放同一时刻完结的全部房间',
                 '原文为 Python 2 写法，`idle = range(n)` 在 Python 3 里不能当堆用，已改为 `list(range(n))`',
                 '对比灵神：灵神 2 个堆、延期时直接顺延 `end`；yiduobo 多一个 `pending` 堆显式排队'],
    ),
)
