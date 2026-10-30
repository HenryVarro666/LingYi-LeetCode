---
title: "LCP 55. 采集果实"
aliases: ["yiduobo的每日leetcode LCP55.采集果实"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578392343"
zhihu_id: "578392343"
zhihu_title: "yiduobo的每日leetcode LCP55.采集果实"
question_id: "LCP 55"
question: "采集果实"
created: "2022-10-29T02:40:33+08:00"
updated: "2022-10-29T02:40:33+08:00"
upvotes: 0
comments: 0
---

# LCP 55. 采集果实

> **[yiduobo的每日leetcode LCP55.采集果实](https://zhuanlan.zhihu.com/p/578392343) · 知乎 · 2022-10-29 · 赞同 0**
> 力扣：LCP 55. 采集果实

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP55.采集果实

[力扣](https://leetcode.cn/problems/PTXy4P/)

一趟遍历，计算采集每种果实所需的轮次，然后乘以单轮的时间，累加之后就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def getMinimumTime(self, time, fruits, limit):
        """
        :type time: List[int]
        :type fruits: List[List[int]]
        :type limit: int
        :rtype: int
        """

        res = 0
        for type, num in fruits:
            t = (num - 1) / limit + 1
            res += time[type] * t
        
        return res
```
