---
title: "2070. 每一个查询的最大美丽值"
aliases: ["yiduobo的每日leetcode 2070.每一个查询的最大美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/sorting", "leetcode/monotonic-stack", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/一-二分查找", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/515917751"
zhihu_id: "515917751"
zhihu_title: "yiduobo的每日leetcode 2070.每一个查询的最大美丽值"
question_id: "2070"
question: "每一个查询的最大美丽值"
problem_url: "https://leetcode.cn/problems/most-beautiful-item-for-each-query/"
difficulty: "Medium"
rating: 1724
created: "2022-05-17T21:25:32+08:00"
updated: "2022-05-17T21:25:32+08:00"
upvotes: 0
comments: 0
---

# 2070. 每一个查询的最大美丽值

> **[yiduobo的每日leetcode 2070.每一个查询的最大美丽值](https://zhuanlan.zhihu.com/p/515917751) · 知乎 · 2022-05-17 · 赞同 0**
> 力扣：[2070. 每一个查询的最大美丽值](https://leetcode.cn/problems/most-beautiful-item-for-each-query/) · Medium · 灵茶山艾府：[两种方法：离线双指针/在线二分（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2070.每一个查询的最大美丽值

[力扣](https://leetcode.cn/problems/most-beautiful-item-for-each-query/)

题目乍一看是一个典型的区间最值问题，但是如果采用离线做法的话，就可以排序后利用单调性来解决了。

首先将物品按价格从小到大排序，同时也将询问从小到大排序。接下来遍历排好序的询问，并使用一个变量p记录排序后的物品中能满足当前询问的物品的最大下标。

随着遍历的进行，询问的阈值是在逐渐增大的，由于物品也是按价格排好序的，因此能满足当前询问的物品的最大下标也是单调不减的，于是可以在均摊O(1)的时间内找出所有询问对应的p，同时可以利用上一个询问的结果以及当前询问新加入的满足条件的物品美丽值来更新当前询问的结果。

最后附上python代码：

```python
class Solution(object):
    def maximumBeauty(self, items, queries):
        """
        :type items: List[List[int]]
        :type queries: List[int]
        :rtype: List[int]
        """

        sorted_items = sorted(items, key=lambda d:d[0])
        sorted_queries = sorted([[q, index] for index, q in enumerate(queries)])
        res = [0] * len(sorted_queries)
        p = 0
        now = 0
        for q, index in sorted_queries:
            while p < len(sorted_items) and sorted_items[p][0] <= q:
                now = max(now, sorted_items[p][1])
                p += 1
            
            res[index] = now
        
        return res
```
