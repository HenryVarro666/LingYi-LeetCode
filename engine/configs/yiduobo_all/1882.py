CONFIG = dict(
    num=1882, title='使用服务器处理任务', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='空闲堆 + 工作堆',
    tags=[],
    code='''
class Solution(object):
    def assignTasks(self, servers, tasks):

        working_server = []
        idle_server = []
        for index, weight in enumerate(servers):
            heapq.heappush(idle_server, [weight, index])

        res = []
        now = 0
        for index, t in enumerate(tasks):
            if now < index:
                now = index

            if not idle_server:
                if working_server[0][0] > now:
                    now = working_server[0][0]

            while working_server and working_server[0][0] == now:
                _, server_id = heapq.heappop(working_server)
                heapq.heappush(idle_server, [servers[server_id], server_id])

            _, server_id = heapq.heappop(idle_server)
            res.append(server_id)
            heapq.heappush(working_server, [now + t, server_id])

        return res
''',
    call='Solution().assignTasks([2,1], [3,3,1,1,2])',
    expect=[1, 0, 1, 1, 0],
    views=[
        dict(type='array', var='tasks', pointers={'index': 'blue'}, label='tasks（第 index 个任务在第 index 秒到达，值 = 耗时）', h=200),
        dict(type='heap', var='idle_server', fmt=lambda x: f'#{x[1]} 权重{x[0]}', label='空闲堆', h=140),
        dict(type='heap', var='working_server', fmt=lambda x: f'#{x[1]} 第{x[0]}秒空闲', label='工作堆', h=140),
        dict(type='array', var='res', label='res（每个任务分到的服务器）', h=130),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'yellow'), ('server_id', 'server_id', 'green')],
    captions={
        'heapq.heappush(idle_server, [weight, index])': '服务器 `{index}`（权重 `{weight}`）先全部放进空闲堆，key = ==[权重, 下标]==',
        'now = 0': '`now`：==当前任务开始执行的时间==，只增不减',
        'if now < index': lambda S, B, r: (f'任务 `{S.index}` 在第 `{S.index}` 秒才到，`now = {S.now}` 更早 → 先对齐到 `{S.index}`' if S.now < S.index
                                           else f'`now = {S.now}` ≥ 到达时间 `{S.index}` → 任务要排到 `now` 之后'),
        'now = index': '`now` 更新为到达时间 `{now}`',
        'if not idle_server': lambda S, B, r: ('没有空闲服务器 → 只能等最早完工的那台' if not S.idle_server else f'还有 `{len(S.idle_server)}` 台空闲服务器，不用等'),
        'if working_server[0][0] > now': '最早完工时间 `{working_server[0][0]}` vs `now = {now}`：晚于 now 就得等到那一刻',
        'now = working_server[0][0]': '等待：`now` 推进到 `{now}`，任务从这一刻开始',
        'while working_server and working_server[0][0] == now': lambda S, B, r: (f'有服务器 `{S.working_server[0][1]}` 恰好在 `now = {S.now}` 完工 → 放回空闲堆' if S.working_server and S.working_server[0][0] == S.now
                                                                                else '已经没有在 now 完工的服务器了'),
        '_, server_id = heapq.heappop(working_server)': '服务器 `{server_id}` 完工，回到空闲状态',
        'heapq.heappush(idle_server, [servers[server_id], server_id])': '放回空闲堆 `[权重 {servers[server_id]}, 下标 {server_id}]`',
        '_, server_id = heapq.heappop(idle_server)': '空闲堆顶 = ==权重最小（相同取下标小）==的服务器 `{server_id}`',
        'res.append(server_id)': '任务 `{index}` 分给服务器 `{server_id}`，`res` = {res}',
        'heapq.heappush(working_server, [now + t, server_id])': '服务器 `{server_id}` 干 `{t}` 秒，==第 `{now + t}` 秒==空闲 → 放进工作堆',
        'return res': '全部任务分配完：`{ret}`',
    },
    cards=dict(
        one_liner='空闲堆选权重最小，工作堆管完工时间',
        complexity='时间 `O((n + m) log n)`，空间 `O(n)`',
        problem=['`servers[i]` 是服务器权重，`tasks[j]` 是任务耗时；第 `j` 个任务在第 `j` 秒到达',
                 '每次从空闲服务器里选权重最小（相同选下标小）的；没有空闲就等最早完工的',
                 '示例：`servers=[5,1,4,3,2]`，`tasks=[2,1,2,4,5,2,1]` → `[1,4,1,4,1,3,2]`',
                 '本视频：`servers=[2,1]`，`tasks=[3,3,1,1,2]`'],
        quote='对于任务处理的顺序，题目要求优先处理下标较小的任务，因此可以一趟遍历，每次先想办法处理了当前的任务然后再继续向后处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个堆：空闲堆 key = 权重，工作堆 key = 完工时间',
              '变量 `now` 表示==当前任务的开始时间==：先与到达时间取大，没空闲服务器再推进到最早完工时刻',
              '把 `now` 时刻完工的服务器弹出放回空闲堆，再用空闲堆顶干活'],
        summary=['时间 `O((n + m) log n)`，`n` 台服务器、`m` 个任务',
                 '易错点：==没有空闲服务器时 now 要推进到最早完工时间==，不是 +1',
                 '完工时间等于 `now` 就算空闲（`==`），所以先回收再分配',
                 '空闲堆元素是 `[权重, 下标]`，权重相同自动按下标排'],
    ),
)
