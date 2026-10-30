CONFIG = dict(
    num=1353, title='最多可以参加的会议数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按开始时间排序 + 结束时间最小堆',
    tags=['灵神题单', '难度分 2016'],
    code='''
class Solution(object):
    def maxEvents(self, events):

        n = len(events)
        events = sorted(events, key=lambda d:d[0])
        heap = []

        max_t = 0
        for index in range(n):
            max_t = max(max_t, events[index][1])

        t = 1
        p = 0
        res = 0
        while t <= max_t:
            while p < n and events[p][0] <= t:
                heapq.heappush(heap, events[p][1])
                p += 1

            while heap:
                if heap[0] >= t:
                    break
                heapq.heappop(heap)

            if heap:
                res += 1
                heapq.heappop(heap)
            else:
                if p == n:
                    break

            t += 1

        return res
''',
    call='Solution().maxEvents([[1,2],[1,2],[1,2],[2,3]])',
    expect=3,
    views=[
        dict(type='intervals', var='events', pointer='p', label='events（按开始时间排序；黄 = 下一个待加入的会议 p）', h=230),
        dict(type='heap', var='heap', fmt=lambda x: f'第{x}天结束', label='heap（已开始的会议的结束日，最小的在堆顶）', h=150),
        dict(type='text', fn=lambda S: (f"今天是第 ==`{S['t']}`== 天，已参加 `{S['res']}` 场" if 't' in S and 'res' in S else ''), h=80),
    ],
    watch=[('t', 't', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green'), ('max_t', 'max_t', 'yellow')],
    captions={
        'events = sorted': '先按==开始时间==排序，这样「已经开始的会议」就是前面连续一段，用指针 `p` 扫',
        'max_t = max(max_t, events[index][1])': '`max_t` = 最晚结束日 = {max_t}',
        't = 1': '从第 1 天开始，每天参加一场',
        'p = 0': '`p`：下一个还没加入堆的会议下标',
        'while t <= max_t': lambda S, B, r: (f'第 `{S.t}` 天 ≤ `max_t = {S.max_t}`，继续' if S.t <= S.max_t else f'`t = {S.t}` > `max_t` → 之后没有会议了'),
        'while p < n and events[p][0] <= t': lambda S, B, r: (f'会议 `{S.events[S.p]}` 的开始日 `{S.events[S.p][0]}` ≤ `t = {S.t}` → 已经开始，可以参加' if S.p < S.n and S.events[S.p][0] <= S.t
                                                             else '没有新开始的会议了'),
        'heapq.heappush(heap, events[p][1])': '把结束日 `{events[p][1]}` 放进堆：堆里存的是==结束日==',
        'p += 1': '`p` → {p}',
        'while heap:': lambda S, B, r: ('堆里还有会议，检查堆顶是否已经结束' if S.heap else '堆是空的，今天没有会议可参加'),
        'if heap[0] >= t': lambda S, B, r: (f'堆顶结束日 `{S.heap[0]}` ≥ 今天 `{S.t}` → 还没结束，就是它' if S.heap[0] >= S.t
                                            else f'堆顶结束日 `{S.heap[0]}` < 今天 `{S.t}` → 已经结束，丢掉'),
        'break': '堆顶会议还没结束 → 停止清理',
        'heapq.heappop(heap)': lambda S, B, r: '丢弃过期会议' if S._line == 23 else '参加结束日最早的会议（弹出堆顶）',
        'if heap:': lambda S, B, r: ('堆里有未结束的会议 → 今天可以参加一场' if S.heap else '堆空 → 今天没有会议可参加'),
        'res += 1': '第 `{t}` 天参加一场，`res` → =={res}==',
        'if p == n': lambda S, B, r: ('堆空而且会议都已加入 → 后面没有候选，提前结束' if S.p == S.n else f'堆空但还有 `{S.n - S.p}` 个会议没开始，今天空着，继续等'),
        't += 1': '进入下一天：`t` → {t}',
        'return res': '最多参加 `{ret}` 场',
    },
    cards=dict(
        one_liner='每天都参加「已开始且结束最早」的会议',
        complexity='时间 `O(U + n log n)`，空间 `O(n)`',
        problem=['`events[i] = [start, end]`，会议可在 `start..end` 内任选一天参加',
                 '一天只能参加一场，求最多能参加几场',
                 '示例：`[[1,2],[2,3],[3,4],[1,2]]` → `4`',
                 '本视频：`[[1,2],[1,2],[1,2],[2,3]]` → `3`'],
        quote='由于题目中所有会议的价值都是相同的，那么在某一时刻，若可以参加两个会议，我们就应该选择参加结束时间较早的那个。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按==开始时间==排序，用指针 `p` 扫：第 `t` 天把所有 `start <= t` 的会议的结束日放进堆',
              '弹掉堆顶中结束日 `< t` 的会议（已错过）',
              '堆不空就参加堆顶（结束最早）的会议，`res += 1`'],
        summary=['时间 `O(U + n log n)`，`U = max_t` 是最晚结束日',
                 '过期判断：堆顶 `< t` 才算结束，`== t` 当天还能参加',
                 '堆空并且 `p == n` 时可以提前 `break`，否则要继续等后面的会议开始',
                 '对比灵神：灵神用并查集给每场会议找最早空闲天，这里按天模拟']),
)
