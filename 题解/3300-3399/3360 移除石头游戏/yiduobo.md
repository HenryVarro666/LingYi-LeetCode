---
title: "3360. 移除石头游戏"
aliases: ["yiduobo的每日leetcode 3360.移除石头游戏"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27331193468"
zhihu_id: "27331193468"
zhihu_title: "yiduobo的每日leetcode 3360.移除石头游戏"
question_id: "3360"
question: "移除石头游戏"
problem_url: "https://leetcode.cn/problems/stone-removal-game/"
difficulty: "Easy"
created: "2025-03-01T23:26:28+08:00"
updated: "2025-03-01T23:26:28+08:00"
upvotes: 1
comments: 0
---

# 3360. 移除石头游戏

> **[yiduobo的每日leetcode 3360.移除石头游戏](https://zhuanlan.zhihu.com/p/27331193468) · 知乎 · 2025-03-01 · 赞同 1**
> 力扣：[3360. 移除石头游戏](https://leetcode.cn/problems/stone-removal-game/) · Easy · 灵茶山艾府：[两种方法：模拟 / O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3360.移除石头游戏

[3360. 移除石头游戏 - 力扣（LeetCode）](https://leetcode.cn/problems/stone-removal-game/description/)

alice和bob在玩一个游戏，他们轮流从一堆石头中移除石头，alice先进行操作，第一轮alice必须移除10块石头，接下来的每一轮，另一位玩家需要移除的石头数量都是上一位玩家移除石头数量减一，第一位无法执行移除操作的玩家就输掉了游戏。现在给出初始的石头数量n，问alice是否能赢。

题目给出了明确的移除方案，另外石头的总数n不超过50，那么可以直接暴力计算alice获胜的情况：

alice移除10块之后，剩下的是否不足9块

alice移除10块、bob移除9块、alice移除8块之后，剩下的不足7块

alice移除10块、bob移除9块、alice移除8块、bob移除7块、alice移除6块之后，剩下的不足5块

alice移除10块、bob移除9块、alice移除8块、bob移除7块、alice移除6块，bob移除5块，alice移除4块之后，剩下的不足3块

综合起来，当石头数目在[10, 19)，[27, 34)，[40, 45)，[49, 50]时，alice必胜。

最后附上python代码：

```python
class Solution(object):
    def canAliceWin(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        return 10 <= n < 19 or 27 <= n < 34 or 40 <= n < 45 or 49 <= n
```
