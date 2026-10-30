---
title: "2212. 射箭比赛中的最大得分"
aliases: ["yiduobo的每日leetcode 2212.射箭比赛中的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/540850029"
zhihu_id: "540850029"
zhihu_title: "yiduobo的每日leetcode 2212.射箭比赛中的最大得分"
question_id: "2212"
question: "射箭比赛中的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-points-in-an-archery-competition/"
difficulty: "Medium"
rating: 1869
created: "2022-07-12T22:13:58+08:00"
updated: "2022-07-12T22:13:58+08:00"
upvotes: 0
comments: 0
---

# 2212. 射箭比赛中的最大得分

> **[yiduobo的每日leetcode 2212.射箭比赛中的最大得分](https://zhuanlan.zhihu.com/p/540850029) · 知乎 · 2022-07-12 · 赞同 0**
> 力扣：[2212. 射箭比赛中的最大得分](https://leetcode.cn/problems/maximum-points-in-an-archery-competition/) · Medium · 灵茶山艾府：[二进制枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2212.射箭比赛中的最大得分

[力扣](https://leetcode.cn/problems/maximum-points-in-an-archery-competition/)

由于比输了就一分都得不到，那么对于某个积分区域，bob要么一支箭都不射，要么就要比alice刚好多出一支箭。这样一来，问题就变成了12个区域，每个区域的代价为aliceArrows[i] + 1，得分为i，问bob能得到的最大得分是多少。

看题面是一个非常标准的01背包问题，不过在这里箭的总量和单个区域需要的箭的数量都很大，不能使用传统的动态规划做法。注意到题目中区域的数量非常少，那么完全可以枚举最后选择了哪些区域，一共是2^12 \= 4096种可能的情况。对于当前枚举到的选择方案，判断箭的数量是否足够，若足够就用当前方案的得分更新答案。对于当前选择方案中多出来的箭，随便放在任意区域就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumBobPoints(self, numArrows, aliceArrows):
        """
        :type numArrows: int
        :type aliceArrows: List[int]
        :rtype: List[int]
        """

        res = [0] * 12
        max_score = 0

        for state in range(4096):
            score = 0
            cnt = 0
            now = [0] * 12
            for index in range(12):
                if state & (1 << index):
                    now[index] = aliceArrows[index] + 1
                    cnt += now[index]
                    score += index
            
            if cnt <= numArrows and score > max_score:
                max_score = score
                res = now[:]
                res[0] += numArrows - cnt
        
        return res
```
