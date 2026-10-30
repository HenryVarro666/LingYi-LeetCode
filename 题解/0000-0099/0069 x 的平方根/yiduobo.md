---
title: "69. x的平方根"
aliases: ["yiduobo的每日leetcode 69.x的平方根"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/面试经典-150-题", "题单/二分算法/四-其他", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/130826635"
zhihu_id: "130826635"
zhihu_title: "yiduobo的每日leetcode 69.x的平方根"
question_id: "69"
question: "x 的平方根 "
problem_url: "https://leetcode.cn/problems/sqrtx/"
difficulty: "Easy"
created: "2020-04-15T14:34:44+08:00"
updated: "2020-04-15T14:34:44+08:00"
upvotes: 0
comments: 0
---

# 69. x的平方根

> **[yiduobo的每日leetcode 69.x的平方根](https://zhuanlan.zhihu.com/p/130826635) · 知乎 · 2020-04-15 · 赞同 0**
> 力扣：[69. x 的平方根 ](https://leetcode.cn/problems/sqrtx/) · Easy · 灵茶山艾府：[开区间二分，不用 long 类型（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

69.x的平方根<https://leetcode-cn.com/problems/sqrtx/>

数学题。我这边使用的是牛顿迭代法，具体就是设曲线为y \= f(p)，那么对于曲线y\=f(p)上的一个点(p, f(p))做切线，切线与x轴相交的点(0, p1)一定是更接近于f(p) \= 0的解的，于是可以不断做切线来逼近最终的答案。

这里的f(p) \= p^2 - x，其中x为输入的要开方的数。

那么对于一个点q，f(q) \= q^2 - x，其切线的斜率为2q，因此可以将(q, f(q))带入这个切线方程可以得到切线方程为y \= 2pq - q^2 - x。

切线与x轴相交于点((x + q^2) / 2q, 0)，于是将q迭代到(x + q^2) / 2q即可。

当某次迭代时，q与(x + q^2) / 2q相差不超过1时，说明已经找到了解的整数部分，此时直接返回即可。

最后附上python代码：

```python
class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """

        if x < 2:
            return x

        x *= 1.0
        x0 = x
        x1 = (x0 + x / x0) / 2

        while abs(x0 - x1) >= 1:
            x0 = x1
            x1 = (x0 + x / x0) / 2

        return int(x1)
```
