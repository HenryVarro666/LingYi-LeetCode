---
title: "3275. 第K近障碍物查询"
aliases: ["yiduobo的每日leetcode 3275.第K近障碍物查询"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794186080"
zhihu_id: "794186080"
zhihu_title: "yiduobo的每日leetcode 3275.第K近障碍物查询"
question_id: "3275"
question: "第 K 近障碍物查询"
problem_url: "https://leetcode.cn/problems/k-th-nearest-obstacle-queries/"
difficulty: "Medium"
rating: 1420
created: "2024-10-03T02:11:09+08:00"
updated: "2024-10-03T02:11:09+08:00"
upvotes: 0
comments: 0
---

# 3275. 第K近障碍物查询

> **[yiduobo的每日leetcode 3275.第K近障碍物查询](https://zhuanlan.zhihu.com/p/794186080) · 知乎 · 2024-10-03 · 赞同 0**
> 力扣：[3275. 第 K 近障碍物查询](https://leetcode.cn/problems/k-th-nearest-obstacle-queries/) · Medium · 灵茶山艾府：[最大堆维护前 k 小（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3275.第K近障碍物查询

[. - 力扣（LeetCode）](https://leetcode.cn/problems/k-th-nearest-obstacle-queries/description/)

题目给出一个无限大的二维平面，然后给出一个正整数k以及一个二维询问数组queries，其中queries\[i\] \= \[x\[i\], y\[i\]\]，表示在平面上(x\[i\], y\[i\])这个位置设置一个障碍物，问每次询问后平面上距离原地第k近的障碍物的距离。这里的距离按照曼哈顿距离计算，同时每个询问的坐标不同，若坐标不足k个则返回-1。

静态的求第k小的数之前遇到过，可以使用排序、堆或者快速选择算法，而本题则是动态的求第k小的问题，依然可以使用堆来处理。

维护一个大小为k的大顶堆，对于每个询问，计算出对应的距离后，将距离加入到堆中。若堆的大小超过k，则弹出堆顶元素。接下来若堆中元素不足k个，则当前询问对应的答案为-1，否则对应的答案就是堆顶元素。

由于python中默认的堆是小顶的，在这里可以使用为来维护距离的相反数，就相当于维护了大顶堆。

最后附上python代码：

```python
class Solution(object):
    def resultsArray(self, queries, k):
        """
        :type queries: List[List[int]]
        :type k: int
        :rtype: List[int]
        """

        heap = []
        res = []
        for x, y in queries:
            d = abs(x) + abs(y)
            heapq.heappush(heap, -d)

            if len(heap) < k:
                res.append(-1)
            else:
                if len(heap) > k:
                    heapq.heappop(heap)
                res.append(-heap[0])
        
        return res
```
