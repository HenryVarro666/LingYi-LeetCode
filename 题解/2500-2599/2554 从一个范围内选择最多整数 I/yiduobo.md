---
title: "2554. 从一个范围内选择最多整数I"
aliases: ["yiduobo的每日leetcode 2554.从一个范围内选择最多整数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638958222"
zhihu_id: "638958222"
zhihu_title: "yiduobo的每日leetcode 2554.从一个范围内选择最多整数I"
question_id: "2554"
question: "从一个范围内选择最多整数 I"
problem_url: "https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-i/"
difficulty: "Medium"
rating: 1333
created: "2023-06-25T22:51:24+08:00"
updated: "2023-06-25T22:51:24+08:00"
upvotes: 1
comments: 0
---

# 2554. 从一个范围内选择最多整数I

> **[yiduobo的每日leetcode 2554.从一个范围内选择最多整数I](https://zhuanlan.zhihu.com/p/638958222) · 知乎 · 2023-06-25 · 赞同 1**
> 力扣：[2554. 从一个范围内选择最多整数 I](https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-i/) · Medium · 灵茶山艾府：[贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2554.从一个范围内选择最多整数I

[力扣](https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-i/)

由于选择的整数都是正整数，那么为了使得选择最多的整数，就应该尽量选择数值较小的整数。于是可以使用一个集合将被ban的整数记录下来，然后从1到n一趟遍历，不断选择没有被ban的整数直到遍历完成或者整数和超过了maxSum为止。

最后附上python代码：

```python
class Solution(object):
    def maxCount(self, banned, n, maxSum):
        """
        :type banned: List[int]
        :type n: int
        :type maxSum: int
        :rtype: int
        """

        ban_set = set(banned)
        s = 0
        res = 0
        for x in range(1, n + 1):
            if x not in ban_set and s + x <= maxSum:
                s += x
                res += 1

        return res
```
