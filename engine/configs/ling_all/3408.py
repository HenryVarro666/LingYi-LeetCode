CALL = """tm = TaskManager([[1, 101, 10], [2, 102, 20], [3, 103, 15]])
out = []
tm.add(4, 104, 5)
tm.edit(102, 8)
out.append(tm.execTop())
tm.rmv(101)
tm.add(5, 105, 15)
out.append(tm.execTop())
out"""

CONFIG = dict(
    num=3408, title='设计任务管理器', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 懒更新/懒删除最大堆',
    tags=['难度分 1807'],
    setup='''
heapify_max = heapq._heapify_max
heappop_max = heapq._heappop_max
def heappush_max(h, x):
    h.append(x)
    heapq._siftdown_max(h, 0, len(h) - 1)
''',
    code='''
class TaskManager:
    def __init__(self, tasks: List[List[int]]):
        self.mp = {taskId: (priority, userId) for userId, taskId, priority in tasks}
        self.h = [(priority, taskId, userId) for userId, taskId, priority in tasks]
        heapify_max(self.h)

    def add(self, userId: int, taskId: int, priority: int) -> None:
        self.mp[taskId] = (priority, userId)
        heappush_max(self.h, (priority, taskId, userId))

    def edit(self, taskId: int, newPriority: int) -> None:
        # 懒修改
        self.add(self.mp[taskId][1], taskId, newPriority)

    def rmv(self, taskId: int) -> None:
        # 懒删除
        self.mp[taskId] = (-1, -1)

    def execTop(self) -> int:
        while self.h:
            priority, taskId, userId = heappop_max(self.h)
            if self.mp[taskId] == (priority, userId):
                self.rmv(taskId)
                return userId
            # else 货不对板，堆顶和 mp 中记录的不一样，说明堆顶数据已被修改或删除，不做处理
        return -1
''',
    call=CALL,
    expect=[3, 5],
    views=[
        dict(type='map', var='self.mp', label='mp（taskId → (优先级, 用户)，最新值）',
             fmt=lambda k, v: f'{k} → {v[0]},{v[1]}', h=190, font=28),
        dict(type='heap', var='self.h', label='h（最大堆，元素 = (优先级, taskId, 用户)）',
             fmt=lambda t: f'{t[0]},{t[1]},{t[2]}', h=200),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['userId', 'taskId', 'priority', ('out', 'out', 'green')],
    max_steps=90,
    captions={
        'self.mp = {': '哈希表 `mp`：每个任务==最新的==(优先级, 用户)',
        'self.h = [': '堆里存 `(优先级, taskId, 用户)`：元组比较先看优先级，再看 `taskId` 大的在前，正好符合题意',
        'heapify_max(self.h)': '原地堆化，`O(n)` 建最大堆',
        'self.mp[taskId] = (priority, userId)': '`mp` 记下任务 `{taskId}` 的最新数据 `({priority}, {userId})`',
        'heappush_max(self.h': '新数据入堆；如果是改过的，旧数据留在堆里不动',
        'self.add(self.mp[taskId][1]': '==懒修改==：用原来的用户 `{self.mp[taskId][1]}` 再 add 一条新优先级 `{newPriority}`，旧的堆元素不找',
        'self.mp[taskId] = (-1, -1)': '==懒删除==：`mp[{taskId}]` 改成 `(-1, -1)`，堆里的旧元素以后一定对不上',
        'while self.h': lambda S, B, r: ('堆里还有元素，看堆顶' if S['self.h'] else '堆空了，没有任务可执行'),
        'heappop_max(self.h)': '弹出堆顶 `({priority}, {taskId}, {userId})`',
        'if self.mp[taskId] == (priority, userId)': lambda S, B, r: (
            f'`mp[{S.taskId}]` = {S["self.mp"][S.taskId]}，和弹出的 `({S.priority}, {S.userId})` ==一致== → 有效，就是它'
            if S['self.mp'][S.taskId] == (S.priority, S.userId)
            else f'`mp[{S.taskId}]` = {S["self.mp"][S.taskId]}，和弹出的 `({S.priority}, {S.userId})` ==不一致== → 货不对板'),
        'self.rmv(taskId)': '执行完把这个任务删掉（置为 `(-1, -1)`）',
        'return userId': '返回执行任务所属用户 `{userId}`',
        'return -1': '没有任务，返回 `-1`',
        'out.append': '这次 execTop 返回 `{out[-1]}`',
    },
    cards=dict(
        one_liner='堆里的旧数据不删不改，弹出时对不上账就丢掉',
        complexity='`add/edit/execTop` 均摊 `O(log(n+q))`，`rmv` `O(1)`',
        problem=['`add/edit/rmv` 管理任务，`execTop` 执行优先级最高的任务',
                 '优先级相同时执行 `taskId` 最大的；执行后删除，返回其 `userId`',
                 '没有任务返回 `-1`；示例两次 `execTop` 返回 `[3, 5]`'],
        quote='execTop：不断弹出「货不对板」的堆顶，也就是任务编号和哈希表中记录的数据不一致的堆顶。直到堆为空或者找到一致的数据。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最大堆管顺序，哈希表 `mp` 记每个任务==最新==的优先级和用户',
              '`edit`：直接再入堆一条新数据（懒修改）；`rmv`：把 `mp` 改成 `(-1, -1)`（懒删除）',
              '`execTop` 弹堆顶，和 `mp` 对不上就是过期数据，直接丢'],
        summary=['每个元素至多入堆、出堆各一次，均摊 `O(log(n+q))`',
                 '元组 `(优先级, taskId, 用户)` 的比较顺序刚好满足「同优先级取 taskId 大」',
                 '易错：`execTop` 执行后别忘了从 `mp` 删除，否则以后会重复执行',
                 'Python 3.14 的 `heapify_max/heappush_max/heappop_max` 已在 setup 补等价实现'],
    ),
)
