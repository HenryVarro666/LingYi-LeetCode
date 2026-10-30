---
title: "786. 第K个最小的素数分数"
aliases: ["yiduobo的每日leetcode 786.第K个最小的素数分数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341103535"
zhihu_id: "341103535"
zhihu_title: "yiduobo的每日leetcode 786.第K个最小的素数分数"
question_id: "786"
question: "第K个最小的素数分数"
problem_url: "https://leetcode.cn/problems/k-th-smallest-prime-fraction/"
created: "2020-12-31T21:58:05+08:00"
updated: "2020-12-31T21:58:05+08:00"
upvotes: 0
comments: 0
---

# 786. 第K个最小的素数分数

> **[yiduobo的每日leetcode 786.第K个最小的素数分数](https://zhuanlan.zhihu.com/p/341103535) · 知乎 · 2020-12-31 · 赞同 0**
> 力扣：[786. 第K个最小的素数分数](https://leetcode.cn/problems/k-th-smallest-prime-fraction/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

786.第K个最小的素数分数

[力扣](https://leetcode-cn.com/problems/k-th-smallest-prime-fraction/)

这一题与之前做过的378题很类似，也是在一个行列分别增长的矩阵中求第k小的值，因此也可以使用二分法来做。

我在这里并没有采用二分法，主要原因是这里需要在实数上进行二分，然后最终再返还回分数，感觉比较麻烦。

我的做法是维护最小堆，初始化的时候将所有的1/m加入到堆中。接下来执行k轮，每轮弹出堆中最小值，同时将最小值所在行的下一个数加入到堆中，这样一来就可以保证每一行最小的数都在堆中，而每一轮弹出的数就是整个矩阵中的最小值，那么在第k轮弹出的数就是最终答案了。

最后附上python代码：

```python
import heapq

class Solution(object):
    def kthSmallestPrimeFraction(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: List[int]
        """

        n = len(A)
        pos_list = [0] * n
        heap = []
        for index in range(1, n):
            heapq.heappush(heap, (A[0] * 1.0 / A[index], 0, index))

        while K:
            v, x, y = heapq.heappop(heap)
            if x < y - 1:
                heapq.heappush(heap, (A[x + 1] * 1.0 / A[y], x + 1, y))
            K -= 1
            if K == 0:
                return [A[x], A[y]]
```
