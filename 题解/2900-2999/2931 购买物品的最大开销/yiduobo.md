---
title: "2931. 购买物品的最大开销"
aliases: ["yiduobo的每日leetcode 2931.购买物品的最大开销"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690474578"
zhihu_id: "690474578"
zhihu_title: "yiduobo的每日leetcode 2931.购买物品的最大开销"
question_id: "2931"
question: "购买物品的最大开销"
problem_url: "https://leetcode.cn/problems/maximum-spending-after-buying-items/"
difficulty: "Hard"
rating: 1822
created: "2024-04-03T02:13:02+08:00"
updated: "2024-04-03T02:13:02+08:00"
upvotes: 1
comments: 0
---

# 2931. 购买物品的最大开销

> **[yiduobo的每日leetcode 2931.购买物品的最大开销](https://zhuanlan.zhihu.com/p/690474578) · 知乎 · 2024-04-03 · 赞同 1**
> 力扣：[2931. 购买物品的最大开销](https://leetcode.cn/problems/maximum-spending-after-buying-items/) · Hard · 灵茶山艾府：[两种方法：排序/最小堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2931.购买物品的最大开销

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-spending-after-buying-items/description/)

为了使得开销最大，那么很直观的想法就是先买便宜的再买贵的。由于各商店的物品都已经排好序了，当前剩下的货物中最便宜的一定是所有商店最右侧商品中的某一个，也就是说一定可以在第k轮买到第k便宜的物品。问题到了这里就转化成了k路归并问题，可以使用堆来进行处理。

具体的思路可以参考之前的23题

[yiduobo：yiduobo的每日leetcode 23.合并K个排序链表](https://zhuanlan.zhihu.com/p/116101679)

最后附上python代码：

```python
class Solution(object):
    def maxSpending(self, values):
        """
        :type values: List[List[int]]
        :rtype: int
        """

        heap = []
        m = len(values)
        n = len(values[0])
        for i in range(m):
            heapq.heappush(heap, [values[i][n - 1], i, n - 1])
        
        res = 0
        for i in range(m * n):
            v, x, y = heapq.heappop(heap)
            res += v * (i + 1)
            if y > 0:
                heapq.heappush(heap, [values[x][y - 1], x, y - 1])
        
        return res
```
