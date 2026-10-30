CONFIG = dict(
    num=3885, title='设计事件管理器', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 懒更新堆',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1548'],
    code='''
class EventManager:
    def __init__(self, events: List[List[int]]):
        self.id_to_priority = {}
        self.h = []
        for eid, priority in events:
            self.id_to_priority[eid] = priority
            self.h.append((-priority, eid))
        heapify(self.h)

    def updatePriority(self, eventId: int, newPriority: int) -> None:
        self.id_to_priority[eventId] = newPriority
        heappush(self.h, (-newPriority, eventId))

    def pollHighest(self) -> int:
        while self.h:
            priority, eid = heappop(self.h)
            if self.id_to_priority.get(eid, -1) == -priority:
                del self.id_to_priority[eid]
                return eid
            # else 货不对板，继续找下一个
        return -1
''',
    call='''em = EventManager([[5, 7], [2, 7], [9, 4]])
out = [em.pollHighest()]
em.updatePriority(9, 7)
out.append(em.pollHighest())
out.append(em.pollHighest())
out.append(em.pollHighest())
out''',
    expect=[2, 5, 9, -1],
    views=[
        dict(type='map', var='self.id_to_priority', label='id_to_priority（事件 → 最新优先级）', fmt=lambda k, v: f'{k} → {v}', h=110),
        dict(type='heap', var='self.h', label='h（-优先级, id）堆顶 = 优先级最高、id 最小', fmt=lambda x: f'{x[1]}:{-x[0]}', top_color='blue', h=190),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['eid', 'priority', ('out', 'out', 'green')],
    captions={
        'self.id_to_priority = {}': '哈希表：事件 id → ==最新==优先级',
        'self.h = []': '堆里存 `(-优先级, id)`：`heapq` 是小根堆，取负后堆顶 = 优先级最高；同优先级 id 小的在前',
        'for eid, priority in events': lambda S, B, r: ('所有事件都记好了' if len(S.self.h) == len(S.events) else f'事件 `{S.eid}`，优先级 `{S.priority}`'),
        'self.id_to_priority[eid] = priority': '记下事件 `{eid}` 的优先级 `{priority}`',
        'self.h.append': '先 `append` 进列表（`-{priority}, {eid}`），暂不整理',
        'heapify(self.h)': lambda S, B, r: f'一次 `heapify` 建堆，`O(n)`：堆顶 = ==({S.self.h[0][0]}, {S.self.h[0][1]})==，优先级最高里 id 最小',
        'self.id_to_priority[eventId] = newPriority': '`updatePriority({eventId}, {newPriority})`：哈希表里的优先级改成最新 `{newPriority}`',
        'heappush(self.h, (-newPriority, eventId))': '==不改堆里的旧数据==，直接再 push 一条 `({-newPriority}, {eventId})`，旧的以后碰到再丢',
        'while self.h': lambda S, B, r: ('堆里还有数据，取堆顶' if S.self.h else '堆空了：没有活跃事件'),
        'priority, eid = heappop(self.h)': '弹出堆顶：事件 `{eid}`，优先级 `{-priority}`',
        'if self.id_to_priority.get(eid, -1) == -priority': lambda S, B, r: (
            f'哈希表里事件 `{S.eid}` 的最新优先级 = `{S.self.id_to_priority.get(S.eid, "没有（已被取走）")}`，堆里是 `{-S.priority}` → '
            + ('==一致，这是有效数据==' if S.self.id_to_priority.get(S.eid, -1) == -S.priority else '==不一致，是旧数据，丢掉继续弹==')),
        'del self.id_to_priority[eid]': '事件 `{eid}` 被取走，从哈希表删除（以后它堆里的旧数据就查不到了）',
        'return eid': '返回 =={ret}==',
        '# else': '货不对板：丢掉，继续弹下一个',
        'return -1': '堆空了，没有活跃事件 → 返回 ==-1==',
    },
    max_steps=90,
    cards=dict(
        one_liner='改优先级不动堆里旧数据，直接多 push 一条，弹出时核对',
        complexity='更新、弹出均摊 `O(log(n+q))`；初始化 `O(n)`',
        problem=['`EventManager(events)`：每个事件有唯一 id 和优先级',
                 '`updatePriority`：改活跃事件的优先级；`pollHighest`：移除并返回优先级最高（相同则 id 最小）的事件，没有返回 `-1`',
                 '本视频：`[[5,7],[2,7],[9,4]]`，poll → 更新 9 为 7 → poll,poll,poll → `[2,5,9,-1]`'],
        quote='用一个堆维护所有活跃事件。但是，如何修改堆中元素的优先级？我们可以用一种「懒更新」的想法：对于 updatePriority，不做更新，而是把一条新的数据插入堆。同时，额外用一个哈希表记录每个 eventId 对应的最新优先级。',
        quote_src='—— 灵茶山艾府题解',
        idea=['堆元素 `(-priority, eid)`：取负后最大优先级在堆顶，同优先级 id 小的在前',
              '`updatePriority`：哈希表改成最新值，再 push 新数据，旧数据留在堆里',
              '`pollHighest`：弹出堆顶，和哈希表对不上就是旧数据，继续弹；对上了就删掉哈希表记录并返回'],
        summary=['初始化 `O(n)`；update 和 poll 均摊 `O(log(n+q))`，每条数据至多入堆出堆各一次',
                 '易错：取走事件后要 `del` 哈希表记录，否则它的旧数据可能被误认成有效',
                 '易错：堆里存 `-priority`，核对时是 `== -priority`',
                 '同类：2349 设计数字容器系统（懒删除堆）'],
    ),
)
