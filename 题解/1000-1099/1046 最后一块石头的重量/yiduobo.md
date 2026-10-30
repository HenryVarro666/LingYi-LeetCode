---
title: "1046. 最后一块石头的重量"
aliases: ["yiduobo的每日leetcode 1046.最后一块石头的重量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371235499"
zhihu_id: "371235499"
zhihu_title: "yiduobo的每日leetcode 1046.最后一块石头的重量"
question_id: "1046"
question: "最后一块石头的重量"
problem_url: "https://leetcode.cn/problems/last-stone-weight/"
created: "2021-05-10T21:47:05+08:00"
updated: "2021-05-10T21:47:05+08:00"
upvotes: 0
comments: 0
---

# 1046. 最后一块石头的重量

> **[yiduobo的每日leetcode 1046.最后一块石头的重量](https://zhuanlan.zhihu.com/p/371235499) · 知乎 · 2021-05-10 · 赞同 0**
> 力扣：[1046. 最后一块石头的重量](https://leetcode.cn/problems/last-stone-weight/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1046.最后一块石头的重量

[力扣](https://leetcode-cn.com/problems/last-stone-weight/)

由于这里石头的个数非常少，所以想怎么做都可以。我在这里采用的是堆来模拟这个过程，每次从堆中取出最重的两块石头，计算二者之差。若这个差不为0，则将这个差重新加入到堆中。重复这个过程直到堆的大小小于2。

最后附上python代码：

```python
class Solution(object):
    def lastStoneWeight(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """

        heap = [-x for x in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            num1 = -heapq.heappop(heap)
            num2 = -heapq.heappop(heap)
            num1 -= num2
            if num1 > 0:
                heapq.heappush(heap, -num1)
        
        if not heap:
            return 0
        return -heap[0]
```
