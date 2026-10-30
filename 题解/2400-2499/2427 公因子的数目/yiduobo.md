---
title: "2427. 公因子的数目"
aliases: ["yiduobo的每日leetcode 2427.公因子的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582365920"
zhihu_id: "582365920"
zhihu_title: "yiduobo的每日leetcode 2427.公因子的数目"
question_id: "2427"
question: "公因子的数目"
problem_url: "https://leetcode.cn/problems/number-of-common-factors/"
difficulty: "Easy"
rating: 1172
created: "2022-11-11T00:43:27+08:00"
updated: "2022-11-11T00:43:27+08:00"
upvotes: 0
comments: 0
---

# 2427. 公因子的数目

> **[yiduobo的每日leetcode 2427.公因子的数目](https://zhuanlan.zhihu.com/p/582365920) · 知乎 · 2022-11-11 · 赞同 0**
> 力扣：[2427. 公因子的数目](https://leetcode.cn/problems/number-of-common-factors/) · Easy · 灵茶山艾府：[计算 gcd(a,b) 的因子（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2427.公因子的数目

[力扣](https://leetcode.cn/problems/number-of-common-factors/)

由于题目的数据规模非常小，那么完全可以从1开始到min(a, b)枚举所有的数x，并统计其中是a和b公因子的x的数目。

最后附上python代码：

```python
class Solution(object):
    def commonFactors(self, a, b):
        """
        :type a: int
        :type b: int
        :rtype: int
        """

        res = 0
        for x in range(1, min(a, b) + 1):
            if a % x == 0 and b % x == 0:
                res += 1
        
        return res
```
