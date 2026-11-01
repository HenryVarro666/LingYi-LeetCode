CONFIG = dict(
    num=1834, title='单线程 CPU', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 最小堆模拟（Go 原文转写）',
    tags=['灵神题单', '常用数据结构', '难度分 1798'],
    code='''
class Solution:
    def getOrder(self, a: List[List[int]]) -> List[int]:
        ans = []
        for i in range(len(a)):
            a[i].append(i)
        a.sort(key=lambda x: x[0])
        h = []
        i, cur, n = 0, 0, len(a)
        while i < n:
            if len(h) > 0:
                p = heappop(h)
                ans.append(p[1])
                cur += p[0]
            if len(h) == 0 and cur < a[i][0]:
                cur = a[i][0]
            while i < n and a[i][0] <= cur:
                heappush(h, (a[i][1], a[i][2]))
                i += 1
        while len(h) > 0:
            ans.append(heappop(h)[1])
        return ans
''',
    call='Solution().getOrder([[1,2],[2,4],[3,2],[4,1]])',
    expect=[0, 2, 3, 1],
    views=[
        dict(type='text', fn=lambda S: (f"当前时间 `cur = {S['cur']}`；堆里是已经到达、等待执行的任务 `(耗时, 编号)`" if 'cur' in S else '先把任务按进入时间排序，并在每项后面附上原编号')),
        dict(type='array', var='a', label='a：[进入时间, 耗时, 编号]（按进入时间排序）', h=310, cell=150, pointers={'i': 'blue'}),
        dict(type='heap', var='h', label='h：最小堆', h=220, fmt=lambda x: f'{x[0]},{x[1]}'),
        dict(type='array', var='ans', label='ans：任务执行顺序', h=150, cell=90),
    ],
    watch=[('i', 'i', 'blue'), ('cur', 'cur', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'a[i].append(i)': '给每个任务附上原下标 `{i}`：排序后还要靠它输出答案',
        'a.sort': '按进入时间排序：`{a}`',
        'h = []': '堆按 (耗时, 编号) 排序：耗时短优先，一样就编号小的优先',
        'i, cur, n': '`i` 是下一个还没入堆的任务，`cur` 是当前时间',
        9: lambda S, B, r: (f"`i = {S['i']} < {S['n']}`：还有任务没进过堆" if S['i'] < S['n'] else '所有任务都进过堆了，剩下的堆里任务依次执行'),
        'if len(h) > 0': lambda S, B, r: ('堆不空 → CPU 取出耗时最短的任务执行' if S['h'] else '堆是空的 → 这一轮没有任务可执行'),
        'p = heappop(h)': '弹出堆顶 `(耗时 {p[0]}, 编号 {p[1]})`：它是==耗时最短==的任务',
        'ans.append(p[1])': '执行任务 `{p[1]}`：`ans = {ans}`',
        'cur += p[0]': '执行完要花 `{p[0]}`：`cur` 从 {B.cur} → {cur}',
        'if len(h) == 0 and cur < a[i][0]': lambda S, B, r: (f"堆空且 `cur = {S['cur']} < {S['a'][S['i']][0]}`：CPU 空闲，直接跳到下个任务的进入时间" if not S['h'] and S['cur'] < S['a'][S['i']][0] else '堆里有任务，或下个任务已经到达 → 时间不用跳'),
        'cur = a[i][0]': '`cur` 跳到 `{cur}`',
        16: lambda S, B, r: ((f"`a[{S['i']}]` 的进入时间 `{S['a'][S['i']][0]} <= cur = {S['cur']}` → 已经到达，入堆" if S['i'] < S['n'] and S['a'][S['i']][0] <= S['cur'] else ('没有任务了' if S['i'] >= S['n'] else '下一个任务还没到达，回到外层循环'))),
        'heappush': '任务 `{a[i][2]}` 入堆：`(耗时 {a[i][1]}, 编号 {a[i][2]})`，堆 = `{h}`',
        'while len(h) > 0': lambda S, B, r: ('所有任务都已入堆，接下来按堆顺序执行' if S['h'] else '堆空了，结束'),
        'ans.append(heappop(h)[1])': '弹出耗时最短的，执行：`ans = {ans}`',
        'return ans': '返回执行顺序 `{ans}`',
    },
    cards=dict(
        one_liner='到达的任务进堆，CPU 空了就取耗时最短的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`tasks[i] = [进入时间, 耗时]`，CPU 空闲时选队列里耗时最短的任务，相同选下标小的',
                 '一旦开始执行就不能中断，求执行顺序',
                 '示例：`[[1,2],[2,4],[3,2],[4,1]]` → `[0,2,3,1]`'],
        quote='按进入时间排序。遍历任务数组，每次至多执行一个任务，然后将所有进入时间不超过当前时间 cur 的任务加入堆中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先给任务附上下标，按进入时间排序',
              '每轮：堆里有任务就弹出堆顶执行，`cur` 加上耗时；若堆空且下个任务还没到，`cur` 直接跳过去',
              '然后把所有进入时间 `<= cur` 的任务入堆；最后堆里剩下的依次弹出'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；Go 里手写的 `hp` 堆（按耗时、再按编号）用 `heapq` 里的 `(耗时, 编号)` 元组代替，元组比较规则相同',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：堆空且任务没到时，要把 `cur` 跳到下个任务的进入时间，否则会死循环',
                 '先执行、再入堆：这样每一轮 CPU 空闲时的任务集合才完整',
                 '同类题：253 会议室 II、621 任务调度器'],
    ),
)
