---
title: "2260. 必须拿起的最小连续卡牌数"
aliases: ["yiduobo的每日leetcode 2260.必须拿起的最小连续卡牌数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548106460"
zhihu_id: "548106460"
zhihu_title: "yiduobo的每日leetcode 2260.必须拿起的最小连续卡牌数"
question_id: "2260"
question: "必须拿起的最小连续卡牌数"
problem_url: "https://leetcode.cn/problems/minimum-consecutive-cards-to-pick-up/"
difficulty: "Medium"
rating: 1365
created: "2022-07-30T23:59:09+08:00"
updated: "2022-07-30T23:59:09+08:00"
upvotes: 0
comments: 0
---

# 2260. 必须拿起的最小连续卡牌数

> **[yiduobo的每日leetcode 2260.必须拿起的最小连续卡牌数](https://zhuanlan.zhihu.com/p/548106460) · 知乎 · 2022-07-30 · 赞同 0**
> 力扣：[2260. 必须拿起的最小连续卡牌数](https://leetcode.cn/problems/minimum-consecutive-cards-to-pick-up/) · Medium · 灵茶山艾府：[贪心+哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2260.必须拿起的最小连续卡牌数

[力扣](https://leetcode.cn/problems/minimum-consecutive-cards-to-pick-up/)

首先可以明确的是，最终拿走的卡牌中必然是首尾卡牌相同，同时中部也没有与头尾相同的卡牌出现。这个结论是很明显的，因为如果出现了与头尾相同的卡牌，那么选择这张卡牌和头部的卡牌之后就能得到更短的合法序列。

也就是说，对于任意位置的卡牌cards[index]，只需要找到其左侧最后一次出现的相同卡牌，然后使用这两个位置间的距离更新答案就能找到最优解。

于是可以使用一个哈希表统计每种卡牌最后一次出现的位置，然后从左向右一趟遍历，若当前卡牌在之前出现过，那么使用哈希表中储存的最后一次出现的位置与当前位置作差来更新答案。除此之外，还需要更新这张卡牌最后一次出现的位置为当前位置。

最后附上python代码：

```python
class Solution(object):
    def minimumCardPickup(self, cards):
        """
        :type cards: List[int]
        :rtype: int
        """

        res = -1
        last_pos = {}
        for index, card in enumerate(cards):
            if card in last_pos:
                if res == -1 or index - last_pos[card] + 1 < res:
                    res = index - last_pos[card] + 1
            
            last_pos[card] = index
        
        return res
```
