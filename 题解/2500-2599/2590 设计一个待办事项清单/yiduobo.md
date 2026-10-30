---
title: "2590. 设计一个待办事项清单"
aliases: ["yiduobo的每日leetcode 2590.设计一个待办事项清单"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643443057"
zhihu_id: "643443057"
zhihu_title: "yiduobo的每日leetcode 2590.设计一个待办事项清单"
question_id: "2590"
question: "设计一个待办事项清单"
problem_url: "https://leetcode.cn/problems/design-a-todo-list/"
created: "2023-07-13T23:19:00+08:00"
updated: "2023-07-13T23:19:00+08:00"
upvotes: 0
comments: 0
---

# 2590. 设计一个待办事项清单

> **[yiduobo的每日leetcode 2590.设计一个待办事项清单](https://zhuanlan.zhihu.com/p/643443057) · 知乎 · 2023-07-13 · 赞同 0**
> 力扣：[2590. 设计一个待办事项清单](https://leetcode.cn/problems/design-a-todo-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2590.设计一个待办事项清单

[力扣](https://leetcode.cn/problems/design-a-todo-list/)

题目的数据规模很小，因此无需过多考虑时间复杂度相关的问题，可以直接使用一个哈希表储存每个用户的待办事项。哈希表的key为用户的id，value则为待办事项的一个list，其中记录了每个事项的id、描述、截止日期以及tag。那么对于题目中的几种操作：

1、addTask：

首先在哈希表中通过userId定位到其对应的待办事项清单，若哈希表中原先没有userId，那么就将其加入到哈希表中，并初始化其待办事项情况为空。

接下来，将四元组任务id、任务描述、截止日期以及tag列表将入到哈希表的末尾。为了得到唯一的任务id，这里还需要使用一个变量nxt_id记录下一个任务的id是什么。每次添加之后，都需要将nxt_id加上1。

添加完成后，返回当前任务的id即可。

2、getAllTasks：

若userId不存在于哈希表中，那么结果就是空，否则就将其对应的清单按照截止日期排序后，将排序后的任务描述按顺序收集到一个list中返回。

3、getTasksForTag：

若userId不存在于哈希表中，那么结果就是空，否则就遍历其对应的清单，将清单中tag列表包含指定tag的任务描述以及截止日期收集起来，然后按照截止日期排序后，在按顺序将任务描述收集到list中返回。

4、completeTask：

若userId不存在于哈希表中，那么就不进行任何操作，否则表里其对应的清单，若清单中某个任务的id与指定的taskId相同，那么就将该任务从清单中弹出。

最后附上python代码：

```python
class TodoList(object):

    def __init__(self):
        self.task_dict = {}
        self.nxt_id = 1

    def addTask(self, userId, taskDescription, dueDate, tags):
        """
        :type userId: int
        :type taskDescription: str
        :type dueDate: int
        :type tags: List[str]
        :rtype: int
        """
        if userId not in self.task_dict:
            self.task_dict[userId] = []
        
        self.task_dict[userId].append([self.nxt_id, taskDescription, dueDate, tags[:]])
        self.nxt_id += 1
        return self.nxt_id - 1

    def getAllTasks(self, userId):
        """
        :type userId: int
        :rtype: List[str]
        """
        return [task[1] for task in sorted(self.task_dict.get(userId, []), key=lambda d:d[2])]

    def getTasksForTag(self, userId, tag):
        """
        :type userId: int
        :type tag: str
        :rtype: List[str]
        """
        task_list= []
        for task in self.task_dict.get(userId, []):
            if tag in task[-1]:
                task_list.append([task[1], task[2]])
        
        return [task[0] for task in sorted(task_list, key=lambda d:d[1])]

    def completeTask(self, userId, taskId):
        """
        :type userId: int
        :type taskId: int
        :rtype: None
        """
        if userId in self.task_dict:
            for index in range(len(self.task_dict[userId])):
                if self.task_dict[userId][index][0] == taskId:
                    self.task_dict[userId].pop(index)
                    break

# Your TodoList object will be instantiated and called as such:
# obj = TodoList()
# param_1 = obj.addTask(userId,taskDescription,dueDate,tags)
# param_2 = obj.getAllTasks(userId)
# param_3 = obj.getTasksForTag(userId,tag)
# obj.completeTask(userId,taskId)
```
