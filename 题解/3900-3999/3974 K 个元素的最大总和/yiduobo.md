---
title: "3974. K个元素的最大总和"
aliases: ["yiduobo的每日leetcode 3974.K个元素的最大总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054639818706006295"
zhihu_id: "2054639818706006295"
zhihu_title: "yiduobo的每日leetcode 3974.K个元素的最大总和"
question_id: "3974"
question: "K 个元素的最大总和"
problem_url: "https://leetcode.cn/problems/maximum-total-sum-of-k-selected-elements/"
difficulty: "Medium"
rating: 1263
created: "2026-06-28T19:24:20+08:00"
updated: "2026-06-28T19:24:23+08:00"
upvotes: 2
comments: 0
---

# 3974. K个元素的最大总和

> **[yiduobo的每日leetcode 3974.K个元素的最大总和](https://zhuanlan.zhihu.com/p/2054639818706006295) · 知乎 · 2026-06-28 · 赞同 2**
> 力扣：[3974. K 个元素的最大总和](https://leetcode.cn/problems/maximum-total-sum-of-k-selected-elements/) · Medium · 灵茶山艾府：[排序不等式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3974.K个元素的最大总和

<https://leetcode.cn/problems/maximum-total-sum-of-k-selected-elements/description/>

题目给出一个正整数数组nums以及两个整数k和mul。

现在要求从nums中选出k个元素，按任意顺序逐个处理这些元素。

对于每个被选择的元素，可以将该元素的值直接加入到总和当中，或者将该元素乘以mul后加入到总和当中。

无论选择哪种操作，mul都会减少1。mul可以变为0或者负数。

问最大可能的和是多少。

首先，为了使得总和最大，操作的元素就应该是nums中最大的k个数。又由于nums中都是正整数，因此当mul大于0时，显然应该执行乘法后再加入总和的操作，反之则应该将元素值直接加入到总和当中。

另一方面，对于两个元素x和y且mul > 1，那么x先操作，y后操作得到的总和为x \* mul + y \* (mul - 1) \= (x + y) \* mul - y，而先操作y得到的则是(x + y) \* mul - x。从这里可以看出，先操作的较大的元素收益更大。

基于以上两点，在这里就只需要对nums从大到小进行一趟排序，然后遍历前k个元素。对于当前遍历到的元素v，若当前的mul大于0，则将v \* mul累加到答案中，并将mul减去1，否则直接将v累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums, k, mul):
        """
        :type nums: List[int]
        :type k: int
        :type mul: int
        :rtype: int
        """
        
        nums.sort(reverse=True)
        res = 0
        for v in nums[:k]:
            if mul > 0:
                res += mul * v
                mul -= 1
            else:
                res += v
        
        return res
```
