---
title: "2660. 保龄球游戏的获胜者"
aliases: ["yiduobo的每日leetcode 2660.保龄球游戏的获胜者"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648259322"
zhihu_id: "648259322"
zhihu_title: "yiduobo的每日leetcode 2660.保龄球游戏的获胜者"
question_id: "2660"
question: "保龄球游戏的获胜者"
problem_url: "https://leetcode.cn/problems/determine-the-winner-of-a-bowling-game/"
created: "2023-08-06T04:32:50+08:00"
updated: "2023-08-06T04:32:50+08:00"
upvotes: 1
comments: 0
---

# 2660. 保龄球游戏的获胜者

> **[yiduobo的每日leetcode 2660.保龄球游戏的获胜者](https://zhuanlan.zhihu.com/p/648259322) · 知乎 · 2023-08-06 · 赞同 1**
> 力扣：[2660. 保龄球游戏的获胜者](https://leetcode.cn/problems/determine-the-winner-of-a-bowling-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2660.保龄球游戏的获胜者

[力扣](https://leetcode.cn/problems/determine-the-winner-of-a-bowling-game/)

按照题目描述的规则一趟遍历，分别计算两个人的得分，然后根据最终得分确定比赛结果即可。

最后附上python代码：

```python
class Solution(object):
    def isWinner(self, player1, player2):
        """
        :type player1: List[int]
        :type player2: List[int]
        :rtype: int
        """

        s1 = s2 = 0
        for index in range(len(player1)):
            s1 += player1[index]
            s2 += player2[index]

            if (index > 0 and player1[index - 1] == 10) or (index > 1 and player1[index - 2] == 10):
                s1 += player1[index]
            
            if (index > 0 and player2[index - 1] == 10) or (index > 1 and player2[index - 2] == 10):
                s2 += player2[index]
        
        if s1 > s2:
            return 1
        elif s1 == s2:
            return 0
        else:
            return 2
```
