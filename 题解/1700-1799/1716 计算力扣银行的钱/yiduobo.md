---
title: "1716. 计算力扣银行的钱"
aliases: ["yiduobo的每日leetcode 1716.计算力扣银行的钱"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/450073032"
zhihu_id: "450073032"
zhihu_title: "yiduobo的每日leetcode 1716.计算力扣银行的钱"
question_id: "1716"
question: "计算力扣银行的钱"
problem_url: "https://leetcode.cn/problems/calculate-money-in-leetcode-bank/"
difficulty: "Easy"
rating: 1295
created: "2021-12-26T19:15:06+08:00"
updated: "2021-12-26T19:15:06+08:00"
upvotes: 0
comments: 0
---

# 1716. 计算力扣银行的钱

> **[yiduobo的每日leetcode 1716.计算力扣银行的钱](https://zhuanlan.zhihu.com/p/450073032) · 知乎 · 2021-12-26 · 赞同 0**
> 力扣：[1716. 计算力扣银行的钱](https://leetcode.cn/problems/calculate-money-in-leetcode-bank/) · Easy · 灵茶山艾府：[O(1) 等差数列求和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1716.计算力扣银行的钱

[力扣](https://leetcode-cn.com/problems/calculate-money-in-leetcode-bank/)

首先，一共会经历m \= n / 7个完整的星期，以及多出来的k \= n % 7天。

对于完整的星期而言，两个相邻的星期之间可以视为每天有1块钱的差，那么一星期下来就是7块钱。

记第一个星期的总额为w1，那么后续星期的总额分别为w1 + 7, w1 + 7 \* 2, ..., w1 + 7 \* (m - 1)。这是一个长度为m的等差数列，那么总额就是(w1 + w1 + 7 \* (m - 1)) \* m / 2。

对于w1，很容易得知w1 \= 28，将其带入即可。

对于剩余的k天，由于已经经过了m个完整的星期，那么这k天所在的星期的起步价就是m + 1。一共有k天，那么最后一天的价格就是m + k，所以总额就是(m + 1 + m + k) \* m / 2。

求出这两部分的总额之后，二者的和就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def totalMoney(self, n):
        """
        :type n: int
        :rtype: int
        """

        k = n % 7
        n /= 7

        res = (28 + 28 + 7 * (n - 1)) * n / 2
        res += (n + 1 + n + k) * k / 2
        return res
```
