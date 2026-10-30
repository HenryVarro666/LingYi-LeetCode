---
title: "1217. 玩筹码"
aliases: ["yiduobo的每日leetcode 1217.玩筹码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382748589"
zhihu_id: "382748589"
zhihu_title: "yiduobo的每日leetcode 1217.玩筹码"
question_id: "1217"
question: "玩筹码"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-move-chips-to-the-same-position/"
created: "2021-06-21T23:42:30+08:00"
updated: "2021-06-21T23:42:30+08:00"
upvotes: 0
comments: 0
---

# 1217. 玩筹码

> **[yiduobo的每日leetcode 1217.玩筹码](https://zhuanlan.zhihu.com/p/382748589) · 知乎 · 2021-06-21 · 赞同 0**
> 力扣：[1217. 玩筹码](https://leetcode.cn/problems/minimum-cost-to-move-chips-to-the-same-position/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1217.玩筹码

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-move-chips-to-the-same-position/)

首先，若只有一堆筹码，那么答案自然为0。接下来考虑有多对筹码的情况。

注意到题目中移动两个格子的操作代价为0，那么说明最终我们可以不花任何代价将所有筹码移动到位置0或者位置1上。接下来只需要将位置0上的筹码移动到位置1，或者将位置1上的筹码移动到位置0，那么此时花费的代价就是0上筹码堆数和1上筹码堆数的较小值。

最后附上python代码：

```python
class Solution(object):
    def minCostToMoveChips(self, position):
        """
        :type position: List[int]
        :rtype: int
        """

        odd = even = 0
        for p in position:
            if p % 2 == 0:
                even += 1
            else:
                odd += 1
            
        return min(odd, even)
```
