---
title: "LCP 06. 拿硬币"
aliases: ["yiduobo的每日leetcode LCP06.拿硬币"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570475453"
zhihu_id: "570475453"
zhihu_title: "yiduobo的每日leetcode LCP06.拿硬币"
question_id: "LCP 06"
question: "拿硬币"
problem_url: "https://leetcode.cn/problems/na-ying-bi/"
created: "2022-10-04T04:47:10+08:00"
updated: "2022-10-04T04:47:10+08:00"
upvotes: 0
comments: 0
---

# LCP 06. 拿硬币

> **[yiduobo的每日leetcode LCP06.拿硬币](https://zhuanlan.zhihu.com/p/570475453) · 知乎 · 2022-10-04 · 赞同 0**
> 力扣：[LCP 06. 拿硬币](https://leetcode.cn/problems/na-ying-bi/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP06.拿硬币

[力扣](https://leetcode.cn/problems/na-ying-bi/)

为了使得拿的次数尽量少，就应该尽量两个两个地拿，那么对于一堆k个硬币而言，拿完地次数就是k除以2向上取整。于是只需遍历每一堆硬币，计算拿完所需的操作次数并累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minCount(self, coins):
        """
        :type coins: List[int]
        :rtype: int
        """

        res = 0
        for coin in coins:
            res += (coin + 1) / 2
        
        return res
```
