---
title: "3273. 对Bob造成的最少伤害"
aliases: ["yiduobo的每日leetcode 3273.对Bob造成的最少伤害"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794157024"
zhihu_id: "794157024"
zhihu_title: "yiduobo的每日leetcode 3273.对Bob造成的最少伤害"
question_id: "3273"
question: "对 Bob 造成的最少伤害"
problem_url: "https://leetcode.cn/problems/minimum-amount-of-damage-dealt-to-bob/"
difficulty: "Hard"
rating: 2013
created: "2024-10-02T04:11:13+08:00"
updated: "2024-10-02T04:11:13+08:00"
upvotes: 1
comments: 0
---

# 3273. 对Bob造成的最少伤害

> **[yiduobo的每日leetcode 3273.对Bob造成的最少伤害](https://zhuanlan.zhihu.com/p/794157024) · 知乎 · 2024-10-02 · 赞同 1**
> 力扣：[3273. 对 Bob 造成的最少伤害](https://leetcode.cn/problems/minimum-amount-of-damage-dealt-to-bob/) · Hard · 灵茶山艾府：[贪心及其证明：邻项交换法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3273.对Bob造成的最少伤害

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-amount-of-damage-dealt-to-bob/)

给出一个整数power以及两个整数数组damage和health，两个数组的长度都为n，分别表示n个敌人的血量和伤害，所有敌人在没死之前伤害都不会衰减。

在每一秒中，在所有依然存活的敌人造成伤害之后，可以选择一个敌人进行还击，这个敌人的血量将减少power。问击杀所有敌人之前所受的最少伤害是多少。

经典的先杀血少的还是先杀输出高的问题。

首先，根据伤其十指不如断其一指的说法，应该集中火力一个个击杀，而不应该轮流打每个敌人。由于bob的输出power是固定的，那么就可以先通过所有敌人的血量除以power计算出bob击杀每个敌人所需的时间times。

接下来决定击杀敌人的顺序。不妨设现在有两个敌人，击杀所需时间分别为t1和t2，每秒造成的伤害分别为d1和d2，那么如果先击杀第一个敌人，造成的总伤害就是t1 \* d1 + (t1 + t2) \* d2，反之如果先击杀第二个敌人，造成的总伤害就是(t1 + t2) \* d1 + t2 \* d2。

对比这两个式子，可以约掉t1 \* d1和t2 \* d2这两项，那么实际上就是对比t1 \* d2与d2 \* d1这两项的大小。若前者较大，那么就应该第一个敌人，否则就应该先击杀第二个敌人。

在这里可以对上面的式子进行移项，即对比t1 / d1与t2 / d2的大小，这样一来就可以根据这个指标对所有敌人进行排序来决定击杀的顺序了。直观上也很合理，既考虑到了好不好杀，也考虑到了输出高不高。

另外需要特别注意的是题目要求计算bob受到的总伤害，因此还需要额外使用一个变量s维护依然存活的敌人的总输出，接下来按上面的标准对敌人排序，然后逐个遍历进行击杀，每击杀一个敌人时计算受到的伤害并累加到答案，然后更新s。

最后附上python代码：

```python
class Solution(object):
    def minDamage(self, power, damage, health):
        """
        :type power: int
        :type damage: List[int]
        :type health: List[int]
        :rtype: int
        """

        times = [(h - 1) // power + 1 for h in health]

        s = sum(damage)
        res = 0
        for d, t in sorted(zip(damage, times), key=lambda d:(d[1] * 1.0 / d[0])):
            res += s * t
            s -= d
        
        return res
```
