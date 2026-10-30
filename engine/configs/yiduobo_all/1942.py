CONFIG = dict(
    num=1942, title='最小未被占据椅子的编号', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='两个堆：空闲椅子 + 使用中椅子',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1695'],
    code='''
class Solution(object):
    def smallestChair(self, times, targetFriend):

        n = len(times)
        idle = list(range(n))
        using = []
        sorted_times = sorted([[index, arrival, leaving] for index, [arrival, leaving] in enumerate(times)], key=lambda d:d[1])
        for index, arrival, leaving in sorted_times:
            while using and using[0][0] <= arrival:
                _, num = heapq.heappop(using)
                heapq.heappush(idle, num)
            
            num = heapq.heappop(idle)
            heapq.heappush(using, [leaving, num])

            if targetFriend == index:
                return num
''',
    call='Solution().smallestChair([[3,10],[1,5],[2,6],[5,8]], 3)',
    expect=0,
    views=[
        dict(type='table', var=lambda S: [list(x) for x in S['sorted_times']] if 'sorted_times' in S else [],
             rows=lambda S: [f'#{i}' for i in range(len(S['sorted_times']))] if 'sorted_times' in S else [],
             cols=['朋友', '到达', '离开'], h=230,
             label='按到达时间排好的朋友 [编号, 到达, 离开]'),
        dict(type='heap', var='idle', label='idle：空闲椅子', h=170),
        dict(type='heap', var='using', label='using：离开时刻→椅子',
             fmt=lambda x: f'{x[0]}→椅{x[1]}', h=170),
        dict(type='text', h=90, fn=lambda S: (f"处理朋友 ==`{S['index']}`==：到达 `{S['arrival']}`，离开 `{S['leaving']}`" if 'arrival' in S else '')),
    ],
    watch=['index', 'arrival', 'leaving', ('num', 'num', 'green'), 'targetFriend'],
    skip=['n = len', 'using = []'],
    captions={
        'idle = list': '一共 `n` 个人，最多同时需要 `n` 张椅子，所以先备好 `0..n-1` 的空闲椅子（原文 `range(n)`，Py3 要转成 list）',
        'sorted_times = ': '按到达时间排序，同时记住每个人的原编号：`{sorted_times}`',
        'for index, arrival': '处理下一位到达的朋友 `{index}`：到达 `{arrival}`，离开 `{leaving}`',
        'while using': lambda S, B, r: (f'最早腾出的椅子在 `{S.using[0][0]}` 时刻 ≤ 到达 `{S.arrival}` → 已空出，放回 idle' if S.using and S.using[0][0] <= S.arrival
                                        else '没有更多椅子在此刻前空出了，退出'),
        'heapq.heappop(using)': '把空出的椅子 `{num}` 弹出',
        'heapq.heappush(idle': '椅子 `{num}` 回到空闲堆：`idle = {idle}`',
        'num = heapq.heappop(idle)': '空闲堆顶就是最小编号：他坐 ==`{num}`== 号椅子',
        'heapq.heappush(using': '记下这张椅子要到 `{leaving}` 时刻才空：`using = {using}`',
        'if targetFriend': lambda S, B, r: (f'`targetFriend = {S.targetFriend}` 就是这位朋友 → 返回他的椅子' if S.targetFriend == S.index
                                            else f'`{S.index}` 不是目标朋友 `{S.targetFriend}`，继续'),
        'return num': '目标朋友坐的是 ==`{num}`== 号椅子',
    },
    cards=dict(
        one_liner='空椅子一个堆，占用中椅子再一个堆，到达时先把到期的还回去',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['朋友按到达时间入座，坐最小编号的空椅子；离开后椅子立刻空出',
                 '给定每人的 `[到达, 离开]`，求 `targetFriend` 坐的椅子编号',
                 '本视频：`[[3,10],[1,5],[2,6],[5,8]]`，目标 `3` → `0`'],
        quote='使用两个堆，分别维护当前空闲的椅子编号，以及当前在使用的椅子什么时候能空出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按到达时间排序（带上原编号），一趟遍历',
              '先把 `using` 中离开时间 ≤ 当前到达时间的椅子弹出，放回 `idle`',
              '再从 `idle` 弹最小编号给当前人，按他的离开时间压入 `using`',
              '初始要准备 `n` 张空闲椅子'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先释放椅子再分配；离开时刻 == 到达时刻时椅子可立即复用（用 `<=`）',
                 '原文为 Python 2 写法，`range(n)` 已改为 `list(range(n))`（才能当堆用）',
                 '同类：安排工作、会议室等「最小编号」系列'],
    ),
)
