---
title: "1942. 最小未被占据椅子的编号"
aliases: ["yiduobo的每日leetcode 1942.最小未被占据椅子的编号"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap", "leetcode/you-xian-dui-lie", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/489871231"
zhihu_id: "489871231"
zhihu_title: "yiduobo的每日leetcode 1942.最小未被占据椅子的编号"
question_id: "1942"
question: "最小未被占据椅子的编号"
problem_url: "https://leetcode.cn/problems/the-number-of-the-smallest-unoccupied-chair/"
difficulty: "Medium"
rating: 1695
created: "2022-03-29T21:59:31+08:00"
updated: "2022-03-29T21:59:31+08:00"
upvotes: 0
comments: 0
---

# 1942. 最小未被占据椅子的编号

> **[yiduobo的每日leetcode 1942.最小未被占据椅子的编号](https://zhuanlan.zhihu.com/p/489871231) · 知乎 · 2022-03-29 · 赞同 0**
> 力扣：[1942. 最小未被占据椅子的编号](https://leetcode.cn/problems/the-number-of-the-smallest-unoccupied-chair/) · Medium · 灵茶山艾府：[两种做法：Bitset 或堆](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1942.最小未被占据椅子的编号

[力扣](https://leetcode-cn.com/problems/the-number-of-the-smallest-unoccupied-chair/)

又是最小系列中的一题，之前遇到过的包括安排工作，吃饭，cpu运算啥的。本题的做法也是类似，使用两个堆，分别维护当前空闲的椅子编号，以及当前在使用的椅子什么时候能空出来。

具体实现上，按照每个人的到达时间从小到大进行排序，然后一趟遍历，对于当前的顾客：

1、首先将正在使用的椅子中，空闲时间小于等于当前顾客到达时间的椅子从堆中弹出

2、接下来弹出空闲椅子的堆顶，安排给当前的顾客。此时应该将这张椅子按照当前顾客离开的时间加入到正在使用的椅子的堆中。若当前顾客时目标顾客，那么返回这张椅子的编号

需要注意的是，由于这里一共有n个顾客，因此初始状态下需要准备n张空闲的椅子。

最后附上python代码：

```python
class Solution(object):
    def smallestChair(self, times, targetFriend):
        """
        :type times: List[List[int]]
        :type targetFriend: int
        :rtype: int
        """

        n = len(times)
        idle = range(n)
        using = []
        sorted_times = sorted([[index, arrival, leaving] for index, [arrival, leaving] in enumerate(times)], key=lambda d:d[1])
        for index, arrival, leaving in sorted_times:
            while using and using[0][0] <= arrival:
                _, num = heapq.heappop(using)
                heapq.heappush(idle, num)
            
            num = heapq.heappop(idle)
            heapq.heappush(using, [leaving, num])

            if targetFriend == index:
                return num
```
