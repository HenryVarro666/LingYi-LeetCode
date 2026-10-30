---
title: "3408. 设计任务管理器"
aliases: ["yiduobo的每日leetcode 3408.设计任务管理器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31687272469"
zhihu_id: "31687272469"
zhihu_title: "yiduobo的每日leetcode 3408.设计任务管理器"
question_id: "3408"
question: "设计任务管理器"
problem_url: "https://leetcode.cn/problems/design-task-manager/"
difficulty: "Medium"
rating: 1807
created: "2025-03-21T02:39:20+08:00"
updated: "2025-03-21T02:39:20+08:00"
upvotes: 0
comments: 0
---

# 3408. 设计任务管理器

> **[yiduobo的每日leetcode 3408.设计任务管理器](https://zhuanlan.zhihu.com/p/31687272469) · 知乎 · 2025-03-21 · 赞同 0**
> 力扣：[3408. 设计任务管理器](https://leetcode.cn/problems/design-task-manager/) · Medium · 灵茶山艾府：[懒删除堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3408.设计任务管理器

[3408. 设计任务管理器 - 力扣（LeetCode）](https://leetcode.cn/problems/design-task-manager/description/)

题目要求设计一个任务管理系统，这个系统需要高效处理添加、修改、执行、删除任务的操作。具体来说：

TaskManager(tasks)：初始化任务管理器，其中tasks\[i\] \= \[userId\[i\], taskId\[i\], priority\[i\]\]，表示为userId\[i\]添加一个优先级为priority\[i\]的任务taskId\[i\]。

add(userId, taskId, priority)：添加任务。表示给用户userId添加一个优先级为priority的任务taskId。

edit(taskId, newPriority)：修改任务。表示将任务taskId的优先级修改为newPriority。

rmv(taskId)：删除任务。表示将任务taskId从系统中删除。

execTop()：执行任务。表示执行所有任务中优先级最高的任务。如果有多个优先级最高，则执行taskId最大的任务。执行完毕后taskId从系统中删除，同时返回这个任务所属的userId。若不存在任何任务，返回-1。

逐个分析题目的需求：

TaskManager(tasks)：

直接调用接下来需要实现的add多次就行了

add(userId, taskId, priority)：

目前看来需要使用某种数据结构将每个任务的信息保存下来，但是具体用什么还需要看后面的需求再进行分析

edit(taskId, newPriority)：

出现了根据taskId修改任务优先级的需求，也就是说需要能通过taskId高效定位，同时还可以高效地将修改后的信息填充回去，因此在这里使用哈希表是比较合适的。

哈希表的key为taskId，value为(userId, priority)形成的二元组。

rmv(taskId)：

使用哈希表的话直接pop掉key为taskId的元素就行了，目前不需要额外的处理。

execTop()：

由于需要执行优先级最高，且taskId最大的任务，那么在这里使用堆来维护这些任务是比较合适的。由于默认是小根对，那么堆中保存的应该是(-priority, -taskId, userId)形成的三元组。

这样的话，在add操作以及edit操作中则需要也将新的任务或者更新后的任务加入到堆中。另一方面，由于原生的堆不好删除，因此在这里可以采取懒删除的方法，在需要使用堆顶信息时再与哈希表中的信息进行比较，如果不一致说明过期了，此时再删除堆顶信息也不迟。

---

这样一来，对于本题中各种操作的具体实现：

TaskManager(tasks)：

初始化哈希表task_dict为空的dict，初始化堆task_heap为空的堆，然后遍历tasks中的每个任务，对于每个任务分别调用add操作。

add(userId, taskId, priority)：

以taskId为key，二元组(userId, priority)为value更新哈希表task_dict，然后将三元组(-priority, -taskId, userId)加入堆task_heap。

edit(taskId, newPriority)：

从task_dict中取出key为taskId的元素(userId, priority)，然后将(userId, newPriority)重新赋值给task_dict[taskId]，最后将(-newPriority, -taskId, userId)加入到堆task_heap中。

需要注意这里不直接对堆中老的信息进行删除，而是等到其出现在堆顶时再执行删除操作。

rmv(taskId)：

从task_dict中删去key为taskId的元素即可，同样的，这里也不直接对堆中的信息进行删除。

execTop()：

若堆不为空，就对比堆顶的任务信息能否与哈希表中的信息匹配上，如果不行，则删除堆顶的信息。重复此过程直到堆顶的信息可以匹配或者堆为空为止。

接下来，若堆为空，则返回-1，否则将堆顶信息从堆中弹出，然后将对应的taskId从哈希表中删去，最后返回对应的userId即可。

最后附上python代码：

```python
class TaskManager(object):

    def __init__(self, tasks):
        """
        :type tasks: List[List[int]]
        """
        self.task_dict = {}
        self.task_heap = []

        for userId, taskId, priority in tasks:
            self.add(userId, taskId, priority)

    def add(self, userId, taskId, priority):
        """
        :type userId: int
        :type taskId: int
        :type priority: int
        :rtype: None
        """
        self.task_dict[taskId] = (userId, priority)
        heapq.heappush(self.task_heap, (-priority, -taskId, userId))

    def edit(self, taskId, newPriority):
        """
        :type taskId: int
        :type newPriority: int
        :rtype: None
        """
        userId, priority = self.task_dict[taskId]
        self.task_dict[taskId] = (userId, newPriority)
        heapq.heappush(self.task_heap, (-newPriority, -taskId, userId))

    def rmv(self, taskId):
        """
        :type taskId: int
        :rtype: None
        """
        self.task_dict.pop(taskId)

    def execTop(self):
        """
        :rtype: int
        """
        while self.task_heap:
            priority, taskId, userId = heapq.heappop(self.task_heap)
            priority = -priority
            taskId = -taskId
            if self.task_dict.get(taskId, None) == (userId, priority):
                self.task_dict.pop(taskId)
                return userId
        
        return -1

# Your TaskManager object will be instantiated and called as such:
# obj = TaskManager(tasks)
# obj.add(userId,taskId,priority)
# obj.edit(taskId,newPriority)
# obj.rmv(taskId)
# param_4 = obj.execTop()
```
