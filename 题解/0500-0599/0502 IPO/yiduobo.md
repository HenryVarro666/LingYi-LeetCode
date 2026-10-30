---
title: "502. IPO"
aliases: ["yiduobo的每日leetcode 502.IPO"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258609628"
zhihu_id: "258609628"
zhihu_title: "yiduobo的每日leetcode 502.IPO"
question_id: "502"
question: "IPO"
problem_url: "https://leetcode.cn/problems/ipo/"
created: "2020-09-23T22:44:48+08:00"
updated: "2020-09-23T22:44:48+08:00"
upvotes: 1
comments: 0
---

# 502. IPO

> **[yiduobo的每日leetcode 502.IPO](https://zhuanlan.zhihu.com/p/258609628) · 知乎 · 2020-09-23 · 赞同 1**
> 力扣：[502. IPO](https://leetcode.cn/problems/ipo/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

502.IPO <https://leetcode-cn.com/problems/ipo/>

按照题目的描述，我们每次都应当选择当前能选择项目中净利润最大的那个。而随着项目的进行，我们手中的启动资金必然是单调递增的，即后续可以启动的项目也会越来越多。于是一个自然的想法就是将项目按启动资金从小到大排序，那么每次可选择的项目必然是这个数组的前缀，而我们需要从中选出收益最大的那一个，更新收益之后扩展这个前缀然后重复上面的操作。那么现在就有将某些数加入候选集，以及维护候选集中最大数这两种需求，那么使用堆来维护这个候选集是一个可行的方案。

于是现在整个流程就是：

1、将所有项目按启动资金从小到大进行排序，并将当前能够启动的项目加入到堆中。堆中维护的是当前可执行项目的最大收益

2、选择堆中收益最大的项目并执行，此时启动资金会得到增长。根据新的启动资金将目前可以启动的项目加入堆中

3、重复步骤2直到k为0或者无法再启动项目

最后附上python代码：

```
class Solution(object):
    def findMaximizedCapital(self, k, W, Profits, Capital):
        """
        :type k: int
        :type W: int
        :type Profits: List[int]
        :type Capital: List[int]
        :rtype: int
        """

        value_list = []
        for index in range(len(Profits)):
            value_list.append([Profits[index], Capital[index]])

        value_list = sorted(value_list, key=lambda d:d[1])

        heap = []
        pos = 0
        for index in range(k):
            while pos < len(value_list) and W >= value_list[pos][1]:
                heapq.heappush(heap, -value_list[pos][0])
                pos += 1
            if not heap:
                break
            W -= heapq.heappop(heap)
        
        return W
```
