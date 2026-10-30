---
title: "2383. 赢得比赛需要的最少训练时长"
aliases: ["yiduobo的每日leetcode 2383.赢得比赛需要的最少训练时长"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565252555"
zhihu_id: "565252555"
zhihu_title: "yiduobo的每日leetcode 2383.赢得比赛需要的最少训练时长"
question_id: "2383"
question: "赢得比赛需要的最少训练时长"
problem_url: "https://leetcode.cn/problems/minimum-hours-of-training-to-win-a-competition/"
difficulty: "Easy"
created: "2022-09-17T01:44:22+08:00"
updated: "2022-09-17T01:44:22+08:00"
upvotes: 0
comments: 0
---

# 2383. 赢得比赛需要的最少训练时长

> **[yiduobo的每日leetcode 2383.赢得比赛需要的最少训练时长](https://zhuanlan.zhihu.com/p/565252555) · 知乎 · 2022-09-17 · 赞同 0**
> 力扣：[2383. 赢得比赛需要的最少训练时长](https://leetcode.cn/problems/minimum-hours-of-training-to-win-a-competition/) · Easy · 灵茶山艾府：[贪心+一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2383.赢得比赛需要的最少训练时长

[力扣](https://leetcode.cn/problems/minimum-hours-of-training-to-win-a-competition/)

题目中有精力和经验两种数值，可以分开来考虑。

对于精力值而言，由于精力值只会不断减少，因此必须保证初始的精力值足够大。为了使得最终有精力剩余，因此初始精力至少要是energy之和加1，那么需要补充的精力值就是energy之和加1，再减去初始精力值了。

对于经验值而言，由于在过程中也会补充一些经验值，且顺序已经规定好了，那么只需一趟遍历，在经验值不足时进行补充就行了。

最后附上python代码：

```python
class Solution(object):
    def minNumberOfHours(self, initialEnergy, initialExperience, energy, experience):
        """
        :type initialEnergy: int
        :type initialExperience: int
        :type energy: List[int]
        :type experience: List[int]
        :rtype: int
        """

        res = sum(energy) + 1 - initialEnergy
        if res < 0:
            res = 0

        now = initialExperience
        for exp in experience:
            if now <= exp:
                res += exp + 1 - now
                now = exp + 1
            
            now += exp
        
        return res
```
