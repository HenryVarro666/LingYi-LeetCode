---
title: "1383. 最大的团队表现值"
aliases: ["yiduobo的每日leetcode 1383.最大的团队表现值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402379502"
zhihu_id: "402379502"
zhihu_title: "yiduobo的每日leetcode 1383.最大的团队表现值"
question_id: "1383"
question: "最大的团队表现值"
problem_url: "https://leetcode.cn/problems/maximum-performance-of-a-team/"
created: "2021-08-22T17:21:27+08:00"
updated: "2021-08-22T17:21:27+08:00"
upvotes: 0
comments: 0
---

# 1383. 最大的团队表现值

> **[yiduobo的每日leetcode 1383.最大的团队表现值](https://zhuanlan.zhihu.com/p/402379502) · 知乎 · 2021-08-22 · 赞同 0**
> 力扣：[1383. 最大的团队表现值](https://leetcode.cn/problems/maximum-performance-of-a-team/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1383.最大的团队表现值

<https://leetcode-cn.com/problems/maximum-performance-of-a-team/>

之前好像遇到过一道相同的题目，但是记不清楚题号了。

最终答案是由所有人的速度和乘上效率的最小值得到了，那么我们可以按效率划一个阈值，对于效率在阈值之上人，我们显然应该选择速度最大的k个，于是就得到了一种做法：

想将左右人按效率值从大到小进行排序，然后从从头向后一趟扫描，对于当前员工，我们将新的效率阈值设定为当前员工的效率值，那么之前员工的效率值必然都是大于等于阈值的，因此相当于对于之前员工中选出的k个速度最大的员工中，新加入当前员工的速度值，然后再从中选出新的k个速度最大的员工。

对于这个top k问题，我们就可以维护一个大小为k的堆，每次对比堆顶员工的的速度与当前新加入员工的速度，去除掉较小的那个员工即可。

最后附上python代码：

```python
class Solution(object):
    def maxPerformance(self, n, speed, efficiency, k):
        """
        :type n: int
        :type speed: List[int]
        :type efficiency: List[int]
        :type k: int
        :rtype: int
        """
        
        heap = []
        now = 0
        res = 0
        mod = 10 ** 9 + 7
        for s, e in sorted(zip(speed, efficiency), key=lambda d:-d[1]):
            heapq.heappush(heap, s)
            now += s
            if len(heap) > k:
                now -= heap[0]
                heapq.heappop(heap)
                
            
            res = max(res, e * now)
        
        return res % mod
```
