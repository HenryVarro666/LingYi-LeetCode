---
title: "1952. 三除数"
aliases: ["yiduobo的每日leetcode 1952.三除数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/491725753"
zhihu_id: "491725753"
zhihu_title: "yiduobo的每日leetcode 1952.三除数"
question_id: "1952"
question: "三除数"
problem_url: "https://leetcode.cn/problems/three-divisors/"
difficulty: "Easy"
rating: 1204
created: "2022-04-01T21:13:37+08:00"
updated: "2022-04-01T21:13:37+08:00"
upvotes: 0
comments: 0
---

# 1952. 三除数

> **[yiduobo的每日leetcode 1952.三除数](https://zhuanlan.zhihu.com/p/491725753) · 知乎 · 2022-04-01 · 赞同 0**
> 力扣：[1952. 三除数](https://leetcode.cn/problems/three-divisors/) · Easy · 灵茶山艾府：[Go 统计因子个数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1952.三除数

[力扣](https://leetcode-cn.com/problems/three-divisors/)

有且仅有三个约数的数必然是质数的完全平方数。

首先1肯定是没有三个约数的。对于大于1的数，则可以写成质数幂次相乘的情况，即

n \= p[0]^k[0] \* p[1]^k[1] \* ... \* p[m]^k[m]

那么n的约数的个数就是

(k[0] + 1) \* (k[1] + 1) \* ... \* (k[m] + 1)

上面这个值要等于3，说明只存在k[0]这一项，且k[0] \= 2，也就是说n \= p[0]^2，其中p[0]为质数

由于题目中n不超过10000，因此可以将100以内的质数先列举出来，若n恰好等于其中某个质数的平方，那么就返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def isThree(self, n):
        """
        :type n: int
        :rtype: bool
        """

        p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        for num in p:
            if num * num == n:
                return True

        return False
```
