---
title: "2940. 找到Alice和Bob可以相遇的建筑"
aliases: ["yiduobo的每日leetcode 2940.找到Alice和Bob可以相遇的建筑"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/segment-tree", "leetcode/binary-search", "leetcode/monotonic-stack", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/八-树状数组和线段树", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691192998"
zhihu_id: "691192998"
zhihu_title: "yiduobo的每日leetcode 2940.找到Alice和Bob可以相遇的建筑"
question_id: "2940"
question: "找到 Alice 和 Bob 可以相遇的建筑"
problem_url: "https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/"
difficulty: "Hard"
rating: 2327
created: "2024-04-08T00:48:16+08:00"
updated: "2024-04-08T00:48:16+08:00"
upvotes: 1
comments: 0
---

# 2940. 找到Alice和Bob可以相遇的建筑

> **[yiduobo的每日leetcode 2940.找到Alice和Bob可以相遇的建筑](https://zhuanlan.zhihu.com/p/691192998) · 知乎 · 2024-04-08 · 赞同 1**
> 力扣：[2940. 找到 Alice 和 Bob 可以相遇的建筑](https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/) · Hard · 灵茶山艾府：[三种方法：离线+最小堆 / 离线+单调栈二分 / 在线+线段树二分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2940.找到Alice和Bob可以相遇的建筑

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/)

首先，题目中的Alice和Bob是等价的，因此在这里方便起见，当询问中的a > b时，可以将二者交换，保证总是有a \< b。

接下来处理特殊情况。若a \= b或者heights[a] \< heights[b]，两人可以在b相遇，因此答案就是b。

而对于一般情况，则需要在区间[b + 1, n - 1]之间寻找一个最小的下标t，满足heights[t] > max(heights[a], heights[b])。这是一个后缀区间询问问题，需要要寻找的是满足条件的最小坐标，因此需要用到线段树。

具体来说，使用线段树维护区间的最大值ma，那么对于上面寻找t的问题，则依然是自顶向下进行查找。对于当前查找的区间[left, right]：

1、若区间的最大值小于等于max(heights[a], heights[b])，那么说明区间中的所有值不达标，因此无解

2、否则的话若区间左右边界相等，那么说明当前区间对应的值，即heights[left]是大于max(heights[a], heights[b])的，因此答案就是left

3、计算区间终点mid。若b + 1小于等于mid，那么就可以在左半区间中去寻找答案，此时应该递归求解左半区间。若有解，那么直接返回，否则就需要再递归求解右半区间并返回求解的结果。

关于线段树的简单介绍可以参考之前的699题：

[yiduobo：yiduobo的每日leetcode 699.掉落的方块](https://zhuanlan.zhihu.com/p/316523832)

最后附上python代码：

```python
class Solution(object):
    def leftmostBuildingQueries(self, heights, queries):
        """
        :type heights: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(heights)
        ma = [0] * (n * 4)

        def build(now, left, right):
            if left == right:
                ma[now] = heights[left]
                return

            mid = (left + right) // 2
            build(now + now + 1, left, mid)
            build(now + now + 2, mid + 1, right)
            ma[now] = max(ma[now + now + 1], ma[now + now + 2])
        
        def query(now, left, right, p, v):
            if ma[now] <= v:
                return -1
            
            if left == right:
                return left
            
            mid = (left + right) // 2
            if p <= mid:
                t = query(now + now + 1, left, mid, p, v)
                if t != -1:
                    return t

            return query(now + now + 2, mid + 1, right, p, v)
        

        build(0, 0, n - 1)
        res = []
        for a, b in queries:
            if a > b:
                a, b = b, a
            
            if a == b or heights[a] < heights[b]:
                res.append(b)
            elif b == n - 1:
                res.append(-1)
            else:
                res.append(query(0, 0, n - 1, b + 1, max(heights[a], heights[b])))
        
        return res
```
