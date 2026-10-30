---
title: "LCP 50. 宝石补给"
aliases: ["yiduobo的每日leetcode LCP50.宝石补给"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/577296812"
zhihu_id: "577296812"
zhihu_title: "yiduobo的每日leetcode LCP50.宝石补给"
question_id: "LCP 50"
question: "宝石补给"
created: "2022-10-26T03:28:48+08:00"
updated: "2022-10-26T03:28:48+08:00"
upvotes: 0
comments: 0
---

# LCP 50. 宝石补给

> **[yiduobo的每日leetcode LCP50.宝石补给](https://zhuanlan.zhihu.com/p/577296812) · 知乎 · 2022-10-26 · 赞同 0**
> 力扣：LCP 50. 宝石补给

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP50.宝石补给

[力扣](https://leetcode.cn/problems/WHnhjV/)

直接模拟宝石转移的过程，最后一趟遍历，找出当前宝石数组中的最大值和最小值，二者之差即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def giveGem(self, gem, operations):
        """
        :type gem: List[int]
        :type operations: List[List[int]]
        :rtype: int
        """

        for x, y in operations:
            delta = gem[x] / 2
            gem[x] -= delta
            gem[y] += delta

        ma = mi = gem[0]
        for g in gem[1:]:
            ma = max(ma, g)
            mi = min(mi, g)
        
        return ma - mi
```
