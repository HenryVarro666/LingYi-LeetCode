---
title: "2600. K件物品的最大和"
aliases: ["yiduobo的每日leetcode 2600.K件物品的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644440042"
zhihu_id: "644440042"
zhihu_title: "yiduobo的每日leetcode 2600.K件物品的最大和"
question_id: "2600"
question: "K 件物品的最大和"
problem_url: "https://leetcode.cn/problems/k-items-with-the-maximum-sum/"
difficulty: "Easy"
created: "2023-07-19T02:49:03+08:00"
updated: "2023-07-19T02:49:03+08:00"
upvotes: 0
comments: 0
---

# 2600. K件物品的最大和

> **[yiduobo的每日leetcode 2600.K件物品的最大和](https://zhuanlan.zhihu.com/p/644440042) · 知乎 · 2023-07-19 · 赞同 0**
> 力扣：[2600. K 件物品的最大和](https://leetcode.cn/problems/k-items-with-the-maximum-sum/) · Easy · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2600.K件物品的最大和

[力扣](https://leetcode.cn/problems/k-items-with-the-maximum-sum/)

为了使得和最大，很明显应该先选择1，若1不够了再选择0，若0也不够了才选择-1。那么在这里就可以对k的大小进行讨论。

若k的数量小于等于1的数量，那么就可以全部选1，此时答案就是k。

若k的数量大于1的数量，且小于等于1和0的数量之和，那么就可以选择所有的1，然后用0来补充，此时的答案就是1的数量。

若k的数量大于0和1的数量之和，那么在选走全部1和0之后，需要被迫选择一些-1才足够k个，此时可以先通过k减去1和0的数量之和得到选择-1的数量，然后用1的数量减去-1的数量得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def kItemsWithMaximumSum(self, numOnes, numZeros, numNegOnes, k):
        """
        :type numOnes: int
        :type numZeros: int
        :type numNegOnes: int
        :type k: int
        :rtype: int
        """

        if k <= numOnes:
            return k
        elif k <= numOnes + numZeros:
            return numOnes
        else:
            return numOnes - (k - numOnes - numZeros)
```
