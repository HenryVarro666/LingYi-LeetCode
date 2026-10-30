CONFIG = dict(
    num=3885, title='设计事件管理器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记最新优先级 + 懒更新堆',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1548'],
    code='''
class EventManager(object):

    def __init__(self, events):
        self.heap = []
        self.hash = {}
        for eid, pri in events:
            heapq.heappush(self.heap, (-pri, eid))
            self.hash[eid] = pri

    def updatePriority(self, eventId, newPriority):
        if eventId in self.hash and newPriority != self.hash[eventId]:
            self.hash[eventId] = newPriority
            heapq.heappush(self.heap, (-newPriority, eventId))

    def pollHighest(self):
        while self.heap:
            pri, eid = heapq.heappop(self.heap)
            if eid in self.hash and self.hash[eid] == -pri:
                self.hash.pop(eid)
                return eid
        
        return -1
''',
    call='''em = EventManager([[5, 7], [2, 7], [9, 4]])
out = [em.pollHighest()]
em.updatePriority(9, 7)
em.updatePriority(9, 7)
out.append(em.pollHighest())
out.append(em.pollHighest())
out.append(em.pollHighest())
out''',
    expect=[2, 5, 9, -1],
    views=[
        dict(type='map', var='self.hash', label='hash（事件 → 最新优先级）', fmt=lambda k, v: f'{k} → {v}', h=110),
        dict(type='heap', var='self.heap', label='heap（-优先级, id）堆顶 = 优先级最高、id 最小', fmt=lambda x: f'{x[1]}:{-x[0]}', top_color='blue', h=190),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['eid', 'pri', ('out', 'out', 'green')],
    captions={
        'self.heap = []': '`heap`：存所有 `(-优先级, id)` 的 pair',
        'self.hash = {}': '`hash`：事件 id → ==最新==优先级，同时表示“还活跃”',
        'for eid, pri in events': lambda S, B, r: ('所有事件都放好了' if len(S.self.heap) == len(S.events) else f'事件 `{S.eid}`，优先级 `{S.pri}`'),
        'heapq.heappush(self.heap, (-pri, eid))': '把 `({-pri}, {eid})` 放进堆：取负，最大优先级在堆顶',
        'self.hash[eid] = pri': '`hash[{eid}] = {pri}`',
        'if eventId in self.hash and': lambda S, B, r: (
            f'`updatePriority({S.eventId}, {S.newPriority})`：事件还在，但优先级 `{S.self.hash[S.eventId]}` 已经是 `{S.newPriority}` → 什么都不用做'
            if S.eventId in S.self.hash and S.newPriority == S.self.hash[S.eventId] else
            (f'`updatePriority({S.eventId}, {S.newPriority})`：事件还活跃，优先级变了 → 要更新'
             if S.eventId in S.self.hash else f'事件 `{S.eventId}` 已不活跃 → 不执行任何操作')),
        'self.hash[eventId] = newPriority': '`hash[{eventId}]` 改成最新值 `{newPriority}`',
        'heapq.heappush(self.heap, (-newPriority, eventId))': '堆里的旧数据不动，再放一条新的 `({-newPriority}, {eventId})`',
        'while self.heap': lambda S, B, r: ('堆里还有数据，取堆顶' if S.self.heap else '堆空了：没有活跃事件'),
        'pri, eid = heapq.heappop(self.heap)': '弹出堆顶：事件 `{eid}`，优先级 `{-pri}`',
        'if eid in self.hash and self.hash[eid] == -pri': lambda S, B, r: (
            f'`hash` 里事件 `{S.eid}` 的优先级 = `{S.self.hash.get(S.eid, "没有（已被取走）")}`，堆里是 `{-S.pri}` → '
            + ('==一致，合法，取走它==' if S.self.hash.get(S.eid) == -S.pri else '==不一致，是旧数据，继续弹==')),
        'self.hash.pop(eid)': '事件 `{eid}` 被移除：从 `hash` 弹出',
        'return eid': '返回 =={ret}==',
        'return -1': '堆空了，没有活跃事件 → 返回 ==-1==',
    },
    max_steps=90,
    cards=dict(
        one_liner='用哈希表记最新优先级，堆弹出时核对，不一致就是旧数据',
        complexity='更新、弹出均摊 `O(log(n+q))`；初始化 `O(n log n)`',
        problem=['事件有唯一 `eventId` 和 `priority`，要支持改优先级、取出最高优先级',
                 '优先级相同取 `eventId` 最小；没有活跃事件返回 `-1`',
                 '本视频：`[[5,7],[2,7],[9,4]]` → poll、update、poll、poll、poll → `[2,5,9,-1]`'],
        quote='题目实际上就是要实现一个具有修改功能的堆，在这里可以采用懒更新的策略，使用哈希表配合原生的堆来实现。',
        quote_src='—— yiduobo 题解原文',
        idea=['`hash` 记每个 `eventId` 的最新 `priority`；堆里放 `(-priority, eventId)`',
              'update：事件还在且优先级真的变了才处理——改 `hash`，再把新的 pair 加入堆',
              'poll：不停弹堆顶，`eid` 在 `hash` 里且优先级相等才合法；合法就从 `hash` 弹出并返回'],
        summary=['更新、弹出均摊 `O(log(n+q))`，每条数据至多入堆出堆各一次',
                 'update 要先判 `eventId in hash`：已被取走的事件不能再更新',
                 'poll 取走后要 `hash.pop(eid)`，旧数据才会被认出',
                 '对比灵神：灵神初始化用 `heapify` 建堆，update 不判断事件是否活跃（题目已保证）；yiduobo 多判了一次“优先级没变就不入堆”'],
    ),
)
