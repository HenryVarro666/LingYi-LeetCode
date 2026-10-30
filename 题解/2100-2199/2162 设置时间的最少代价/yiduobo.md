---
title: "2162. 设置时间的最少代价"
aliases: ["yiduobo的每日leetcode 2162.设置时间的最少代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/532504054"
zhihu_id: "532504054"
zhihu_title: "yiduobo的每日leetcode 2162.设置时间的最少代价"
question_id: "2162"
question: "设置时间的最少代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-set-cooking-time/"
difficulty: "Medium"
rating: 1852
created: "2022-06-22T23:42:06+08:00"
updated: "2022-06-22T23:42:06+08:00"
upvotes: 0
comments: 0
---

# 2162. 设置时间的最少代价

> **[yiduobo的每日leetcode 2162.设置时间的最少代价](https://zhuanlan.zhihu.com/p/532504054) · 知乎 · 2022-06-22 · 赞同 0**
> 力扣：[2162. 设置时间的最少代价](https://leetcode.cn/problems/minimum-cost-to-set-cooking-time/) · Medium · 灵茶山艾府：[分类讨论](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2162.设置时间的最少代价

[力扣](https://leetcode.cn/problems/minimum-cost-to-set-cooking-time/)

由于最多只有4位数字，那么最多也只有一万种可能的输入，可以直接暴力求解。

需要注意的时，题目中的微波炉对不满4位的输入会自动填充上前缀0，因此在枚举每一位上的数字时需要进行特殊判断，也可以先确定输入数字的个数，强制让最高位不为0再进行枚举。

对于当前枚举的数字，计算其代表的时间以及花费的代价，并更加题目需要的时间来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minCostSetTime(self, startAt, moveCost, pushCost, targetSeconds):
        """
        :type startAt: int
        :type moveCost: int
        :type pushCost: int
        :type targetSeconds: int
        :rtype: int
        """

        res = (moveCost + pushCost) * 4
        for a in range(1, 10):
            for b in range(10):
                for c in range(10):
                    for d in range(10):
                        if a * 600 + b * 60 + c * 10 + d == targetSeconds:
                            now = pushCost * 4
                            if a != startAt:
                                now += moveCost
                            if a != b:
                                now += moveCost
                            if b != c:
                                now += moveCost
                            if c != d:
                                now += moveCost
                            res = min(res, now)
        
        for b in range(1, 10):
            for c in range(10):
                for d in range(10):
                    if b * 60 + c * 10 + d == targetSeconds:
                        now = pushCost * 3
                        if b != startAt:
                            now += moveCost
                        if b != c:
                            now += moveCost
                        if c != d:
                            now += moveCost
                        res = min(res, now)
        
        for c in range(1, 10):
            for d in range(10):
                if c * 10 + d == targetSeconds:
                    now = pushCost * 2
                    if c != startAt:
                        now += moveCost
                    if c != d:
                        now += moveCost
                    res = min(res, now)
        
        for d in range(1, 10):
            if d == targetSeconds:
                now = pushCost
                if d != startAt:
                    now += moveCost
                res = min(res, now)
        
        return res
```
