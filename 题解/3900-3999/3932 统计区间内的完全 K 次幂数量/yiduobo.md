---
title: "3932. 统计区间内的完全k次幂数量"
aliases: ["yiduobo的每日leetcode 3932.统计区间内的完全k次幂数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042062249611760930"
zhihu_id: "2042062249611760930"
zhihu_title: "yiduobo的每日leetcode 3932.统计区间内的完全k次幂数量"
question_id: "3932"
question: "统计区间内的完全 K 次幂数量"
problem_url: "https://leetcode.cn/problems/count-k-th-roots-in-a-range/"
difficulty: "Medium"
created: "2026-05-25T21:26:50+08:00"
updated: "2026-05-25T21:26:50+08:00"
upvotes: 0
comments: 0
---

# 3932. 统计区间内的完全k次幂数量

> **[yiduobo的每日leetcode 3932.统计区间内的完全k次幂数量](https://zhuanlan.zhihu.com/p/2042062249611760930) · 知乎 · 2026-05-25 · 赞同 0**
> 力扣：[3932. 统计区间内的完全 K 次幂数量](https://leetcode.cn/problems/count-k-th-roots-in-a-range/) · Medium · 灵茶山艾府：[数学做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3932.统计区间内的完全k次幂数量

<https://leetcode.cn/problems/count-k-th-roots-in-a-range/description/>

题目给出三个整数l、r以及k，其中l、r满足0 \<\= l \<\= r \<\= 10^9，k的取值则在1到30之间。

如存在一个整数x，使得y \= x^k，则称整数y是一个完全k次幂。

要求计算区间[l, r]内的完全k次幂的数量。

首先，当k为1时，l到r之间的所有元素都是其自身的1次幂，因此答案就是r - l + 1。

而对于k > 1的情况，l到r之间的完全k次幂的数量显然是k次根号下r这个数量级的，基于本题的数据规模，可以使用一个变量v从0开始向上枚举，直到v^k >\= l的元素v。接下来再从v开始向上枚举，直到v^k > r为止，那么从首个满足v^k >\= l的元素v开始，到v^k \<\= r的最大的v结束，这些元素都是符合条件的完全k次幂，因此只需在枚举的过程中同步计数这些元素的数量即可。

最后附上python代码：

```python
class Solution(object):
    def countKthRoots(self, l, r, k):
        """
        :type l: int
        :type r: int
        :type k: int
        :rtype: int
        """
        
        if k == 1:
            return r - l + 1
        
        def p(x):
            v = 1
            for _ in range(k):
                v *= x
            return v

        v = 0
        res = 0
        while p(v) < l:
            v += 1
        while p(v) <= r:
            res += 1
            v += 1
        
        return res
```
