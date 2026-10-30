---
title: "3478. 选出和最大的K个元素"
aliases: ["yiduobo的每日leetcode 3478.选出和最大的K个元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897265781231837240"
zhihu_id: "1897265781231837240"
zhihu_title: "yiduobo的每日leetcode 3478.选出和最大的K个元素"
question_id: "3478"
question: "选出和最大的 K 个元素"
problem_url: "https://leetcode.cn/problems/choose-k-elements-with-maximum-sum/"
difficulty: "Medium"
rating: 1753
created: "2025-04-20T12:48:20+08:00"
updated: "2025-04-20T12:48:20+08:00"
upvotes: 1
comments: 0
---

# 3478. 选出和最大的K个元素

> **[yiduobo的每日leetcode 3478.选出和最大的K个元素](https://zhuanlan.zhihu.com/p/1897265781231837240) · 知乎 · 2025-04-20 · 赞同 1**
> 力扣：[3478. 选出和最大的 K 个元素](https://leetcode.cn/problems/choose-k-elements-with-maximum-sum/) · Medium · 灵茶山艾府：[最小堆维护前 k 大（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3478.选出和最大的K个元素

[3478. 选出和最大的 K 个元素 - 力扣（LeetCode）](https://leetcode.cn/problems/choose-k-elements-with-maximum-sum/description/)

题目给出两个整数数组nums1以及nums2，这两个数组的长度均为n。另外给出一个正整数k。

接下来对0到n - 1之间的每个下标index，需要先找出所有nums1中所有小于nums1[index]的元素的下标，然后从这些下标在nums2中对应的元素中选出最大的k个，将这些元素之和作为当前下标index在结果数组res中对应的结果。

由于nums1中的元素是固定的，因此对于找出所有小于nums1中特定元素的所有下标这一问题，可以先将nums1中的元素以及对应的下标做成二元组数组info，然后对info按元素值从小到大进行排序。这样一来对于info[p] \= (v, index)而言，info[0]到info[p - 1]之间的二元组对应的元素都小于等于v，从中剔除掉值等于v的二元组后，问题就转化成了前缀的top k问题，接下来使用一个大小为k的小顶堆就能计算每个下标对应的答案了。

最后附上python代码：

```python
class Solution(object):
    def findMaxSum(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        n = len(nums1)
        res = [0] * n
        heap = []
        s = 0

        info = sorted(enumerate(nums1), key=lambda d:d[1])
        p = 0
        while p < len(info):
            q = p
            while q < len(info) and info[p][1] == info[q][1]:
                res[info[q][0]] = s
                q += 1

            for index in range(p, q):
                heapq.heappush(heap, nums2[info[index][0]])
                s += nums2[info[index][0]]
                if len(heap) > k:
                    s -= heapq.heappop(heap)

            p = q
        
        return res
```
