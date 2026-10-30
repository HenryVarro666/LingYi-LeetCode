CONFIG = dict(
    num=630, title='课程表 III', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按截止日排序 + 反悔堆',
    tags=['堆（优先队列）', '反悔贪心', '难度分 2000'],
    setup='''
import heapq
def heappush_max(h, x):
    h.append(x)
    heapq._siftdown_max(h, 0, len(h) - 1)
def heapreplace_max(h, x):
    return heapq._heapreplace_max(h, x)
''',
    code='''
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        courses.sort(key=lambda c: c[1])  # 按照 last_day 从小到大排序
        h = []  # 最大堆
        day = 0  # 已消耗时间
        for duration, last_day in courses:
            if day + duration <= last_day:  # 没有超过 last_day，直接学习
                day += duration
                heappush_max(h, duration)
            elif h and duration < h[0]:  # 该课程的时间比之前的最长时间要短
                # 反悔，撤销之前 duration 最长的课程，改为学习该课程
                # 节省出来的时间，能在后面上完更多的课程
                day -= heapreplace_max(h, duration) - duration
        return len(h)
''',
    call='Solution().scheduleCourse([[5,5],[4,6],[2,6],[8,14],[3,16]])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前课程：耗时 `{S['duration']}`，截止 `{S['last_day']}`；已用 ==`{S['day']}`== 天" if 'duration' in S and 'day' in S else '课程已按截止日排序后逐门处理'), size=26),
        dict(type='array', var="[f'{a}/{b}' for a, b in courses]", label='courses（耗时/截止日，按截止日排序）', h=230, cell=96,
             color=lambda S, i, v: 'yellow' if 'duration' in S and v == f"{S['duration']}/{S['last_day']}" else None),
        dict(type='heap', var='h', label='最大堆 h：已选课程的 duration（堆顶最长）', h=300),
    ],
    watch=[('day', 'day', 'blue'), ('duration', 'duration', 'yellow'), ('last_day', 'last_day', 'pink'), ('已选课程数', 'len(h)', 'green')],
    captions={
        'courses.sort': '先考的先上：按 `last_day` 从小到大排序 → {courses}',
        'h = []': '最大堆 `h` 存已选课程的耗时，堆顶是耗时最长的那门',
        'day = 0': '`day` 记录已消耗的天数',
        'for duration': '看下一门课：耗时 `{duration}`，截止第 `{last_day}` 天',
        'if day + duration': '`{day} + {duration} = {day + duration}` 与 `last_day = {last_day}` 比：{"来得及 → 直接学" if day + duration <= last_day else "来不及，考虑反悔"}',
        'day += duration': '学这门课：`day` → =={day}==',
        'heappush_max': '耗时 `{duration}` 入最大堆，已选 `{len(h)}` 门：{h}',
        'elif h and': lambda S, B, r: (f'来不及，但已选课程里最长的是 `{S.h[0]}`，当前耗时 `{S.duration}` 更短 → ==可以反悔==' if S.h and S.duration < S.h[0] else (f'来不及，且当前耗时 `{S.duration}` ≥ 堆顶 `{S.h[0]}`：换了也没有好处 → 放弃这门' if S.h else '来不及，堆里也没有可撤销的课 → 放弃')),
        'day -= heapreplace_max': '撤销最长的课、改学当前课：数量不变，`day` 省出 `{B.day - day}` 天 → =={day}==，后面更有机会',
        'return len(h)': '堆里剩下几门，就是最多修的课程数：=={len(h)}==',
    },
    cards=dict(
        one_liner='先按截止日排序，来不及就反悔：撤销最长的那门',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`courses[i] = [duration, lastDay]`：要连续上 `duration` 天，且必须在 `lastDay` 前上完',
                 '同一时间只能上一门课，第 1 天开始，求最多修几门',
                 '本视频：`[[5,5],[4,6],[2,6],[8,14],[3,16]]` → `3`'],
        quote='比如先上完 duration=7 的课和 duration=10 的课，后面遍历到了 duration=4 的课，但受到 lastDay 的限制，无法上 duration=4 的课。此时，我们可以「撤销」前面 duration 最长的课。',
        quote_src='—— 灵茶山艾府题解',
        idea=['lastDay 越早的课越要早上完 → 先按 `lastDay` 排序，遍历',
              '来得及就学；来不及时，==撤销已选里耗时最长的==，换成更短的当前课',
              '课数不变，却省出时间 → 用最大堆随时取出最长耗时'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：必须先按 `lastDay` 排序，堆里存的是 `duration` 而不是 `lastDay`',
                 '只有 `duration < h[0]` 才反悔，否则换了反而更慢',
                 '`heappush_max`、`heapreplace_max` 是新版 Python 的最大堆函数，视频里用等价实现（setup 里补的）',
                 '同类：§1.9 反悔贪心，如 2813、3049'],
    ),
)
