---
title: "256. 粉刷房子"
aliases: ["yiduobo的每日leetcode 256.粉刷房子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593022223"
zhihu_id: "593022223"
zhihu_title: "yiduobo的每日leetcode 256.粉刷房子"
question_id: "256"
question: "粉刷房子"
problem_url: "https://leetcode.cn/problems/paint-house/"
created: "2022-12-20T01:10:33+08:00"
updated: "2022-12-20T01:10:33+08:00"
upvotes: 0
comments: 0
---

# 256. 粉刷房子

> **[yiduobo的每日leetcode 256.粉刷房子](https://zhuanlan.zhihu.com/p/593022223) · 知乎 · 2022-12-20 · 赞同 0**
> 力扣：[256. 粉刷房子](https://leetcode.cn/problems/paint-house/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

256.粉刷房子

[力扣](https://leetcode.cn/problems/paint-house/)

非常经典的动态规划问题。令f[i][j]表示完成前i栋房子的粉刷，其中第i栋房子的颜色为j时的最小代价，这里j的取值为0、1、2，分别代表红色、蓝色、绿色。

那么对于f[i][j]，就有

f[i][0] \= f[i - 1][1] + f[i - 1][2] + cost[i][0]

f[i][1] \= f[i - 1][0] + f[i - 1][2] + cost[i][1]

f[i][2] \= f[i - 1][0] + f[i - 1][1] + cost[i][2]

也就是对于f[i][j]而言，其上一栋房子的颜色不能为j。

注意到这里每一轮状态只与上一轮有关，因此可以将i这一维滚动掉来节省空间。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """

        n = len(costs)
        f = costs[0][:]

        for index in range(1, n):
            g = f[:]
            f[0] = min(g[1], g[2]) + costs[index][0]
            f[1] = min(g[0], g[2]) + costs[index][1]
            f[2] = min(g[0], g[1]) + costs[index][2]

        return min(f)
```
