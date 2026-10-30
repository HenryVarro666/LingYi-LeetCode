---
title: "2410. 运动员和训练师的最大匹配数"
aliases: ["yiduobo的每日leetcode 2410.运动员和训练师的最大匹配数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568467778"
zhihu_id: "568467778"
zhihu_title: "yiduobo的每日leetcode 2410.运动员和训练师的最大匹配数"
question_id: "2410"
question: "运动员和训练师的最大匹配数"
problem_url: "https://leetcode.cn/problems/maximum-matching-of-players-with-trainers/"
difficulty: "Medium"
rating: 1381
created: "2022-09-27T03:16:09+08:00"
updated: "2022-09-27T03:16:09+08:00"
upvotes: 0
comments: 0
---

# 2410. 运动员和训练师的最大匹配数

> **[yiduobo的每日leetcode 2410.运动员和训练师的最大匹配数](https://zhuanlan.zhihu.com/p/568467778) · 知乎 · 2022-09-27 · 赞同 0**
> 力扣：[2410. 运动员和训练师的最大匹配数](https://leetcode.cn/problems/maximum-matching-of-players-with-trainers/) · Medium · 灵茶山艾府：[排序 + 双指针，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2410.运动员和训练师的最大匹配数

[力扣](https://leetcode.cn/problems/maximum-matching-of-players-with-trainers/)

首先，题目只要求配对的数量最多，对运动员的能力没有要求，因此很明显就应该先让能力值低的运动员先匹配，这样才能使得成功匹配的数量最多。

接下来，对于某个运动员而言，最赚的就是让剩余的训练师中，训练能力值刚好大于运动员能力值的训练师来训练该运动员。

根据以上两点，就得到了一种利用单调性的做法：

首先将运动员和训练师都按能力值从小到大进行排序，然后遍历每位运动员。使用一个遍历p表示能满足当前运动员的能力值最小的训练师的下标，那么随着遍历的进行，p也必然是逐渐向后移动的，这样一来就可以在均摊O(1)的时间内找出每位运动员匹配的训练师的。另外，若某一时刻p到达了数组末尾，说明没有训练师能搞定当前的运动员，那么对于后续的运动员，需要的训练能力值只会更高，因此也没有训练师能搞定后续的运动员，因此匹配到这里就可以结束了。

最后附上python代码：

```python
class Solution(object):
    def matchPlayersAndTrainers(self, players, trainers):
        """
        :type players: List[int]
        :type trainers: List[int]
        :rtype: int
        """

        trainers.sort()
        p = 0
        res = 0
        for player in sorted(players):
            while p < len(trainers) and trainers[p] < player:
                p += 1
            
            if p == len(trainers):
                break
            
            res += 1
            p += 1
        
        return res
```
