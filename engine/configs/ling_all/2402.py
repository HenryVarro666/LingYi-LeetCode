CONFIG = dict(
    num=2402, title='会议室 III', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='两个最小堆：空闲房间 + 使用中房间',
    tags=['灵神题单', '堆', '难度分 2093'],
    code='''
class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort(key=lambda m: m[0])

        idle = list(range(n))  # 会议室编号
        using = []  # (结束时间，会议室编号)
        cnt = [0] * n  # 会议室的开会次数

        for start, end in meetings:
            # 在 start 时刻空出来的会议室
            while using and using[0][0] <= start:
                heappush(idle, heappop(using)[1])

            if idle:  # 有空闲的会议室
                i = heappop(idle)
            else:  # 没有空闲的会议室
                e, i = heappop(using)  # 弹出一个最早结束的会议室（若有多个同时结束，弹出编号最小的会议室）
                end += e - start  # 更新当前会议的结束时间

            heappush(using, (end, i))  # 使用一个会议室
            cnt[i] += 1

        return cnt.index(max(cnt))
''',
    call='Solution().mostBooked(2, [[0,5],[1,3],[2,6],[6,9],[7,8]])',
    expect=1,
    views=[
        dict(type='array', var=lambda S: [f'[{a},{b})' for a, b in S['meetings']], label='meetings（已排序）', cell=100, h=200,
             color=lambda S, i, v: 'yellow' if 'start' in S and v.startswith(f"[{S['start']},") else None),
        dict(type='heap', var='idle', label='idle：空闲房间号', top_color='green', h=130),
        dict(type='heap', var='using', fmt=lambda x: f'房{x[1]}·{x[0]}', label='using：房间·结束时间', top_color='pink', h=130),
        dict(type='array', var='cnt', label='cnt：各房间开会次数', cell=100, h=170,
             color=lambda S, i, v: 'green' if v == max(S['cnt']) and v > 0 else None),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'orange'), ('i', 'i', 'pink')],
    captions={
        'meetings.sort': '按开始时间排序，才能==按时间顺序==模拟开会',
        'idle = list': '`idle`：最小堆，堆顶 = 编号最小的空闲房间',
        'using = []': '`using`：最小堆，按（结束时间，编号）排，堆顶 = 最早结束的房间',
        'cnt = [0]': '`cnt[i]` 统计房间 `i` 开了几场会',
        'for start, end': lambda S, B, r: (f'处理会议 `[{S.start}, {S.end})`' if [S.start, S.end] in S.meetings else '会议都处理完了'),
        'while using and': lambda S, B, r: (f'`using` 堆顶 `房{S.using[0][1]}` 在 `{S.using[0][0]}` 结束，≤ start `{S.start}` → 已空出来' if S.using and S.using[0][0] <= S.start
                                            else ('`using` 为空，没有会议室要释放' if not S.using else f'`using` 堆顶结束时间 `{S.using[0][0]}` > start `{S.start}`，没有更多空出来的')),
        'heappush(idle, heappop(using)[1])': '把到期的房间还回 `idle`：`idle` = {idle}（房间在两个堆之间来回倒）',
        'if idle': lambda S, B, r: (f'有空闲房间 `{S.idle}` → 成立，会议准点开始' if S.idle else '没有空闲房间 → 会议只能延期，等最早结束的那间'),
        'i = heappop(idle)': '用编号最小的空闲房间 `{i}`',
        'e, i = heappop(using)': '没人空着：等最早结束的房间 `{i}`，它在 `{e}` 结束（同时结束取编号小的）',
        'end += e - start': '等了 `{e} - {start}` = `{e - start}`，时长不变，新结束时间 `end` = =={end}==',
        'heappush(using, (end, i))': '房间 `{i}` 占用到 `{end}`，入 `using`',
        'cnt[i] += 1': '房间 `{i}` 又开了一场：`cnt` = {cnt}',
        'return cnt.index': '开会最多的是 `cnt.index(max(cnt))`：次数相同取编号小的 → 房间 =={ret}==',
    },
    cards=dict(
        one_liner='空闲房间一个堆，使用中房间一个堆，按时间顺序模拟',
        complexity='时间 `O(m log m + n + m log n)`，空间 `O(n)`',
        problem=['`n` 个会议室，会议 `[start, end)`：用编号最小的空闲房，没有就延期到有房空出',
                 '延期会议持续时间不变，返回开会最多的房间（并列取编号小）',
                 '示例：`n=2`，`[[0,10],[1,5],[2,7],[3,4]]` → `0`',
                 '本视频：`n=2`，`[[0,5],[1,3],[2,6],[6,9],[7,8]]` → `1`'],
        quote='这两类会议室是互补关系，伴随着会议的开始和结束，会议室在这两类中来回倒',
        quote_src='—— 灵茶山艾府题解',
        idea=['`idle` 堆：空闲房间编号，取最小；`using` 堆：（结束时间，编号），取最早结束',
              '每个会议先把 `using` 里 ≤ start 的房间倒回 `idle`',
              '有空房就用；没有就弹 `using` 堆顶，`end += e - start` 顺延'],
        summary=['时间 `O(m log m + n + m log n)`，空间 `O(n)`',
                 '`<= start` 要带等号：半开区间，结束那刻房间就空了',
                 '无空房时直接顺延 `end`，不需要另存等待队列：开始时间互不相同，按序处理即可',
                 '相似题：1882 使用服务器处理任务、1606 找到处理最多请求的服务器'],
    ),
)
