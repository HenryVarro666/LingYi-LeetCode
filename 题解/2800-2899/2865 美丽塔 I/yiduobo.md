---
title: "2865. 美丽塔I"
aliases: ["yiduobo的每日leetcode 2865.美丽塔I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/monotonic-stack"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661904039"
zhihu_id: "661904039"
zhihu_title: "yiduobo的每日leetcode 2865.美丽塔I"
question_id: "2865"
question: "美丽塔 I"
problem_url: "https://leetcode.cn/problems/beautiful-towers-i/"
difficulty: "Medium"
created: "2023-10-18T02:52:22+08:00"
updated: "2023-10-18T02:52:22+08:00"
upvotes: 0
comments: 0
---

# 2865. 美丽塔I

> **[yiduobo的每日leetcode 2865.美丽塔I](https://zhuanlan.zhihu.com/p/661904039) · 知乎 · 2023-10-18 · 赞同 0**
> 力扣：[2865. 美丽塔 I](https://leetcode.cn/problems/beautiful-towers-i/) · Medium · 灵茶山艾府：[O(n) 前后缀分解+单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2865.美丽塔I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/beautiful-towers-i/)

题目要求找出和最大的山状数组，根据题目描述，山峰位置是最特殊的，因此在这里就应该尝试枚举山峰的下标，然后计算选择当前下标作为山峰时两侧山坡上数值之和的最大值。

在确定了山峰之后，从山峰出发向两侧行走。这两段的处理方法是对称的，在这里以向左侧行走举例。

设h[index]表示下标index的最终高度，那么index这个位置而言，其高度不能超过右侧相邻位置的最终高度h[index + 1]。另一方面，为了使得h[index]最大，那么其取值就应该尽量向maxHeight[index]靠拢，因此h[index]的最终取值就是maxHeight[index]和h[index + 1]中的较小值。注意到这里每个下标的最终高度h的计算只与右侧相邻位置有关，因此在这里可以使用遍历迭代来代替h数组。

最后附上python代码：

```python
class Solution(object):
    def maximumSumOfHeights(self, maxHeights):
        """
        :type maxHeights: List[int]
        :rtype: int
        """

        res = 0
        n = len(maxHeights)
        for i in range(n):
            now = s = maxHeights[i]
            for j in range(i - 1, -1, -1):
                if maxHeights[j] < now:
                    now = maxHeights[j]
                s += now
            
            now = maxHeights[i]
            for j in range(i + 1, n):
                if maxHeights[j] < now:
                    now = maxHeights[j]
                s += now
            res = max(res, s)
        
        return res
```
