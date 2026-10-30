---
title: "3885. 设计时间管理器"
aliases: ["yiduobo的每日leetcode 3885.设计时间管理器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022790052934161659"
zhihu_id: "2022790052934161659"
zhihu_title: "yiduobo的每日leetcode 3885.设计时间管理器"
question_id: "3885"
question: "设计事件管理器"
problem_url: "https://leetcode.cn/problems/design-event-manager/"
difficulty: "Medium"
rating: 1548
created: "2026-04-01T21:47:35+08:00"
updated: "2026-04-01T21:47:35+08:00"
upvotes: 1
comments: 0
---

# 3885. 设计时间管理器

> **[yiduobo的每日leetcode 3885.设计时间管理器](https://zhuanlan.zhihu.com/p/2022790052934161659) · 知乎 · 2026-04-01 · 赞同 1**
> 力扣：[3885. 设计事件管理器](https://leetcode.cn/problems/design-event-manager/) · Medium · 灵茶山艾府：[懒更新堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3885.设计时间管理器

<https://leetcode.cn/problems/design-event-manager/description/>

题目给出一组初始事件列表，其中每个事件都有一个唯一的eventId以及一个priority(优先级)。

现在要求实现EventManager类：

- 构造函数EventManager(events)，表示使用给定的事件初始化管理器，其中events\[index\] \= \[eventId\[index\], priority\[index\]\]
- updatePriority(eventId, newPrioriry)，表示将id为eventId的活跃事件的优先级更新为newPriority
- pollHighest()，表示移除掉具有最高优先级的活跃事件的eventId，若有多个活动事件具有相同的优先级，那么就返回eventId最小的事件。若没有活跃事件，则返回-1

注意这里的活跃事件指的是没有被pollHighest移除的事件。

题目实际上就是要实现一个具有修改功能的堆，在这里可以采用懒更新的策略，使用哈希表配合原生的堆来实现。

具体来说，就是使用一个哈希表记录每个eventId对应的priority，同时使用一个堆记录所有(priority, eventId)的pair对。

接下来对于update操作，若eventId依然存在于哈希表中，那么就将哈希表中eventId对应的priority更新为newPriority，同时将(newPriority, eventId)加入到堆中，反之则不执行任何操作。

而对于pollHighest操作，则只需不停从堆中弹出堆顶的pair对(pri, eid)，若eid存在于哈希表中，同时其对应的priority恰好等于pri，那么就将eid从哈希表中弹出，并返回eid。重复此过程，直到堆为空或者找到了合法的eid为止。

最后附上python代码：

```python
class EventManager(object):

    def __init__(self, events):
        """
        :type events: List[List[int]]
        """
        self.heap = []
        self.hash = {}
        for eid, pri in events:
            heapq.heappush(self.heap, (-pri, eid))
            self.hash[eid] = pri

    def updatePriority(self, eventId, newPriority):
        """
        :type eventId: int
        :type newPriority: int
        :rtype: None
        """
        if eventId in self.hash and newPriority != self.hash[eventId]:
            self.hash[eventId] = newPriority
            heapq.heappush(self.heap, (-newPriority, eventId))

    def pollHighest(self):
        """
        :rtype: int
        """
        while self.heap:
            pri, eid = heapq.heappop(self.heap)
            if eid in self.hash and self.hash[eid] == -pri:
                self.hash.pop(eid)
                return eid
        
        return -1

# Your EventManager object will be instantiated and called as such:
# obj = EventManager(events)
# obj.updatePriority(eventId,newPriority)
# param_2 = obj.pollHighest()
```
