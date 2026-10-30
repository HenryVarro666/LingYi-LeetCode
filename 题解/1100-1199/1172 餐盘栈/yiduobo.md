---
title: "1172. 餐盘栈"
aliases: ["yiduobo的每日leetcode 1172.餐盘栈"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/design", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/三-栈", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379724320"
zhihu_id: "379724320"
zhihu_title: "yiduobo的每日leetcode 1172.餐盘栈"
question_id: "1172"
question: "餐盘栈"
problem_url: "https://leetcode.cn/problems/dinner-plate-stacks/"
difficulty: "Hard"
rating: 2110
created: "2021-06-10T23:45:03+08:00"
updated: "2021-06-10T23:45:03+08:00"
upvotes: 0
comments: 0
---

# 1172. 餐盘栈

> **[yiduobo的每日leetcode 1172.餐盘栈](https://zhuanlan.zhihu.com/p/379724320) · 知乎 · 2021-06-10 · 赞同 0**
> 力扣：[1172. 餐盘栈](https://leetcode.cn/problems/dinner-plate-stacks/) · Hard · 灵茶山艾府：[与其维护第一个未满栈，不如维护所有未满栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1172.餐盘栈

[力扣](https://leetcode-cn.com/problems/dinner-plate-stacks/)

题目要求我们维护一系列容量为capacity的栈，并给出了几种操作：

1、push操作，需要将给定的num压入编号最小的非满栈中。

2、pop操作，将最后一个非空栈的栈顶弹出

3、pop at stack操作，将指定栈的栈顶弹出

首先，由于需要维护一系列的栈，同时需要有下标访问的能力，那么我们需要使用一个list为维护这些栈。那么此时对于操作2和操作3都是比较容易实现的：

2、pop操作，我们只需要从list的末尾开始向前进行检测。若当前栈为空，那么将其从list当中移除，并继续考察前一个栈。若当前栈不为空，那么此时应该返回栈顶元素。若最终将所有栈都从list中移除，那么返回-1。

3、pop at stack操作，若指定栈编号大于当前栈的数量，或者指定栈为空，那么返回-1，否则将指定栈的栈顶弹出。

接下来还需要处理push操作。push操作要求我们在任意时刻都可以很快得知当前编号最小的非满栈的下标，那么一个自然的想法就是使用一个堆来维护所有非满栈的下标，那么堆顶元素对应的栈就是当前下标最小的非满栈。

那么对于push操作，若当前堆中有元素，设堆顶为p，那么就将num插入到第p个栈中，否则在list的末尾新加入一个栈，然后将num插入到最后这个栈中。

另外，关于这个堆，我们也应当在适当的时候更新里面的参数。对于每种操作：

1、push操作，在push完成之后，若当前push的栈非满，那么需要将栈的下标加入到堆中。

2、pop操作，在pop完成之后，若当前pop的栈由于本次pop操作从满栈变成了非满栈，那么需要将栈的下标加入到堆中。需要注意的是，这里只有在栈的状态从满栈变成非满栈的时候才需要将其加入到堆中。

3、pop at stack操作，与情况2类似，也是若当前pop的栈由于本次pop操作从满栈变成了非满栈，那么就将其加入到堆中。

至此，我们在使用一个list加一个堆的情况下就可以实现题目的所有要求了。

最后附上python代码：

```python
class DinnerPlates(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.stacks = []
        self.heap = []
        self.capacity = capacity

    def push(self, val):
        """
        :type val: int
        :rtype: None
        """

        if not self.heap:
            self.stacks.append([])
            self.stacks[-1].append(val)
            p = len(self.stacks) - 1
        else:
            p = heapq.heappop(self.heap)
            if len(self.stacks) - 1 < p:
                self.stacks.append([])
            self.stacks[p].append(val)

        if len(self.stacks[p]) < self.capacity:
            heapq.heappush(self.heap, p)

    def pop(self):
        """
        :rtype: int
        """

        while self.stacks and len(self.stacks[-1]) == 0:
            self.stacks.pop()
        
        if not self.stacks:
            return -1
        
        p = len(self.stacks) - 1
        if len(self.stacks[p]) == self.capacity:
            heapq.heappush(self.heap, p)

        return self.stacks[p].pop()

    def popAtStack(self, index):
        """
        :type index: int
        :rtype: int
        """

        if len(self.stacks) - 1 < index:
            return -1
        
        if not self.stacks[index]:
            return -1
        
        if len(self.stacks[index]) == self.capacity:
            heapq.heappush(self.heap, index)
        
        return self.stacks[index].pop()

# Your DinnerPlates object will be instantiated and called as such:
# obj = DinnerPlates(capacity)
# obj.push(val)
# param_2 = obj.pop()
# param_3 = obj.popAtStack(index)
```
