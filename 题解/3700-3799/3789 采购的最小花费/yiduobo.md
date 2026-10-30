---
title: "3789. 采购的最小花费"
aliases: ["yiduobo的每日leetcode 3789.采购的最小花费"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1988661521417524813"
zhihu_id: "1988661521417524813"
zhihu_title: "yiduobo的每日leetcode 3789.采购的最小花费"
question_id: "3789"
question: "采购的最小花费"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-acquire-required-items/"
difficulty: "Medium"
rating: 1580
created: "2025-12-28T17:33:49+08:00"
updated: "2025-12-28T17:33:50+08:00"
upvotes: 1
comments: 0
---

# 3789. 采购的最小花费

> **[yiduobo的每日leetcode 3789.采购的最小花费](https://zhuanlan.zhihu.com/p/1988661521417524813) · 知乎 · 2025-12-28 · 赞同 1**
> 力扣：[3789. 采购的最小花费](https://leetcode.cn/problems/minimum-cost-to-acquire-required-items/) · Medium · 灵茶山艾府：[分类讨论，O(1) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3789.采购的最小花费

[3789. 采购的最小花费 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-acquire-required-items/description/)

题目给出五个整数cost1，cost2，costBoth，need1以及need2。

现在有三种类型的物品可以购买

- 类型1的物品花费cost1，可以用来满足类型1的需求一个单位。
- 类型2的物品花费cost2，可以用来满足类型2的需求一个单位。
- 类型3的物品花费costBoth，可以用来满足类型1和类型2的需求各一个单位。

现在要求购买一些物品，使得满足类型1的总需求至少need1，满足类型2的总需求至少need2，问可能得最小花费是多少。

首先，若costBoth比cost1和cost2之和更大，那么就分开买显然是更划算的，此时的答案就是cost1 \* need1 + cost2 \* need2。

接下来，若costBoth比cost1和cost2之和更小，那么尽量成对的买是更划算的，此时就应该先买min(need1, need2)个类型3的物品，花费为costBoth \* min(need1, need2)。此时可能还有部分类型1的需求或者类型2的需求，可以选择购买对应类型的物品，也可以继续购买类型3的物品，自然还是哪种方案便宜就选择哪种。

具体来说，若need1 \< need2，那么对于剩下的物品，单独买的话单价就是cost2，否则单价就是cost1，在这里记为c。若c大于costBoth，那么对于剩下的物品就还是通过购买类型3的物品来完成，花费为costBoth \* abs(need1 - need2)，反之，则应该单独购买，花费为c \* abs(need1 - need2)。

将这两个步骤的花费相加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, cost1, cost2, costBoth, need1, need2):
        """
        :type cost1: int
        :type cost2: int
        :type costBoth: int
        :type need1: int
        :type need2: int
        :rtype: int
        """
        
        if costBoth > cost1 + cost2:
            return cost1 * need1 + cost2 * need2
        
        res = costBoth * min(need1, need2)
        if need1 < need2:
            c = cost2
        else:
            c = cost1
        
        if costBoth < c:
            res += costBoth * abs(need1 - need2)
        else:
            res += c * abs(need1 - need2)
        
        return res
```
