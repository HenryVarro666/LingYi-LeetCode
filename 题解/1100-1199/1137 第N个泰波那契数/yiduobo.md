---
title: "1137. 第N个泰波那契数"
aliases: ["yiduobo的每日leetcode 1137.第N个泰波那契数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376860193"
zhihu_id: "376860193"
zhihu_title: "yiduobo的每日leetcode 1137.第N个泰波那契数"
question_id: "1137"
question: "第N个泰波那契数"
problem_url: "https://leetcode.cn/problems/n-th-tribonacci-number/"
created: "2021-05-31T23:28:41+08:00"
updated: "2021-05-31T23:28:41+08:00"
upvotes: 0
comments: 0
---

# 1137. 第N个泰波那契数

> **[yiduobo的每日leetcode 1137.第N个泰波那契数](https://zhuanlan.zhihu.com/p/376860193) · 知乎 · 2021-05-31 · 赞同 0**
> 力扣：[1137. 第N个泰波那契数](https://leetcode.cn/problems/n-th-tribonacci-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1137.第N个泰波那契数

[力扣](https://leetcode-cn.com/problems/n-th-tribonacci-number/)

由于这里的N不超过37，因此没必要使用矩阵快速幂之类的东西，根据定义逐个计算就行了。

最后附上python代码：

```python
class Solution(object):
    def tribonacci(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 0:
            return 0

        a, b, c = 0, 1, 1
        for index in range(3, n + 1):
            a, b, c = b, c, a + b + c
        
        return c
```
