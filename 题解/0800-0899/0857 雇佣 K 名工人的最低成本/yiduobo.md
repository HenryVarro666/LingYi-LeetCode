---
title: "857. 雇佣K名工人的最低成本"
aliases: ["yiduobo的每日leetcode 857.雇佣K名工人的最低成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348911974"
zhihu_id: "348911974"
zhihu_title: "yiduobo的每日leetcode 857.雇佣K名工人的最低成本"
question_id: "857"
question: "雇佣 K 名工人的最低成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-hire-k-workers/"
difficulty: "Hard"
rating: 2260
created: "2021-02-05T23:57:04+08:00"
updated: "2021-02-05T23:57:04+08:00"
upvotes: 0
comments: 0
---

# 857. 雇佣K名工人的最低成本

> **[yiduobo的每日leetcode 857.雇佣K名工人的最低成本](https://zhuanlan.zhihu.com/p/348911974) · 知乎 · 2021-02-05 · 赞同 0**
> 力扣：[857. 雇佣 K 名工人的最低成本](https://leetcode.cn/problems/minimum-cost-to-hire-k-workers/) · Hard · 灵茶山艾府：[一步步提示如何思考此题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

857.雇佣K名工人的最低成本

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-hire-k-workers/)

不愧是万恶的资本主义国家的题库，这题目描述的屁股都是歪的。。。

仔细分析题目给出的工资标准，可以发现对于一组工人来说，如果想要让每个人都拿到期望的最低工资，那么就需要将单位工作质量价格最高的工人作为工资标准，给其他工人进行对应的换算。换一个角度来说，就是

max(w_per_q) \* sumq

一个自然的想法就是按照w_per_q从小到大进行排序，那么对于第index位工人，从0到index这些工人的工资标准都需要按照w_pre_q[index]来进行计算，而当这里的index大于等于K时，我们则需要从中选出q最小的K位工人来保证sumq最小。于是这里就出现了一个topK的问题，可以使用堆来解决。

于是现在就有了一种做法，首先将所有工人按照w/q从小到大进行排序，接下来从头开始遍历所有工人，设当前遍历到第index位工人：

1、将sumq加上q[index]

2、若当前堆的大小为K，那么在加上当前这位工人之后超过了K为工人，因此需要从堆中弹出一个q最大的工人，同时sumq减去该工人的q。

3、若当前index大于等于k - 1，说明已经可以选出足够的工人，那么使用w[index] / q[index] \* sumq来更新答案。

4、最后将当前工人的q加入到堆中

最后附上python代码。由于python的堆默认为小根堆，因此这里采用取相反数的方法来填充这个堆：

```python
class Solution(object):
    def mincostToHireWorkers(self, quality, wage, K):
        """
        :type quality: List[int]
        :type wage: List[int]
        :type K: int
        :rtype: float
        """

        heap = []
        sum_q = 0
        res = None
        for index, (q, w) in enumerate(sorted(zip(quality, wage), key=lambda d:d[1]* 1.0 / d[0])):
            sum_q += q
            if len(heap) == K:
                sum_q += heapq.heappop(heap)
            if index >= K - 1 and res is None or res > w * 1.0 / q * sum_q:
                res = w * 1.0 / q * sum_q
            heapq.heappush(heap, -q)
        
        return res
```
