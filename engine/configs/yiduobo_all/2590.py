CONFIG = dict(
    num=2590, title='设计一个待办事项清单', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表 + 列表',
    tags=[],
    code='''
class TodoList(object):

    def __init__(self):
        self.task_dict = {}
        self.nxt_id = 1

    def addTask(self, userId, taskDescription, dueDate, tags):
        if userId not in self.task_dict:
            self.task_dict[userId] = []
        
        self.task_dict[userId].append([self.nxt_id, taskDescription, dueDate, tags[:]])
        self.nxt_id += 1
        return self.nxt_id - 1

    def getAllTasks(self, userId):
        return [task[1] for task in sorted(self.task_dict.get(userId, []), key=lambda d:d[2])]

    def getTasksForTag(self, userId, tag):
        task_list= []
        for task in self.task_dict.get(userId, []):
            if tag in task[-1]:
                task_list.append([task[1], task[2]])
        
        return [task[0] for task in sorted(task_list, key=lambda d:d[1])]

    def completeTask(self, userId, taskId):
        if userId in self.task_dict:
            for index in range(len(self.task_dict[userId])):
                if self.task_dict[userId][index][0] == taskId:
                    self.task_dict[userId].pop(index)
                    break
''',
    call='''t = TodoList()
out = []
out.append(t.addTask(1, "Task1", 50, []))
out.append(t.addTask(1, "Task2", 100, ["P1"]))
out.append(t.getAllTasks(1))
out.append(t.addTask(1, "Task3", 30, ["P1"]))
out.append(t.getTasksForTag(1, "P1"))
t.completeTask(1, 2)
out.append(t.getAllTasks(1))
out''',
    expect=[1, 2, ['Task1', 'Task2'], 3, ['Task3', 'Task2'], ['Task3', 'Task1']],
    views=[
        dict(type='map', var='self.task_dict', label='task_dict（userId → 任务列表；每项 id:描述@截止日期#tag）',
             fmt=lambda k, v: '  '.join(f"{x[0]}:{x[1]}@{x[2]}" + ''.join('#' + g for g in x[3]) for x in v) or '（空）', font=24, h=170),
        dict(type='array', var=lambda S: [t[1] for t in sorted(S['task_list'], key=lambda d: d[1])] if 'task_list' in S else None,
             label='getTasksForTag：命中的任务按截止日期排序（描述）', cell=130, h=170),
        dict(type='calls', label='正在执行', h=150),
    ],
    watch=[('下一个 id', 'self.nxt_id', 'green'), 'userId', 'taskId', 'tag'],
    skip=['self.task_dict = {}', 'self.nxt_id = 1', 'task_list= []', 'task_list.append'],
    captions={
        'self.task_dict[userId] = []': '这个用户第一次出现：在哈希表里建一份空清单',
        'if userId not in self.task_dict': lambda S, B, r: ('`userId = {}` 还不在哈希表里'.format(S.userId) if S.userId not in B['self.task_dict'] else '`userId = {}` 已有清单'.format(S.userId)),
        '.append([self.nxt_id': '四元组 `[id={self.nxt_id}, {taskDescription}, 截止 {dueDate}, tags]` 加到清单末尾；`tags[:]` 复制一份，避免外部修改',
        'self.nxt_id += 1': '`nxt_id` 加 1，给下一个任务用',
        'return self.nxt_id - 1': '返回刚添加的任务 id ==`{ret}`==',
        'return [task[1] for task in sorted': '按截止日期 `d[2]` 排序后，只收集任务描述：`{ret}`',
        'for task in self.task_dict.get': '遍历 `userId = {userId}` 的清单，没有该用户就当空清单',
        'if tag in task[-1]': lambda S, B, r: ('任务 `{}` 的 tags 含 `{}` → 收集（描述 + 截止日期）'.format(S.task[1], S.tag) if S.tag in S.task[-1]
                                               else '任务 `{}` 的 tags 不含 `{}` → 跳过'.format(S.task[1], S.tag)),
        'return [task[0] for task in sorted(task_list': '命中的任务按截止日期 `d[1]` 排序，再取描述：`{ret}`',
        'if userId in self.task_dict': lambda S, B, r: '`userId = {}` 有清单，去找 `taskId = {}`'.format(S.userId, S.taskId) if S.userId in B['self.task_dict'] else '用户不存在 → 什么都不做',
        'for index in range': '依次检查清单里的每个任务',
        'if self.task_dict[userId][index][0] == taskId': lambda S, B, r: '第 {} 个任务 id = {}，{}'.format(S.index, S.task_dict[S.userId][S.index][0] if False else S['self.task_dict'][S.userId][S.index][0], '正是要完成的 `taskId`' if S['self.task_dict'][S.userId][S.index][0] == S.taskId else '不是目标，继续'),
        '.pop(index)': '把这个任务从清单里弹出，即「完成」了它',
        'break': 'id 唯一，找到就可以停',
    },
    cards=dict(
        one_liner='数据很小：每个用户一份列表，查询时现排序',
        complexity='`addTask` `O(1)`；`getAllTasks` `O(k log k)`；`completeTask` `O(k)`（k = 用户任务数）',
        problem=['设计待办清单：`addTask` 添加任务并返回唯一 id，`getAllTasks` 按截止日期返回描述',
                 '`getTasksForTag` 只返回带指定 tag 的任务；`completeTask` 完成并删除任务',
                 '示例：加入 `Task1(50)`、`Task2(100,P1)`、`Task3(30,P1)`'],
        quote='题目的数据规模很小，因此无需过多考虑时间复杂度相关的问题，可以直接使用一个哈希表储存每个用户的待办事项。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表：`userId` → 任务列表，任务 = `[id, 描述, 截止日期, tags]`',
              '`nxt_id` 记录下一个任务 id，每次添加后加 1',
              '查询时先过滤、再按截止日期排序；完成时遍历找 id 并 `pop`'],
        summary=['不需要复杂结构：数据规模小，每次查询现排序即可',
                 '易错：`tags[:]` 要复制一份；返回 id 要用 `nxt_id - 1`',
                 '`getTasksForTag` 先收集 `[描述, 截止日期]`，排序后再只取描述',
                 '代码未改，原文已是 Python 3 可运行的写法；题面库里没有，示例按官方样例精简'],
    ),
)
