CONFIG = dict(
    num=1834, title='单线程 CPU', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 堆模拟',
    tags=['灵神题单', '常用数据结构', '难度分 1798'],
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
    call='Solution().getOrder([[5,2],[1,4],[1,1],[3,3]])',
    expect=[2, 1, 0, 3],
    views=[
        dict(type='text', fn=lambda S: (f"`t = {S['t']}`：CPU 上一次空闲的时间；堆里是积压的任务 `[耗时, 编号]`" if 't' in S else '')),
        dict(type='array', var='sorted_tasks', label='sorted_tasks：[进入时间, 耗时, 编号]', h=250, cell=150),
        dict(type='heap', var='heap', label='heap：积压任务', h=220, fmt=lambda x: f'{x[0]},{x[1]}'),
        dict(type='array', var='res', label='res：执行顺序', h=140, cell=90),
    ],
    watch=[('t', 't', 'orange'), 'e', 'p', 'id', ('res', 'res', 'green')],
    captions={
        'heap = []': '堆保存积压的任务 `[耗时, 编号]`，耗时最短的在堆顶',
        't = 0': '`t`：CPU 上一次空闲的时间点',
        'sorted_tasks = sorted': '按（进入时间，耗时，编号）排序：`{sorted_tasks}`',
        'for e, p, id in': lambda S, B, r: ('所有任务都处理过了' if 'id' in B and B['id'] == S['id'] and S['id'] == 0 and B.get('e') == S['e'] and B.get('t') == S['t'] and len(S['sorted_tasks']) and S['heap'] is not None and B.get('heap') == S['heap'] else f"处理任务：进入时间 `e = {S['e']}`，耗时 `p = {S['p']}`，编号 `{S['id']}`"),
        'while t < e and heap': lambda S, B, r: (f"`t = {S['t']} < e = {S['e']}` 且堆不空 → CPU 在新任务到达前还能处理积压的任务" if S['t'] < S['e'] and S['heap'] else (f"`t = {S['t']}` 已经到了 `e = {S['e']}`，不用再处理积压" if S['heap'] else '堆空了，没有积压任务')),
        'min_p, min_id = heapq.heappop(heap)': '弹出耗时最短的积压任务 `编号 {min_id}，耗时 {min_p}`',
        't += min_p': '执行它：`t` 从 {B.t} → {t}',
        'res.append(min_id)': '执行顺序加入 `{min_id}`：`res = {res}`',
        'if t <= e and not heap': lambda S, B, r: (f"`t = {S['t']} <= e = {S['e']}` 且没有积压 → CPU 空闲，新任务一到就能执行" if S['t'] <= S['e'] and not S['heap'] else f"CPU 还在忙（`t = {S['t']} > e = {S['e']}`）或有积压 → 新任务只能先排队"),
        'res.append(id)': '直接执行任务 `{id}`：`res = {res}`',
        't = e + p': '执行完的时间：`t = {e} + {p} = {t}`',
        'heapq.heappush': '任务 `{id}` 进堆排队：`[耗时 {p}, 编号 {id}]`，堆 = `{heap}`',
        'while heap': lambda S, B, r: ('所有任务都到达了，堆里剩下的依次执行' if S['heap'] else '堆空了，全部执行完'),
        'return res': '返回执行顺序 `{res}`',
    },
    cards=dict(
        one_liner='用堆维护积压任务，CPU 空了就取耗时最短的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`tasks[i] = [进入时间, 耗时]`，CPU 空闲时选队列里耗时最短的任务，相同选下标小的',
                 '一旦开始就不能中断，求执行顺序',
                 '本视频：`[[5,2],[1,4],[1,1],[3,3]]` → `[2,1,0,3]`'],
        quote='由于CPU每次都将执行当前堆积任务中执行耗时最短的任务，因此在这里需要使用一个堆来维护这些堆积的任务，从而高效地得到任意时刻堆积任务中耗时最短的任务是什么。',
        quote_src='—— yiduobo 题解原文',
        idea=['按（进入时间、耗时、编号）排序，再一趟遍历，`t` 记录 CPU 上次空闲的时间',
              '新任务 `e` 到达前，`t < e` 且堆不空：不断弹堆顶执行，推进 `t`',
              '若 `t <= e` 且堆空：CPU 空闲，直接执行新任务；否则新任务入堆排队'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`t < e` 才处理积压；之后 `t <= e` 且堆空才直接执行，否则必须入堆',
                 '遍历结束后堆里可能还有积压任务，要全部弹出',
                 '原文用 `heapq`，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神每轮先执行再入堆，`cur` 跳时间；这里按新任务到达来推进 `t`'],
    ),
)
