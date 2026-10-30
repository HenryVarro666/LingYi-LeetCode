---
title: "2534. 通过门的时间"
aliases: ["yiduobo的每日leetcode 2534.通过门的时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637171523"
zhihu_id: "637171523"
zhihu_title: "yiduobo的每日leetcode 2534.通过门的时间"
question_id: "2534"
question: "通过门的时间"
problem_url: "https://leetcode.cn/problems/time-taken-to-cross-the-door/"
created: "2023-06-15T01:16:25+08:00"
updated: "2023-06-15T01:16:25+08:00"
upvotes: 0
comments: 0
---

# 2534. 通过门的时间

> **[yiduobo的每日leetcode 2534.通过门的时间](https://zhuanlan.zhihu.com/p/637171523) · 知乎 · 2023-06-15 · 赞同 0**
> 力扣：[2534. 通过门的时间](https://leetcode.cn/problems/time-taken-to-cross-the-door/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2534.通过门的时间

[力扣](https://leetcode.cn/problems/time-taken-to-cross-the-door/)

又是带优先级的时序模拟问题，不过本题只有两个等待队列waiting_in和waiting_out。另外，本题中每个人只会进出队列一次，而每个人的到达时间都不超过n，因此在最坏情况下排队时间不会超过2n，因此可以直接暴力遍历时间点now而不需要去计算选取。

另外，这里的优先级也与上一秒的选择有关，因此需要使用一个变量pre记录上一秒门的使用情况。

对于当前时间点now，先将在now时刻到来的人根据其state值加入到对应的队列中，然后根据pre以及两个队列中是否有人在等待来决定在当前时刻使用门的人的下标index，并根据index以及使用门的方式更新答案以及pre。若当前时刻没有人使用门，那么就更新pre为None，同时不更新答案。最后，将now加上1，然后重复此过程直到所有人都已到达，且两个队列都为空，也就是所有人都已经安排好了门为止。

最后附上python代码：

```python
class Solution(object):
    def timeTaken(self, arrival, state):
        """
        :type arrival: List[int]
        :type state: List[int]
        :rtype: List[int]
        """

        waiting_in = []
        waiting_out = []
        pre = None
        now = 0
        p = 0
        n = len(arrival)

        res = [0] * n
        while p < n or waiting_in or waiting_out:
            while p < n and arrival[p] == now:
                if state[p] == 0:
                    heapq.heappush(waiting_in, p)
                else:
                    heapq.heappush(waiting_out, p)
                p += 1
            
            if waiting_in:
                if waiting_out:
                    if pre == 0:
                        index = heapq.heappop(waiting_in)
                    else:
                        index = heapq.heappop(waiting_out)
                else:
                    index = heapq.heappop(waiting_in)
                    pre = 0

            elif waiting_out:
                index = heapq.heappop(waiting_out)
                pre = 1

            else:
                index = None
                pre = None

            if index is not None:
                res[index] = now
            
            now += 1
        
        return res
```
