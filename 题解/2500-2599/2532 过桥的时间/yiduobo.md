---
title: "2532. 过桥的时间"
aliases: ["yiduobo的每日leetcode 2532.过桥的时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/编程能力强化训练"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637167348"
zhihu_id: "637167348"
zhihu_title: "yiduobo的每日leetcode 2532.过桥的时间"
question_id: "2532"
question: "过桥的时间"
problem_url: "https://leetcode.cn/problems/time-to-cross-a-bridge/"
difficulty: "Hard"
rating: 2589
created: "2023-06-15T00:49:05+08:00"
updated: "2023-06-15T00:49:05+08:00"
upvotes: 0
comments: 0
---

# 2532. 过桥的时间

> **[yiduobo的每日leetcode 2532.过桥的时间](https://zhuanlan.zhihu.com/p/637167348) · 知乎 · 2023-06-15 · 赞同 0**
> 力扣：[2532. 过桥的时间](https://leetcode.cn/problems/time-to-cross-a-bridge/) · Hard · 灵茶山艾府：[复杂模拟题如何思考？视频讲解！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2532.过桥的时间

[力扣](https://leetcode.cn/problems/time-to-cross-a-bridge/)

较为复杂的时序模拟题。本题中单个工人有四种状态，分别是在桥左侧等待、在桥右侧等待、从右侧仓库搬运货物到桥右侧、从左侧仓库搬运货物到桥左侧。

由于本题中只有过桥是独占的，而其他动作可以并行，因此本题的时间节点应该围绕桥的空闲时刻展开。对于在桥两侧等待的操作，就只需使用堆来维护工人效率以及工人的下标，而对于搬运货物的操作，则需要使用堆来维护搬运完成的时间，从而通过时间节点判断当前搬运工作是否完成。但是在这里为了定位到具体的工人，因此也同样需要维护当前工人的下标。

另外，有一种特殊情况是所有工人都在搬运，桥是一直空闲的，这种情况出现时下一个时间节点的选取则应该是最早完成搬运的时刻而不再是桥的空闲时刻。

需要特别注意的是，题目问的是最后一个搬运箱子的工人来到桥左侧的时间，而不是最后一件货物入库的时间。因此在这里只需右侧仓库被搬运空，且最后一个位于桥右侧的工人过桥了，就算完成任务了。

根据上面的描述，就得到了下面的算法：

1、使用四个堆left_bridge、right_bridge、left_warehouse、right_warehouse分别维护处于在桥左侧等待、在桥右侧等待、从左侧仓库搬运货物到桥左侧、从右侧仓库搬运货物到桥右侧四种状态的工人。

其中left_bridge、right_bridge以工人来回过桥的时间之和为第一关键字，工人下标为第二关键字的大顶堆，而left_warehouse、right_warehouse则是以工人完成搬运的时间为第一关键字，工人下标为第二关键字的小顶堆。具体实现上，可以通过将数值取反，使用小顶堆来替代大顶堆。

2、接下来，使用一个变量now表示当前的时间节点。

若待搬运货物n大于0，或者right_bridge、right_warehouse不都为空，也就是还有工人在桥的右侧，那么就需要不断执行以下操作，直到n等于0且没有工人还位于桥的右侧为止。

2-1）若left_warehouse非空，且其中完成搬运工作的最早时间小于等于now，那么就将对应的工人从left_warehouse中移除，并将其加入到left_bridge中。重复此过程直到left_warehouse为空或者其中完成搬运工作的最早时间大于now为止。

2-2）同样的，若right_warehouse非空，且其中完成搬运工作的最早时间小于等于now，那么就将对应工人从right_warehouse中移除，并将其加入到right_bridge中。重复此过程直到right_warehouse为空或者其中完成搬运工作的最早时间大于now为止。

2-3）接下来，则需要安排工人过桥。

若right_bridge非空，那么就安排右侧的工人过桥。设这位工人的下标为index，那么其过桥后时间节点将会从now变为now + time[index][2]，需要更新now。而对于这位工人，则需要先将其从right_bridge中移除，然后还需要安排其完成入左侧仓库的工作，因此需要将其加入到left_warehouse中，其完成入库工作的时间则是新的now再加上time[index][3]。

若right_bridge为空，且left_bridge非空同时n > 0，那么就安排左侧的工人过桥。设这位工人的下标为index，那么其过桥后时间节点将会从now变为now + time[index][0]，需要更新now。而对于这位工人，则需要先将其从left_bridge中移除，然后还需要安排其完成从右侧仓库搬运到桥的工作，因此需要将其加入到right_warehouse中，其完成搬运到桥工作的时间则是新的now再加上time[index][1]。另外，在这里还需将n减去1，表示有一件货物开始被搬运了。

若left_bridge和right_bridge都为空，那么就出现了上面描述的所有工人都在搬运，桥一直是空闲的情况。此时则需要找出left_warehouse和right_warehouse中完成搬运的最早时间点next_t，然后使用next_t更新now。

最后附上python代码：

```python
class Solution(object):
    def findCrossingTime(self, n, k, time):
        """
        :type n: int
        :type k: int
        :type time: List[List[int]]
        :rtype: int
        """

        left_bridge = []
        left_warehouse = []
        right_bridge = []
        right_warehouse = []

        for index, (l2r, pick, r2l, put) in enumerate(time):
            heapq.heappush(left_bridge, [-l2r - r2l, -index])
        
        now = 0
        while n > 0 or right_bridge or right_warehouse:
            while left_warehouse and left_warehouse[0][0] <= now:
                t, index = heapq.heappop(left_warehouse)
                heapq.heappush(left_bridge, [-time[index][0] - time[index][2], -index])
            
            while right_warehouse and right_warehouse[0][0] <= now:
                t, index = heapq.heappop(right_warehouse)
                heapq.heappush(right_bridge, [-time[index][0] - time[index][2], -index])
            
            if right_bridge:
                _, index = heapq.heappop(right_bridge)
                index = -index
                now += time[index][2]
                heapq.heappush(left_warehouse, [now + time[index][3], index])
            elif left_bridge and n > 0:
                _, index = heapq.heappop(left_bridge)
                index = -index
                now += time[index][0]
                heapq.heappush(right_warehouse, [now + time[index][1], index])
                n -= 1
            else:
                next_t = None
                if left_warehouse:
                    next_t = left_warehouse[0][0]
                if right_warehouse:
                    if next_t is None or next_t > right_warehouse[0][0]:
                        next_t = right_warehouse[0][0]
                
                now = next_t
        
        return now
```
