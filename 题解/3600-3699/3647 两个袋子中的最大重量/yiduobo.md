---
title: "3647. 两个袋子中的最大重量"
aliases: ["yiduobo的每日leetcode 3647.两个袋子中的最大重量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948173225830889260"
zhihu_id: "1948173225830889260"
zhihu_title: "yiduobo的每日leetcode 3647.两个袋子中的最大重量"
question_id: "3647"
question: "两个袋子中的最大重量"
problem_url: "https://leetcode.cn/problems/maximum-weight-in-two-bags/"
created: "2025-09-09T22:24:41+08:00"
updated: "2025-09-09T22:24:42+08:00"
upvotes: 0
comments: 0
---

# 3647. 两个袋子中的最大重量

> **[yiduobo的每日leetcode 3647.两个袋子中的最大重量](https://zhuanlan.zhihu.com/p/1948173225830889260) · 知乎 · 2025-09-09 · 赞同 0**
> 力扣：[3647. 两个袋子中的最大重量](https://leetcode.cn/problems/maximum-weight-in-two-bags/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3647.两个袋子中的最大重量

<https://leetcode.cn/problems/maximum-weight-in-two-bags/description/>

题目给出一个整数数组weights和两个整数w1和w2，表示两个袋子的最大容量。每个物品可以放入一个袋子中，问这两个袋子可以装入的最大总重量。

虽然有两个袋子，但是依然是背包问题。令f[k][i][j]表示前k个物品，其中第一个袋子放了重量i的物品，第二个袋子放了重量j的物品，是否可能达成。初始情况下f[0][0][0]为true，而对于f[k][i][j]，可以考虑不要weights[k]，也可以考虑将weights[k]放入第一个袋子或者第二个袋子，那么就有

f\[k\]\[i\]\[j\] \= f\[k - 1\]\[i\]\[j\] or f\[k - 1\]\[i - weights\[k\]\]\[j\] or f\[k - 1\]\[i\]\[j - weights\[k\]\]

计算结束后，遍历所有的(i, j)对，若f[-1][i][j]为true，那么就是用i + j更新答案。

另外和常规的背包问题一样，在这里也可以利用倒序遍历省去k这一维。

最后附上python代码：

```python
class Solution(object):
    def maxWeight(self, weights, w1, w2):
        """
        :type weights: List[int]
        :type w1: int
        :type w2: int
        :rtype: int
        """
        
        f = [[False] * (w2 + 1) for _ in range(w1 + 1)]
        f[0][0] = True
        for w in weights:
            for i in range(w1, -1, -1):
                for j in range(w2, -1, -1):
                    if i >= w and f[i - w][j]:
                        f[i][j] = True
                    if j >= w and f[i][j - w]:
                        f[i][j] = True
        
        res = 0
        for i in range(w1 + 1):
            for j in range(w2 + 1):
                if f[i][j]:
                    res = max(res, i + j)
        return res
```
