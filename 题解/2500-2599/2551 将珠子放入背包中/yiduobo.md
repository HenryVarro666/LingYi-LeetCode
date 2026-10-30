---
title: "2551. 将珠子放入背包中"
aliases: ["yiduobo的每日leetcode 2551.将珠子放入背包中"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638954142"
zhihu_id: "638954142"
zhihu_title: "yiduobo的每日leetcode 2551.将珠子放入背包中"
question_id: "2551"
question: "将珠子放入背包中"
problem_url: "https://leetcode.cn/problems/put-marbles-in-bags/"
difficulty: "Hard"
rating: 2042
created: "2023-06-25T01:24:43+08:00"
updated: "2023-06-25T01:24:43+08:00"
upvotes: 1
comments: 0
---

# 2551. 将珠子放入背包中

> **[yiduobo的每日leetcode 2551.将珠子放入背包中](https://zhuanlan.zhihu.com/p/638954142) · 知乎 · 2023-06-25 · 赞同 1**
> 力扣：[2551. 将珠子放入背包中](https://leetcode.cn/problems/put-marbles-in-bags/) · Hard · 灵茶山艾府：[问题转化 + 排序贪心（Python/Go/C++/Java）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2551.将珠子放入背包中

[力扣](https://leetcode.cn/problems/put-marbles-in-bags/)

题目本质上是将一个数组分割成k个子数组，那么不妨设某种分割方案的分割点分别为p[0]、p[1]、...、p[k - 2]，那么这种方案的分数就是

weights\[0\] + weights\[p\[0\]\] + weights\[p\[0\] + 1\] + ... + weights\[p\[k - 2\] + 1\] + weights\[n - 1\]

对于上面这个式子，weights[0]和weights[n - 1]是固定的，而其余的(k - 1) \* 2项则是由k - 1组连续下标构成的，那么在这里就可以将原数组weights进行变形，计算相邻项之和形成新的数组s。为了使得得分最大，就需要在s中选出最大的k - 1项，而为了使得得分最小，则需要选出最小的k - 1项。对于这个问题，则可以利用两个堆来完成这两个top k的求解，而最终答案就是最大的k - 1项之和减去最小的k - 1项之和。

最后附上python代码：

```python
class Solution(object):
    def putMarbles(self, weights, k):
        """
        :type weights: List[int]
        :type k: int
        :rtype: int
        """

        ma_heap = []
        ma = 0
        mi_heap = []
        mi = 0
        for index in range(1, len(weights)):
            s = weights[index] + weights[index - 1]

            heapq.heappush(ma_heap, s)
            ma += s
            if len(ma_heap) >= k:
                ma -= ma_heap[0]
                heapq.heappop(ma_heap)
            
            heapq.heappush(mi_heap, -s)
            mi += s
            if len(mi_heap) >= k:
                mi -= -mi_heap[0]
                heapq.heappop(mi_heap)
        
        return ma - mi
```
