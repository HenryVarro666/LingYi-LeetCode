CONFIG = dict(
    num=630, title='课程表 III', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='截止时间排序 + 大顶堆（存负数）',
    tags=['堆（优先队列）', '反悔贪心', '难度分 2000'],
    code='''
import heapq

class Solution(object):
    def scheduleCourse(self, courses):

        courses = sorted(courses, key=lambda d:d[1])
        heap = []
        now = 0
        res = 0
        for course in courses:
            t, d = course
            if now + t <= d:
                heapq.heappush(heap, -t)
                now += t
                res += 1
            elif heap:
                max_t = -heapq.heappop(heap)
                if max_t > t:
                    now -= max_t - t
                    heapq.heappush(heap, -t)
                else:
                    heapq.heappush(heap, -max_t)

        return res
''',
    call='Solution().scheduleCourse([[5,5],[4,6],[2,6],[8,14],[3,16]])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前课程：耗时 `t={S['t']}`，截止 `d={S['d']}`；已学总耗时 `now={S['now']}`；已学 ==`{S['res']}`== 门" if 't' in S and 'now' in S else '先按截止时间从小到大排序'), size=26),
        dict(type='array', var="[f'{a}/{b}' for a, b in courses]", label='courses（耗时/截止，已按截止时间排序）', h=230, cell=96,
             color=lambda S, i, v: 'yellow' if 't' in S and v == f"{S['t']}/{S['d']}" else None),
        dict(type='heap', var='heap', label='heap：已学课程耗时的相反数（堆顶 = 耗时最多的）', h=300, fmt=lambda x: str(x)),
    ],
    watch=[('now', 'now', 'blue'), ('t', 't', 'yellow'), ('d', 'd', 'pink'), ('res', 'res', 'green')],
    captions={
        'courses = sorted': '没有规定起始时间、重要程度一样 → 能同时选的，先学截止早的：按截止时间排序 {courses}',
        'heap = []': '堆里存 `-t`，Python 只有小顶堆，取负后堆顶就是耗时最多的',
        'now = 0': '`now`：已学课程的总耗时',
        'res = 0': '`res`：已学课程数',
        't, d = course': '看下一门：耗时 `t={t}`，截止 `d={d}`',
        'if now + t <= d': '`{now} + {t} = {now + t}` 与 `d = {d}` 比：{"来得及 → 直接学" if now + t <= d else "来不及，看能不能换掉耗时最多的"}',
        13: '耗时 `{t}` 入堆（存 `-{t}`）：现在堆里 {heap}',
        20: '当前课入堆（存 `-{t}`）：{heap}，已学课数不变，但总耗时更小',
        'for course in courses': '取下一门课 `course`',
        'now += t': '学这门：`now` → =={now}==',
        'res += 1': '多学一门，`res` → =={res}==',
        'elif heap': lambda S, B, r: ('来不及，但已经学过课，可以尝试替换' if S.heap else '来不及，也没有课可以替换'),
        'max_t = -heapq.heappop': '取出已学里耗时最多的：`max_t` = =={max_t}==',
        'if max_t > t': lambda S, B, r: (f'`max_t = {S.max_t} > t = {S.t}`：用当前课替换它，结束时间必然更早、不会超过 d' if S.max_t > S.t else f'`max_t = {S.max_t} ≤ t = {S.t}`：换了不划算'),
        'now -= max_t - t': '替换后总耗时减少 `{max_t} - {t}` → `now` = =={now}=='  ,
        'heappush(heap, -max_t)': '不换：把 `{max_t}` 放回堆里',
        'return res': '一共能学 `{res}` 门',
    },
    cards=dict(
        one_liner='能一起学就先学截止早的，学不下就换掉耗时最长的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`courses[i] = [耗时, 截止日]`，课要连续学完且不能晚于截止日',
                 '一次只能学一门，求最多能学几门',
                 '本视频：`[[5,5],[4,6],[2,6],[8,14],[3,16]]` → `3`'],
        quote='对于任意两门课程，如果可以同时选择，我们就应该优先学习截止时间较早的。如果不能同时选择，那么我们就应该选择耗费时间较少的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按截止时间排序，一趟扫描：能学就学',
              '学不了：从已学课程里找耗时最多的 `max_t`',
              '若 `max_t > t`，用当前课替换它：原来 `max_t` 的时间足够学当前课，所以截止时间必然满足',
              '用堆（存负数）维护已学课程的最大耗时'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`now` 要同步减去 `max_t - t`，`res` 不变（一出一进）',
                 '不替换时必须把弹出的 `max_t` 放回堆里',
                 '对比灵神：灵神用 `heapreplace` 一步完成弹出和压入，并用 `len(h)` 当答案；yiduobo 用 `res` 计数',
                 '原文为 Python 2 风格，本题代码无需修改'],
    ),
)
