---
title: "2361. 乘坐火车路线的最少费用"
aliases: ["yiduobo的每日leetcode 2361.乘坐火车路线的最少费用"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630507435"
zhihu_id: "630507435"
zhihu_title: "yiduobo的每日leetcode 2361.乘坐火车路线的最少费用"
question_id: "2361"
question: "乘坐火车路线的最少费用"
problem_url: "https://leetcode.cn/problems/minimum-costs-using-the-train-line/"
created: "2023-05-19T02:47:11+08:00"
updated: "2023-05-19T02:47:11+08:00"
upvotes: 0
comments: 0
---

# 2361. 乘坐火车路线的最少费用

> **[yiduobo的每日leetcode 2361.乘坐火车路线的最少费用](https://zhuanlan.zhihu.com/p/630507435) · 知乎 · 2023-05-19 · 赞同 0**
> 力扣：[2361. 乘坐火车路线的最少费用](https://leetcode.cn/problems/minimum-costs-using-the-train-line/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2361.乘坐火车路线的最少费用

[力扣](https://leetcode.cn/problems/minimum-costs-using-the-train-line/)

经典的动态规划问题。令f[i]和g[i]分别表示来到常规线路的第i站以及特快线路的第i站所需的最少费用，那么对于f[i]和g[i]，首先有边界情况f[0] \= 0，g[0] \= expressCost，而对于i > 0的情况：

1、对于f[i]：

可以乘坐常规线路从f[i - 1]来到f[i]，于是有f[i] \= f[i - 1] + regular[i - 1]

也可以乘坐特快线路从g[i - 1]来到g[i]，然后再从g[i]无代价转回到f[i]，于是有f[i] \= g[i - 1] + express[i - 1]

综合起来，就有f[i] \= min(f[i - 1] + regular[i - 1], g[i - 1] + express[i - 1])

2、对于g[i]：

可以乘坐常规线路从f[i - 1]来到f[i]，然后再花费expressCost转到特快线路，于是有g[i] \= f[i - 1] + regular[i - 1] + expressCost

也可以乘坐特快线路从g[i - 1]来到g[i]，于是有g[i] \= g[i - 1] + express[i - 1]

综合起来，就有g[i] \= min(f[i - 1] + regular[i - 1] + expressCost, g[i - 1] + express[i - 1])

很明显，每一轮的f[i]都小于等于g[i]，因此只需将每一轮的f[i]加入到答案中即可。

另外注意到每一轮的状态只与上一轮有关，因此可以使用变量迭代，省去数组的空间。

最后附上python代码：

```python
class Solution(object):
    def minimumCosts(self, regular, express, expressCost):
        """
        :type regular: List[int]
        :type express: List[int]
        :type expressCost: int
        :rtype: List[int]
        """

        f = 0
        g = expressCost

        res = []

        for r, e in zip(regular, express):
            new_f = min(f + r, g + e)
            new_g = min(f + r + expressCost, g + e)
            f, g = new_f, new_g
            res.append(f)
        
        return res
```
