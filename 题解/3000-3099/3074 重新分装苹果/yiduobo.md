---
title: "3074. 重新分装苹果"
aliases: ["yiduobo的每日leetcode 3074.重新分装苹果"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697757676"
zhihu_id: "697757676"
zhihu_title: "yiduobo的每日leetcode 3074.重新分装苹果"
question_id: "3074"
question: "重新分装苹果"
problem_url: "https://leetcode.cn/problems/apple-redistribution-into-boxes/"
difficulty: "Easy"
rating: 1198
created: "2024-05-14T20:36:07+08:00"
updated: "2024-05-14T20:36:07+08:00"
upvotes: 0
comments: 0
---

# 3074. 重新分装苹果

> **[yiduobo的每日leetcode 3074.重新分装苹果](https://zhuanlan.zhihu.com/p/697757676) · 知乎 · 2024-05-14 · 赞同 0**
> 力扣：[3074. 重新分装苹果](https://leetcode.cn/problems/apple-redistribution-into-boxes/) · Easy · 灵茶山艾府：[排序贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3074.重新分装苹果

[. - 力扣（LeetCode）](https://leetcode.cn/problems/apple-redistribution-into-boxes/)

由于同一个包裹中的苹果可以分装到不同的箱子中，那么在这里就应该尽量选择容积大的箱子才能使得最终答案最小，于是只需先将箱子按大小从大到小排序，然后遍历苹果，按箱子容积从大到小的顺序填装苹果即可。

最后附上python代码：

```python
class Solution(object):
    def minimumBoxes(self, apple, capacity):
        """
        :type apple: List[int]
        :type capacity: List[int]
        :rtype: int
        """

        capacity.sort(reverse=True)
        p = 0
        s = 0
        for v in apple:
            s += v
            while s > capacity[p]:
                s -= capacity[p]
                p += 1
        
        return p + 1
```
