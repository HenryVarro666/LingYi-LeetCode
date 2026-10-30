---
title: "2139. 得到目标值的最少行动次数"
aliases: ["yiduobo的每日leetcode 2139.得到目标值的最少行动次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/528386570"
zhihu_id: "528386570"
zhihu_title: "yiduobo的每日leetcode 2139.得到目标值的最少行动次数"
question_id: "2139"
question: "得到目标值的最少行动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-reach-target-score/"
difficulty: "Medium"
rating: 1417
created: "2022-06-13T23:00:34+08:00"
updated: "2022-06-13T23:00:34+08:00"
upvotes: 0
comments: 0
---

# 2139. 得到目标值的最少行动次数

> **[yiduobo的每日leetcode 2139.得到目标值的最少行动次数](https://zhuanlan.zhihu.com/p/528386570) · 知乎 · 2022-06-13 · 赞同 0**
> 力扣：[2139. 得到目标值的最少行动次数](https://leetcode.cn/problems/minimum-moves-to-reach-target-score/) · Medium · 灵茶山艾府：[逆向思维 + 贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2139.得到目标值的最少行动次数

[力扣](https://leetcode.cn/problems/minimum-moves-to-reach-target-score/)

首先，如果不能使用加倍，那么对于目标target，就需要执行target - 1次加1操作，换言之，使用加倍操作相当于节省了target - 2次操作次数。为了使得总的操作数尽可能少，那么当target越大时使用加倍操作就越赚，因此在这里可以倒推，从target开始迭代，直到target等于1或者没有可用的加倍操作为止：

1、若此时加倍操作已经没有可用次数，那么就需要target - 1次操作让1变为target。此时应当将答案加上target - 1，然后直接返回

2、若此时还可以使用加倍操作，且target为偶数，那么根据最开始的结论，这就是使用加倍操作的绝佳时机，也就是从target / 2使用加倍操作之后得到了target，因此此时应当将答案加上1，然后将target除以2并继续迭代

3、若此时还可以使用加倍操作，且target为奇数，那么只有可能从target - 1执行一次加1操作得到target，因此此时应当将答案加上1，然后将target减去1并继续迭代

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, target, maxDoubles):
        """
        :type target: int
        :type maxDoubles: int
        :rtype: int
        """

        res = 0
        while target > 1 and maxDoubles > 0:
            if target % 2 == 0:
                target /= 2
                maxDoubles -= 1
                res += 1
            else:
                target -= 1
                res += 1
        
        res += target - 1
        return res
```
