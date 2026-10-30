---
title: "2497. 图中最大星和"
aliases: ["yiduobo的每日leetcode 2497.图中最大星和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633499097"
zhihu_id: "633499097"
zhihu_title: "yiduobo的每日leetcode 2497.图中最大星和"
question_id: "2497"
question: "图中最大星和"
problem_url: "https://leetcode.cn/problems/maximum-star-sum-of-a-graph/"
difficulty: "Medium"
created: "2023-05-31T01:49:34+08:00"
updated: "2023-05-31T01:49:34+08:00"
upvotes: 0
comments: 0
---

# 2497. 图中最大星和

> **[yiduobo的每日leetcode 2497.图中最大星和](https://zhuanlan.zhihu.com/p/633499097) · 知乎 · 2023-05-31 · 赞同 0**
> 力扣：[2497. 图中最大星和](https://leetcode.cn/problems/maximum-star-sum-of-a-graph/) · Medium · 灵茶山艾府：[枚举+排序](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2497.图中最大星和

[力扣](https://leetcode.cn/problems/maximum-star-sum-of-a-graph/)

题目描述得稍显复杂，但是本质上题目就是给出了一个n行的二维数组，每一行中的数字则由与当前行号对应节点相邻的所有节点值组成。题目要求对于每一行选出不超过k个数字，然后找出其中选出的数字之和与行号对应节点的数值之和的最大值。

对于这个问题，一种可行的处理方法是遍历每行，对于每行使用一个大小为k的堆来选择最大的k个数。当然也不一定需要k个，例如负数就不应该被选择。

具体实现上，也无需将这个二维数组构造出来，只需完整地遍历图中的所有边，就相当于遍历了整个二维数组。

最后附上python代码：

```python
class Solution(object):
    def maxStarSum(self, vals, edges, k):
        """
        :type vals: List[int]
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """

        n = len(vals)
        heap_list = [[] for _ in range(n)]
        s = vals[:]

        for x, y in edges:
            if vals[y] > 0:
                s[x] += vals[y]
                heapq.heappush(heap_list[x], vals[y])
                if len(heap_list[x]) > k:
                    s[x] -= heap_list[x][0]
                    heapq.heappop(heap_list[x])
            
            if vals[x] > 0:
                s[y] += vals[x]
                heapq.heappush(heap_list[y], vals[x])
                if len(heap_list[y]) > k:
                    s[y] -= heap_list[y][0]
                    heapq.heappop(heap_list[y])
        
        return max(s)
```
