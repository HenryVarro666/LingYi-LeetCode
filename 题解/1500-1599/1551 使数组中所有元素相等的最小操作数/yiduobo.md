---
title: "1551. 使数组中所有元素相等的最小操作数"
aliases: ["yiduobo的每日leetcode 1551.使数组中所有元素相等的最小操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426116053"
zhihu_id: "426116053"
zhihu_title: "yiduobo的每日leetcode 1551.使数组中所有元素相等的最小操作数"
question_id: "1551"
question: "使数组中所有元素相等的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-equal/"
created: "2021-10-26T23:42:32+08:00"
updated: "2021-10-26T23:42:32+08:00"
upvotes: 0
comments: 0
---

# 1551. 使数组中所有元素相等的最小操作数

> **[yiduobo的每日leetcode 1551.使数组中所有元素相等的最小操作数](https://zhuanlan.zhihu.com/p/426116053) · 知乎 · 2021-10-26 · 赞同 0**
> 力扣：[1551. 使数组中所有元素相等的最小操作数](https://leetcode.cn/problems/minimum-operations-to-make-array-equal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1551.使数组中所有元素相等的最小操作数

[力扣](https://leetcode-cn.com/problems/minimum-operations-to-make-array-equal/)

题目要求选择数组中的两个数，让其中一个加上1，另一个减去1。换言之，这是一个零和的操作，即无论怎么操作，数组中所有数的总和是不变的。

对于一个长度为n的数字而言，其总和为

(1 + 2 \* n - 1) \* n / 2 \= n \* n

为了使得数组中这n个数都相等，那么最终操作的结果必然是让数组中的每个数都变成n。考虑到数组是一个公差为2的等差数列，那么一个自然的想法就是让数组的首尾两两组队进行操作。由于是两两组队，自然涉及到n的奇偶性的问题，分别对这两种情况进行讨论：

1、当n为奇数时，配对的情况为[1, 2 \* n - 1]、[3，2 \* n - 3]、...、[n - 2, n + 2]，除此之外还会剩下一个单独的n，那么对于每一组，其代价分别为

(n - 1) \* 2、(n - 3) \* 2、...、2 \* 2

同样也是等差数列。对其求和可得操作数

res \= (n + 1) \* ((n - 3) / 2 + 1) \* 2 \= (n + 1) \* (n - 1) / 4

2、当n为偶数时，配对的情况为[1, 2 \* n - 1]、[3，2 \* n - 3]、...、[n - 1, n + 1]，那么对于每一组，其代价分别为

(n - 1) \* 2、(n - 3) \* 2、...、1 \* 2

同样求和，可得

res \= n \* ((n - 2) / 2 + 1) / 2 \= n \* n / 4

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n & 1:
            return (n + 1) * (n - 1) / 4
        else:
            return n * n / 4
```
