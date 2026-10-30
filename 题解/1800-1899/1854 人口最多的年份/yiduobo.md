---
title: "1854. 人口最多的年份"
aliases: ["yiduobo的每日leetcode 1854.人口最多的年份"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/471593881"
zhihu_id: "471593881"
zhihu_title: "yiduobo的每日leetcode 1854.人口最多的年份"
question_id: "1854"
question: "人口最多的年份"
problem_url: "https://leetcode.cn/problems/maximum-population-year/"
created: "2022-02-24T00:57:03+08:00"
updated: "2022-02-24T00:57:03+08:00"
upvotes: 0
comments: 0
---

# 1854. 人口最多的年份

> **[yiduobo的每日leetcode 1854.人口最多的年份](https://zhuanlan.zhihu.com/p/471593881) · 知乎 · 2022-02-24 · 赞同 0**
> 力扣：[1854. 人口最多的年份](https://leetcode.cn/problems/maximum-population-year/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1854.人口最多的年份

[力扣](https://leetcode-cn.com/problems/maximum-population-year/)

比较基础的题目。使用一个dict记录每年人口变化的情况，然后从1950年开始到2050年一趟遍历，通过dict中记录的这一年的人口变化，配合上一年的总人口计算出本年度的总人口，并更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumPopulation(self, logs):
        """
        :type logs: List[List[int]]
        :rtype: int
        """

        delta = {}
        for birth, death in logs:
            delta[birth] = delta.get(birth, 0) + 1
            delta[death] = delta.get(death, 0) - 1
        
        ma = 0
        res = None
        now = 0
        for y in range(1950, 2051):
            now += delta.get(y, 0)
            if now > ma:
                ma = now
                res = y
        
        return res
```
