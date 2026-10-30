---
title: "2214. 通关游戏所需的最低生命值"
aliases: ["yiduobo的每日leetcode 2214.通关游戏所需的最低生命值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627851546"
zhihu_id: "627851546"
zhihu_title: "yiduobo的每日leetcode 2214.通关游戏所需的最低生命值"
question_id: "2214"
question: "通关游戏所需的最低生命值"
problem_url: "https://leetcode.cn/problems/minimum-health-to-beat-game/"
created: "2023-05-08T23:48:43+08:00"
updated: "2023-05-08T23:48:43+08:00"
upvotes: 0
comments: 0
---

# 2214. 通关游戏所需的最低生命值

> **[yiduobo的每日leetcode 2214.通关游戏所需的最低生命值](https://zhuanlan.zhihu.com/p/627851546) · 知乎 · 2023-05-08 · 赞同 0**
> 力扣：[2214. 通关游戏所需的最低生命值](https://leetcode.cn/problems/minimum-health-to-beat-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2214.通关游戏所需的最低生命值

[力扣](https://leetcode.cn/problems/minimum-health-to-beat-game/)

观察样例可以发现，如果使用护盾去格挡较低的伤害，可能会浪费掉部分护盾，因此在这里就应该使用护盾去格挡最高的那次伤害，从而可知最终格挡的伤害就是min(max(damage), arror)。更进一步的，最终受到的伤害就是sum(damage) - min(max(damage), arror)，因此最终答案就是受到的伤害值加1。

最后附上python代码：

```python
class Solution(object):
    def minimumHealth(self, damage, armor):
        """
        :type damage: List[int]
        :type armor: int
        :rtype: int
        """

        return sum(damage) - min(max(damage), armor) + 1
```
