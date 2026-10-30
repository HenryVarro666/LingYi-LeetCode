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
    author='yiduobo', technique='哈希表 + 小根堆（取负）懒删除',
    tags=['难度分 1807'],
    code='''
class TaskManager(object):

    def __init__(self, tasks):
        self.task_dict = {}
        self.task_heap = []

        for userId, taskId, priority in tasks:
            self.add(userId, taskId, priority)

    def add(self, userId, taskId, priority):
        self.task_dict[taskId] = (userId, priority)
        heapq.heappush(self.task_heap, (-priority, -taskId, userId))

    def edit(self, taskId, newPriority):
        userId, priority = self.task_dict[taskId]
        self.task_dict[taskId] = (userId, newPriority)
        heapq.heappush(self.task_heap, (-newPriority, -taskId, userId))

    def rmv(self, taskId):
        self.task_dict.pop(taskId)

    def execTop(self):
        while self.task_heap:
            priority, taskId, userId = heapq.heappop(self.task_heap)
            priority = -priority
            taskId = -taskId
            if self.task_dict.get(taskId, None) == (userId, priority):
                self.task_dict.pop(taskId)
                return userId
        
        return -1
''',
    call=CALL,
    expect=[3, 5],
    views=[
        dict(type='map', var='self.task_dict', label='task_dict（taskId → (用户, 优先级)）',
             fmt=lambda k, v: f'{k} → {v[0]},{v[1]}', h=190, font=28),
        dict(type='heap', var='self.task_heap', label='task_heap（小根堆，元素 = (−优先级, −taskId, 用户)）',
             fmt=lambda t: f'{t[0]},{t[1]},{t[2]}', h=200),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['userId', 'taskId', 'priority', ('out', 'out', 'green')],
    max_steps=90,
    captions={
        'self.task_dict = {}': '哈希表：`taskId` → `(userId, priority)`，能按 `taskId` 直接定位和修改',
        'self.task_heap = []': '堆默认小根堆，存 `(-优先级, -taskId, userId)`，堆顶就是优先级最高、同级 taskId 最大的',
        'self.add(userId, taskId, priority)': '初始化不重写逻辑，直接调用 `add`',
        'self.task_dict[taskId] = (userId, priority)': '哈希表记下任务 `{taskId}`：`({userId}, {priority})`',
        'heapq.heappush(self.task_heap, (-priority': '`({-priority}, {-taskId}, {userId})` 入堆',
        'self.task_dict[taskId] = (userId, newPriority)': '哈希表里改成新优先级 `{newPriority}`，堆里的旧数据先不动',
        'userId, priority = self.task_dict[taskId]': '先从哈希表取出任务 `{taskId}` 的用户 `{userId}`',
        'heapq.heappush(self.task_heap, (-newPriority': '把新数据 `({-newPriority}, {-taskId}, {userId})` 也加进堆，旧数据等它到堆顶再删',
        'self.task_dict.pop(taskId)': lambda S, B, r: (
            f'==懒删除==：只从哈希表删掉任务 `{S.taskId}`，堆里的旧数据以后对账时必然对不上' if S['_line'] == 20
            else f'任务 `{S.taskId}` 执行完毕，从哈希表删除（以后堆里的同名旧数据会被丢弃）'),
        'while self.task_heap': lambda S, B, r: ('堆非空，检查堆顶' if S['self.task_heap'] else '堆空了，没有任务'),
        'heapq.heappop(self.task_heap)': '弹出堆顶 `({priority}, {taskId}, {userId})`（还是取负的值）',
        'priority = -priority': '取负还原优先级：`{priority}`',
        'taskId = -taskId': '取负还原 taskId：`{taskId}`',
        'if self.task_dict.get': lambda S, B, r: (
            f'哈希表里 `{S.taskId}` 是 `{S["self.task_dict"].get(S.taskId)}`，和 `({S.userId}, {S.priority})` ==一致== → 有效'
            if S['self.task_dict'].get(S.taskId) == (S.userId, S.priority)
            else f'哈希表里 `{S.taskId}` 是 `{S["self.task_dict"].get(S.taskId)}`，和 `({S.userId}, {S.priority})` ==对不上== → 已过期，直接丢弃'),
        'return userId': '执行任务，返回用户 `{userId}`',
        'return -1': '没有任务，返回 `-1`',
        'out.append': '这次 execTop 返回 `{out[-1]}`',
    },
    cards=dict(
        one_liner='先用哈希表记最新状态，堆里过期的等弹出时再丢',
        complexity='`add/edit/execTop` 均摊 `O(log n)`，`rmv` `O(1)`',
        problem=['`add/edit/rmv` 管理任务，`execTop` 执行优先级最高的任务',
                 '优先级相同取 `taskId` 最大的；执行后删除并返回 `userId`',
                 '没有任务返回 `-1`；示例两次 `execTop` 返回 `[3, 5]`'],
        quote='由于原生的堆不好删除，因此在这里可以采取懒删除的方法，在需要使用堆顶信息时再与哈希表中的信息进行比较，如果不一致说明过期了，此时再删除堆顶信息也不迟。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐个需求拆解：按 `taskId` 改和删 → 哈希表；取最大 → 堆',
              '默认小根堆，所以存 `-priority`、`-taskId`，同优先级时 `taskId` 大的排前面',
              '`edit`/`rmv` 只改哈希表，`execTop` 时再对账、丢过期数据'],
        summary=['每个堆元素至多出堆一次，均摊 `O(log n)`',
                 '`rmv` 是 `pop` 哈希表，堆里旧元素留着，所以 `execTop` 必须用 `get` 对账',
                 '易错：堆里是取负的值，对账前要把 `priority`、`taskId` 还原',
                 '对比灵神：灵神 `rmv` 置 `(-1,-1)` 并用最大堆工具函数，这里取负 + 哈希表 `pop`',
                 '原文为 Python 3 可运行写法，无需修改'],
    ),
)
