CONFIG = dict(
    num=1834, title='单线程 CPU', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 最小堆模拟',
    tags=['堆（优先队列）', '难度分 1798'],
    code='''
class Solution(object):
    def getOrder(self, tasks):

        heap = []
        t = 0

        sorted_tasks = sorted([[task[0], task[1], index] for index, task in enumerate(tasks)], key=lambda d:(d[0], d[1], d[2]))
        res = []
        for e, p, id in sorted_tasks:
            while t < e and heap:
                min_p, min_id = heapq.heappop(heap)
                t += min_p
                res.append(min_id)
            
            if t <= e and not heap:
                res.append(id)
                t = e + p
            else:
                heapq.heappush(heap, [p, id])

        while heap:
            min_p, min_id = heapq.heappop(heap)
            res.append(min_id)
        
        return res
''',
    call='Solution().getOrder([[1,2],[2,4],[3,2],[4,1]])',
    expect=[0, 2, 3, 1],
    views=[
        dict(type='text', fn=lambda S: (f"CPU 空闲时刻 `t = {S['t']}`；当前任务到达 `e = {S['e']}`，耗时 `p = {S['p']}`，编号 `{S['id']}`" if 'e' in S else '先把任务按 (到达时间, 耗时, 编号) 排序')),
        dict(type='array', var='[f"{a},{b},#{c}" for a, b, c in sorted_tasks]', cell=130, h=200, label='sorted_tasks：到达,耗时,#编号'),
        dict(type='heap', var='heap', fmt=lambda x: f'耗时{x[0]} #{x[1]}', h=150, label='heap：已到达未执行的任务'),
        dict(type='array', var='res', h=150, label='res：CPU 执行顺序'),
    ],
    watch=[('t', 't', 'blue'), ('e', 'e', 'pink'), ('p', 'p', 'yellow'), ('id', 'id', 'purple')],
    captions={
        't = 0': '`t`：CPU 上一次空闲的时间',
        'sorted_tasks = sorted': '按到达时间、耗时、编号排序：==同一时刻到达的，最短最先==',
        'for e, p, id': lambda S, B, r: ('所有任务都已到达，下面清空堆里积压的任务' if 'e' in B and (S.e, S.p, S.id) == (B.e, B.p, B.id) else f'下一个到达的任务：到达 `{S.e}`，耗时 `{S.p}`，编号 `{S.id}`'),
        'while t < e and heap': lambda S, B, r: (f'`t = {S.t} < e = {S.e}` 且堆非空 → CPU 在新任务到达前还能做积压任务' if S.t < S.e and S.heap
                                                else (f'堆为空 → 没有积压任务，退出' if not S.heap else f'`t = {S.t} >= e = {S.e}` → 新任务已到达，退出')),
        'min_p, min_id = heapq.heappop(heap)': '弹出耗时最短的积压任务：耗时 `{min_p}`，编号 `{min_id}`',
        't += min_p': '执行它，CPU 空闲时间推进到 `t = {t}`',
        'res.append(min_id)': '记录执行顺序：`res = {res}`',
        'if t <= e and not heap': lambda S, B, r: (f'`t = {S.t} <= e = {S.e}` 且堆为空 → CPU 空闲，新任务一到就执行' if S.t <= S.e and not S.heap
                                                  else (f'`t = {S.t} > e = {S.e}`：CPU 还在忙 → 新任务得排队' if S.t > S.e else '堆里还有积压任务，要先做它们 → 新任务得排队')),
        'res.append(id)': '直接执行任务 `{id}`：`res = {res}`',
        't = e + p': '执行耗时 `{p}`：`t = {e} + {p} = {t}`',
        'heapq.heappush(heap, [p, id])': '任务 `{id}` 入堆排队：`[耗时 {p}, 编号 {id}]`，==耗时第一关键字、编号第二==',
        'while heap': lambda S, B, r: (f'堆里还有积压任务 → 继续执行' if S.heap else '堆空了 → 结束'),
        'return res': 'CPU 处理顺序 `{res}`',
    },
    cards=dict(
        one_liner='排序后按到达时间推进，堆里挑耗时最短的任务',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`tasks[i] = [到达时间, 耗时]`，单线程 CPU 一次只做一个任务，做完才能换',
                 'CPU 空闲时，从已到达的任务里选耗时最短的（并列选编号小的）',
                 '返回任务执行顺序；示例：`[[1,2],[2,4],[3,2],[4,1]]` → `[0,2,3,1]`'],
        quote='没有想到什么特别好的转化方法，只能老老实实按题目描述的工作流程进行模拟。……需要使用一个堆来维护这些堆积的任务。',
        quote_src='—— yiduobo 题解原文',
        idea=['任务先按 `(到达, 耗时, 编号)` 排序，再一趟遍历',
              '新任务到达前，CPU 能把堆里积压的任务（耗时短的先）做完',
              '若堆空且 CPU 已空闲，新任务直接执行，否则入堆排队'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：`t` 是 CPU 空闲时间，空闲时要跳到 `e + p`',
                 '易错点：遍历结束后，堆里可能还有积压任务要清空',
                 '堆元素 `[耗时, 编号]`，天然满足并列取编号小',
                 '原文代码在 Python 3 下无需修改'],
    ),
)
