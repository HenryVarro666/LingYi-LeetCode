---
title: "3763. Maximum Total Sum With Threshold Constraints"
aliases: ["yiduobo的每日leetcode 3763.Maximum Total Sum With Threshold Constraints"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981111096430589893"
zhihu_id: "1981111096430589893"
zhihu_title: "yiduobo的每日leetcode 3763.Maximum Total Sum With Threshold Constraints"
question_id: "3763"
question: "Maximum Total Sum With Threshold Constraints"
problem_url: "https://leetcode.cn/problems/maximum-total-sum-with-threshold-constraints/"
created: "2025-12-07T21:35:33+08:00"
updated: "2025-12-07T21:35:34+08:00"
upvotes: 0
comments: 0
---

# 3763. Maximum Total Sum With Threshold Constraints

> **[yiduobo的每日leetcode 3763.Maximum Total Sum With Threshold Constraints](https://zhuanlan.zhihu.com/p/1981111096430589893) · 知乎 · 2025-12-07 · 赞同 0**
> 力扣：[3763. Maximum Total Sum With Threshold Constraints](https://leetcode.cn/problems/maximum-total-sum-with-threshold-constraints/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3763.Maximum Total Sum With Threshold Constraints

[3763. Maximum Total Sum with Threshold Constraints - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-sum-with-threshold-constraints/description/)

题目给出两个长度为n的整数数组nums以及threshold。

接下来从step\=1开始执行以下操作：

- 选择一个之前没选过的下标index，满足threshold[index] \<\= step
- 将nums[index]累加到答案中
- 将step加上1

重复以上过程直到无法选出可用的index为止。

问可能得到的最大答案是多少。

根据题目的要求，每一轮选择的index都需要满足threshold[index]小于等于当前的step，而step是准备增大的，也就是说每一轮的候选下标，都相当于在上一轮选择后剩余的候选下标的基础上，额外添加所有threshold恰好等于step的下标，而为了使得最终答案最大，每一轮都应该选择候选下标种对应的nums最大的那一个。

基于上面的思路，相当于需要完成两个操作：

1、随着step的增大，将threshold恰好等于step的下标选出来并加入到候选下标中

2、从候选下标中选出一个对应的nums最大的下标

其中第二点是动态的最大值问题，使用一个堆就可以很方便的处理。而对于第一点，则可以先对threshold排序，利用单调性来处理。

具体来说，先将nums和threshold合并得到info，然后将info按照threshold从小到大进行排序。

接下来从1开始往上遍历step，使用一个堆记录当前可用的候选下标对应的nums值，同时使用一个变量p记录info中满足info[p]的threshold大于当前step的最小的p。

对于当前的step，就可以对比当前的info[p]的threshold以及step的大小，若二者相同，则将info[p]对应的nums加入到堆中，然后将p向后移动，直到p来到info的末尾，或者info[p]对应的threshold大于step为止。

接下来，若堆为空，说明当前的step无法选择，可以直接返回当前答案，反之，则从堆中取出最大值，累加到答案中然后继续考虑下一个step即可。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: List[int]
        :rtype: int
        """
        
        info = sorted(zip(threshold, nums))
        heap = []
        
        res = 0
        p = 0
        for step in range(1, len(nums) + 1):
            while p < len(info) and info[p][0] == step:
                heapq.heappush(heap, -info[p][1])
                p += 1
            
            if not heap:
                break
            else:
                res -= heapq.heappop(heap)
        
        return res
```
