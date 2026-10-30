---
title: "888. 公平的糖果棒交换"
aliases: ["yiduobo的每日leetcode 888.公平的糖果棒交换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351916133"
zhihu_id: "351916133"
zhihu_title: "yiduobo的每日leetcode 888.公平的糖果棒交换"
question_id: "888"
question: "公平的糖果棒交换"
problem_url: "https://leetcode.cn/problems/fair-candy-swap/"
created: "2021-02-21T20:03:52+08:00"
updated: "2021-02-21T20:03:52+08:00"
upvotes: 0
comments: 0
---

# 888. 公平的糖果棒交换

> **[yiduobo的每日leetcode 888.公平的糖果棒交换](https://zhuanlan.zhihu.com/p/351916133) · 知乎 · 2021-02-21 · 赞同 0**
> 力扣：[888. 公平的糖果棒交换](https://leetcode.cn/problems/fair-candy-swap/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

888.公平的糖果棒交换

[力扣](https://leetcode-cn.com/problems/fair-candy-swap/)

由于题目要求只能交换一次，那么就需要靠这一次交换抹平A和B的差值，于是可以先统计二者的和sumA和sumB，令差值diff \= sumA - sumB，接下来就只需要从A和B中找出来一组数，使其满足numA \= numB + diff / 2即可。这个查找的过程则可以利用哈希表来做。

最后附上python代码：

```python
class Solution(object):
    def fairCandySwap(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: List[int]
        """

        sumA = sumB = 0
        setA = set()
        for num in A:
            setA.add(num)
            sumA += num
        
        for num in B:
            sumB += num
        
        diff = (sumA - sumB) / 2
        for num in B:
            if num + diff in setA:
                return [num + diff, num]
```
