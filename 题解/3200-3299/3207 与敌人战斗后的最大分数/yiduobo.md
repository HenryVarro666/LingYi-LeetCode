---
title: "3207. 与敌人战斗后的最大分数"
aliases: ["yiduobo的每日leetcode 3207.与敌人战斗后的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707737848"
zhihu_id: "707737848"
zhihu_title: "yiduobo的每日leetcode 3207.与敌人战斗后的最大分数"
question_id: "3207"
question: "与敌人战斗后的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-points-after-enemy-battles/"
difficulty: "Medium"
rating: 1591
created: "2024-07-08T21:22:04+08:00"
updated: "2024-07-08T21:22:04+08:00"
upvotes: 0
comments: 0
---

# 3207. 与敌人战斗后的最大分数

> **[yiduobo的每日leetcode 3207.与敌人战斗后的最大分数](https://zhuanlan.zhihu.com/p/707737848) · 知乎 · 2024-07-08 · 赞同 0**
> 力扣：[3207. 与敌人战斗后的最大分数](https://leetcode.cn/problems/maximum-points-after-enemy-battles/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3207.与敌人战斗后的最大分数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-points-after-enemy-battles/)

题目给出一个下标从0开始的整数数组enemyEnergies，表示敌人现有的能量。另外给出一个整数currentEnergy，表示一开始拥有的能量。接下来每一轮，可以：

1、选择一个未标记，且满足currentEnergy >\= enemyEnergies[i]的敌人i与之交战，获得一分的同时将currentEnergy减去enemyEnergies[i]

2、若目前的分数大于1，则可以选择一个未标记的敌人i，将其标记，同时吸取其能量值，即将eneryEnergies[i]累加到currentEnergy中

问最大可能得得分是多少

注意到题目中的战斗操作可以对同一个敌人进行多次，同时题目要求的是分数最大，也就是战斗的次数最多，那么在这里就应该挑软柿子捏，选择与战斗力最低的敌人不断作战，同时将其他敌人的能量值都加以吸收。

于是只需计算enemyEnergies中的最小值mi以及总和s，若currentEnergy \< mi，那么说明找不到可以战斗的对手，同时初始的得分为0又无法执行吸取操作，那么对应的答案就是0。反之，则可以先将s - mi累加到currentEnergy中，表示吸取了除mi之外所有敌人的能量，然后计算currentEnergy整除mi的结果，即为可以进行战斗的次数。

最后附上python代码：

```python
class Solution(object):
    def maximumPoints(self, enemyEnergies, currentEnergy):
        """
        :type enemyEnergies: List[int]
        :type currentEnergy: int
        :rtype: int
        """

        mi = min(enemyEnergies)
        if currentEnergy < mi:
            return 0
        
        return (currentEnergy + sum(enemyEnergies) - mi) // mi
```
