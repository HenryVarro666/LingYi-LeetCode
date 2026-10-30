---
title: "2542. 最大子序列的分数"
aliases: ["yiduobo的每日leetcode 2542.最大子序列的分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637862769"
zhihu_id: "637862769"
zhihu_title: "yiduobo的每日leetcode 2542.最大子序列的分数"
question_id: "2542"
question: "最大子序列的分数"
problem_url: "https://leetcode.cn/problems/maximum-subsequence-score/"
difficulty: "Medium"
rating: 2056
created: "2023-06-19T22:33:44+08:00"
updated: "2023-06-19T22:33:44+08:00"
upvotes: 0
comments: 0
---

# 2542. 最大子序列的分数

> **[yiduobo的每日leetcode 2542.最大子序列的分数](https://zhuanlan.zhihu.com/p/637862769) · 知乎 · 2023-06-19 · 赞同 0**
> 力扣：[2542. 最大子序列的分数](https://leetcode.cn/problems/maximum-subsequence-score/) · Medium · 灵茶山艾府：[转换问题+最小堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2542.最大子序列的分数

[力扣](https://leetcode.cn/problems/maximum-subsequence-score/)

题目中的分数计算公式由两个部分组成，对于其中加法的部分，是一个从nums1的某个子集中取top k的问题。这子集不是静态的，因此为了求解这个问题，就必须保证这个子集包含了上一轮的子集，这样的话就可以利用一个大小为k的小顶堆不断迭代求解这个top k问题。

另一方面，计算公式乘号右侧取最小值的部分，则恰好决定了加法部分的候选集。

为了使得候选集稳定扩展，一个可行的处理方法就是将nums2中的数从大到小进行排序，然后一趟遍历逐个选取作为最小值的部分中的最小值。设当前遍历到的是nums2[index]，那么其对应的加法部分的候选集就相当于在上一轮候选集的基础上额外添加了nums1[index]，此时只需使用堆来维护此时候选集中的top k并计算这些数之和，乘以nums2[index]后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """

        heap = []
        res = 0
        s = 0
        for x, y in sorted(zip(nums1, nums2), key=lambda d:d[1], reverse=True):
            heapq.heappush(heap, x)
            s += x
            if len(heap) > k:
                s -= heap[0]
                heapq.heappop(heap)
            
            if len(heap) == k:
                res = max(res, y * s)
        
        return res
```
