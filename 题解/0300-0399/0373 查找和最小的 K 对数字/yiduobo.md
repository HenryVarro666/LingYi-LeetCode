---
title: "373. 查找和最小的K对数字"
aliases: ["yiduobo的每日leetcode 373.查找和最小的K对数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap-priority-queue", "题单/二分算法", "题单/常用数据结构", "题单/面试经典-150-题", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列", "题单/面试经典-150-题/堆"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165394469"
zhihu_id: "165394469"
zhihu_title: "yiduobo的每日leetcode 373.查找和最小的K对数字"
question_id: "373"
question: "查找和最小的 K 对数字"
problem_url: "https://leetcode.cn/problems/find-k-pairs-with-smallest-sums/"
difficulty: "Medium"
created: "2020-07-30T21:25:53+08:00"
updated: "2020-07-30T21:25:53+08:00"
upvotes: 0
comments: 0
---

# 373. 查找和最小的K对数字

> **[yiduobo的每日leetcode 373.查找和最小的K对数字](https://zhuanlan.zhihu.com/p/165394469) · 知乎 · 2020-07-30 · 赞同 0**
> 力扣：[373. 查找和最小的 K 对数字](https://leetcode.cn/problems/find-k-pairs-with-smallest-sums/) · Medium · 灵茶山艾府：[讲清楚为什么一开始要把 (i,0) 都入堆！两种理解角度（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

373.查找和最小的K对数字<https://leetcode-cn.com/problems/find-k-pairs-with-smallest-sums/>

对于nums1和nums2，设其长度分别为m和n，那么一共可以形成m \* n的加和。将这些加和按下标排列好，可以形成一个m \* n的矩阵，那么就可以视为m个长度为n的单调递增数组，找出其中最小的k个数。当然也可以视为n个长度为m的单调递增数组，找出其中最小的k个数。

到了这里就转化为了一个m路归并或者n路归并问题，使用二叉堆就可以很快解决，最终的时间复杂度为O(klog(min(m, n)))。

需要注意的是，这里显然不能直接先计算这个m \* n的矩阵，因为这样一来时间复杂度直接就到O(m \* n)了，而是需要边算边做。

最后附上python代码：

```python
import heapq

class Solution(object):
    def kSmallestPairs(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[List[int]]
        """

        swap_flag = False
        if len(nums1) > len(nums2):
            tmp1 = nums2
            tmp2 = nums1
            swap_flag = True
        else:
            tmp1 = nums1
            tmp2 = nums2

        pos_list = [0] * len(tmp1)
        heap = [[x + tmp2[0], index] for index, x in enumerate(tmp1)]
        heapq.heapify(heap)

        res = []
        while k > 0 and heap:
            val, index = heapq.heappop(heap)
            if swap_flag:
                res.append([tmp2[pos_list[index]], tmp1[index]])
            else:
                res.append([tmp1[index], tmp2[pos_list[index]]])
            pos_list[index] += 1
            if pos_list[index] < len(tmp2):
                heapq.heappush(heap, [tmp1[index] + tmp2[pos_list[index]], index])
            k -= 1
            
        return res
```
