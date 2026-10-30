---
title: "2548. 填满背包的最大价格"
aliases: ["yiduobo的每日leetcode 2548.填满背包的最大价格"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638945059"
zhihu_id: "638945059"
zhihu_title: "yiduobo的每日leetcode 2548.填满背包的最大价格"
question_id: "2548"
question: "填满背包的最大价格"
problem_url: "https://leetcode.cn/problems/maximum-price-to-fill-a-bag/"
created: "2023-06-22T22:37:58+08:00"
updated: "2023-06-22T22:37:58+08:00"
upvotes: 2
comments: 0
---

# 2548. 填满背包的最大价格

> **[yiduobo的每日leetcode 2548.填满背包的最大价格](https://zhuanlan.zhihu.com/p/638945059) · 知乎 · 2023-06-22 · 赞同 2**
> 力扣：[2548. 填满背包的最大价格](https://leetcode.cn/problems/maximum-price-to-fill-a-bag/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2548.填满背包的最大价格

[力扣](https://leetcode.cn/problems/maximum-price-to-fill-a-bag/)

由于本体的物品可以随意拆分，因此在这里可以使用贪心法，按价格重量比从大到小进行排序，然后一趟遍历尽量将价格重量比较高的物品加入背包中即可。

最后附上python代码：

```python
class Solution(object):
    def maxPrice(self, items, capacity):
        """
        :type items: List[List[int]]
        :type capacity: int
        :rtype: float
        """

        res = 0.0
        for p, w in sorted(items, key=lambda d:d[0] * 1.0 / d[1], reverse=True):
            if w >= capacity:
                res += capacity * 1.0 / w * p
                return res
            
            res += p
            capacity -= w

        return -1.0
```
