---
title: "2838. Maximum Coins Heros Can Collect"
aliases: ["yiduobo的每日leetcode 2838.Maximum Coins Heros Can Collect"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659574870"
zhihu_id: "659574870"
zhihu_title: "yiduobo的每日leetcode 2838.Maximum Coins Heros Can Collect"
question_id: "2838"
question: "Maximum Coins Heros Can Collect"
problem_url: "https://leetcode.cn/problems/maximum-coins-heroes-can-collect/"
created: "2023-10-05T03:51:27+08:00"
updated: "2023-10-05T03:51:27+08:00"
upvotes: 0
comments: 0
---

# 2838. Maximum Coins Heros Can Collect

> **[yiduobo的每日leetcode 2838.Maximum Coins Heros Can Collect](https://zhuanlan.zhihu.com/p/659574870) · 知乎 · 2023-10-05 · 赞同 0**
> 力扣：[2838. Maximum Coins Heros Can Collect](https://leetcode.cn/problems/maximum-coins-heroes-can-collect/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2838.Maximum Coins Heros Can Collect

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-coins-heroes-can-collect/)

题目给出若干英雄的能力值以及若干怪兽的能力值和这些怪兽能爆的金币，问每个英雄最多可以获得多少金币。

对于这个问题，由于能力值的取值范围较大，不能直接使用树状数组等结构，需要先做离散化映射。另一种处理方法则是将英雄和怪兽都按能力值从小到大进行排序，然后利用单调性求解。

更具体的说，对于排序后的英雄heroes[i]，若其能击败的最大的怪物是monsters[j]，那么对于heroes[i + 1]，其能击败的最大的怪物monsters[k]必然满足k >\= j。这样一来，就只需先将英雄和怪物都排序，然后使用一个变量p记录当前可以击败的最大的怪物下标，接下来遍历每个英雄并更新对应的p以及可以获得的金币即可。

最后附上python代码：

```python
class Solution(object):
    def maximumCoins(self, heroes, monsters, coins):
        """
        :type heroes: List[int]
        :type monsters: List[int]
        :type coins: List[int]
        :rtype: List[int]
        """

        info = sorted(zip(monsters, coins))
        res = [0] * len(heroes)

        p = 0
        s = 0
        for index, power in sorted(enumerate(heroes), key=lambda d:d[1]):
            while p < len(info) and info[p][0] <= power:
                s += info[p][1]
                p += 1
            
            res[index] = s
        
        return res
```
