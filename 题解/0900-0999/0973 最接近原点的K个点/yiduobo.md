---
title: "973. 最接近原点的K个点"
aliases: ["yiduobo的每日leetcode 973.最接近原点的K个点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362293767"
zhihu_id: "362293767"
zhihu_title: "yiduobo的每日leetcode 973.最接近原点的K个点"
question_id: "973"
question: "最接近原点的K个点"
problem_url: "https://leetcode.cn/problems/k-closest-points-to-origin/"
created: "2021-04-04T21:55:43+08:00"
updated: "2021-04-04T21:55:43+08:00"
upvotes: 0
comments: 0
---

# 973. 最接近原点的K个点

> **[yiduobo的每日leetcode 973.最接近原点的K个点](https://zhuanlan.zhihu.com/p/362293767) · 知乎 · 2021-04-04 · 赞同 0**
> 力扣：[973. 最接近原点的K个点](https://leetcode.cn/problems/k-closest-points-to-origin/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

973.最接近原点的K个点

[力扣](https://leetcode-cn.com/problems/k-closest-points-to-origin/)

首先计算每个点到原点的距离，然后题目就变成了top k问题，使用快排取top k或者维护大小为k的二叉堆都是可行的做法。不过注意到这里的top k并不需要top k也有序，因此可以使用快排中使用的快速选择法。具体来说就是对于l到r这一段区间，我们随机选择其中一个数作为基准mid，然后将小于mid的数放在区间的头部，将大于mid的数放在区间的尾部，接下来只需要判断小于mid的数的个数以及大于mid的数的个数与k的大小关系，然后决定下一步是否需要递归求解，以及在哪个子区间内递归求解即可。

最后附上python代码，这里的实现与题解有细微差别，主要是关于等于mid的数的位置。这里是l到j中的数满足小于等于mid，而i到r中的数满足大于等于mid，因此最终检测区间长度时需要特别注意：

```python
class Solution(object):
    def kClosest(self, points, k):
        """
        :type points: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """

        dis = [[x * x + y * y, index] for index, (x, y) in enumerate(points)]
        
        self.qsort(dis, 0, len(dis) - 1, k)
        #print dis
        return [points[index] for _, index in dis[:k]]
    
    def qsort(self, dis, l, r, k):
        mid = dis[(l + r) / 2][0]
        i, j = l, r
        while i < j:
            while dis[i][0] < mid:
                i += 1
            while dis[j][0] > mid:
                j -= 1
            if i <= j:
                dis[i], dis[j] = dis[j], dis[i]
                i += 1
                j -= 1

        if j - l + 1 > k:
            self.qsort(dis, l, j, k)
        elif i - l < k and i < r:
            self.qsort(dis, i, r, k - (i - l))
```
