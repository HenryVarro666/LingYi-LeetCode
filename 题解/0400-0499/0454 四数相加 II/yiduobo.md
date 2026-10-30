---
title: "454. 四数相加II"
aliases: ["yiduobo的每日leetcode 454.四数相加II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/214396866"
zhihu_id: "214396866"
zhihu_title: "yiduobo的每日leetcode 454.四数相加II"
question_id: "454"
question: "四数相加 II"
problem_url: "https://leetcode.cn/problems/4sum-ii/"
difficulty: "Medium"
created: "2020-09-04T00:02:59+08:00"
updated: "2020-09-04T00:02:59+08:00"
upvotes: 0
comments: 0
---

# 454. 四数相加II

> **[yiduobo的每日leetcode 454.四数相加II](https://zhuanlan.zhihu.com/p/214396866) · 知乎 · 2020-09-04 · 赞同 0**
> 力扣：[454. 四数相加 II](https://leetcode.cn/problems/4sum-ii/) · Medium · 灵茶山艾府：[O(n^2) 简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

454.四数相加II <https://leetcode-cn.com/problems/4sum-ii/>

乍一看与之前的四数之和很像，但是这里题目保证了N\<\=500，且需要从A、B、C、D中都选取一个元素。如果将A和B，C和D两两组合，那么就相当于从两个长度不超过25000的数组中各选取一个元素，使他们的和等于0。对于这个问题，很自然就想到用dict来统计每种组合值出现的次数。

统计完A和B的所有组合之后，枚举C和D中所有的数，设两数之和为x。接下来检测A和B的组合中，-x出现的次数cnt，将cnt累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def fourSumCount(self, A, B, C, D):
        """
        :type A: List[int]
        :type B: List[int]
        :type C: List[int]
        :type D: List[int]
        :rtype: int
        """

        sum = {}
        for num1 in A:
            for num2 in B:
                sum[num1 + num2] = sum.get(num1 + num2, 0) + 1

        res = 0
        for num1 in C:
            for num2 in D:
                res += sum.get(-num1 - num2, 0)

        return res
```
