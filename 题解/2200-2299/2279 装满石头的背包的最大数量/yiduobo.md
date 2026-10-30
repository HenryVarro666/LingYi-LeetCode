---
title: "2279. 装满石头的背包的最大数量"
aliases: ["yiduobo的每日leetcode 2279.装满石头的背包的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550866759"
zhihu_id: "550866759"
zhihu_title: "yiduobo的每日leetcode 2279.装满石头的背包的最大数量"
question_id: "2279"
question: "装满石头的背包的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/"
difficulty: "Medium"
rating: 1249
created: "2022-08-07T15:43:18+08:00"
updated: "2022-08-07T15:43:18+08:00"
upvotes: 0
comments: 0
---

# 2279. 装满石头的背包的最大数量

> **[yiduobo的每日leetcode 2279.装满石头的背包的最大数量](https://zhuanlan.zhihu.com/p/550866759) · 知乎 · 2022-08-07 · 赞同 0**
> 力扣：[2279. 装满石头的背包的最大数量](https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/) · Medium · 灵茶山艾府：[排序 + 贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2279.装满石头的背包的最大数量

[力扣](https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/)

由于背包的权重都是一样的，因此在这里就应该优先填满剩余空间小的背包，这样才能使得最终被填满的背包最多。于是可以按照背包的剩余空间从小到大进行排序，然后一趟遍历经历填充背包就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumBags(self, capacity, rocks, additionalRocks):
        """
        :type capacity: List[int]
        :type rocks: List[int]
        :type additionalRocks: int
        :rtype: int
        """

        res = 0
        for space in sorted([capacity[index] - rocks[index] for index in range(len(capacity))]):
            if additionalRocks < space:
                break
            res += 1
            additionalRocks -= space
        
        return res
```
