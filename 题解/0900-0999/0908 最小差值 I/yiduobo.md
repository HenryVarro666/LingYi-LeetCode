---
title: "908. 最小差值I"
aliases: ["yiduobo的每日leetcode 908.最小差值I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/graph", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354423054"
zhihu_id: "354423054"
zhihu_title: "yiduobo的每日leetcode 908.最小差值I"
question_id: "908"
question: "最小差值 I"
problem_url: "https://leetcode.cn/problems/smallest-range-i/"
difficulty: "Easy"
created: "2021-03-03T23:35:17+08:00"
updated: "2021-03-03T23:35:17+08:00"
upvotes: 0
comments: 0
---

# 908. 最小差值I

> **[yiduobo的每日leetcode 908.最小差值I](https://zhuanlan.zhihu.com/p/354423054) · 知乎 · 2021-03-03 · 赞同 0**
> 力扣：[908. 最小差值 I](https://leetcode.cn/problems/smallest-range-i/) · Easy · 灵茶山艾府：[【图】分类讨论，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

908.最小差值I

[力扣](https://leetcode-cn.com/problems/smallest-range-i/)

题目要求使得数组中最大值和最小值的差值尽量小，那么我们可以先计算出数组中max和min的差值，若这个差值小于等于两倍的K，那么就可以抹平这个差距，否则最多只能提供减少2K的差值。

最后附上python代码：

```python
class Solution(object):
    def smallestRangeI(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        max_num = min_num = A[0]
        for num in A[1:]:
            if num > max_num:
                max_num = num
            if num < min_num:
                min_num = num
                
        return max(max_num - min_num - K - K, 0)
```
