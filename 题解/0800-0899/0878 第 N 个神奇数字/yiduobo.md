---
title: "878. 第N个神奇数字"
aliases: ["yiduobo的每日leetcode 878.第N个神奇数字"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/数学算法", "题单/二分算法/二-二分答案", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350568420"
zhihu_id: "350568420"
zhihu_title: "yiduobo的每日leetcode 878.第N个神奇数字"
question_id: "878"
question: "第 N 个神奇数字"
problem_url: "https://leetcode.cn/problems/nth-magical-number/"
difficulty: "Hard"
rating: 1897
created: "2021-02-17T00:19:35+08:00"
updated: "2021-02-17T00:19:35+08:00"
upvotes: 0
comments: 0
---

# 878. 第N个神奇数字

> **[yiduobo的每日leetcode 878.第N个神奇数字](https://zhuanlan.zhihu.com/p/350568420) · 知乎 · 2021-02-17 · 赞同 0**
> 力扣：[878. 第 N 个神奇数字](https://leetcode.cn/problems/nth-magical-number/) · Hard · 灵茶山艾府：[二分答案+容斥原理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

878.第N个神奇数字

[力扣](https://leetcode-cn.com/problems/nth-magical-number/)

首先，可以注意到一定时存在某些数字同时可以整除A和B，那么对于这些数字而言，在计数时只能计算一次。

这些数字中，最小的显然就是A和B的最小公倍数p，那么每p个数中就有p/A个数能整除A，p/B个数能整除B，p本身能同时整除A和B，因此每p个数中就有p/A + p/B - 1个数可以整除A或者B，记这个数为cnt。

接下来，我们就可以利用上面p和cnt的性质，来确定第n个数位于第几个p的区间内，同时让n对cnt取模，得到k，k即为在当前的p区间内答案是第几个数。

最后我们需要找出当前p区间内第k大的数，于是可以令x为A，y为B然后进行枚举。若此时的x较小，那么让x加上A，否则让y加上B，重复k轮之后，x和y中较小的数即为所求。

最后附上python代码：

```python
class Solution(object):
    def nthMagicalNumber(self, n, a, b):
        """
        :type n: int
        :type a: int
        :type b: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        n -= 1
        p = a * b / self.gcd(a, b)
        cnt = p / a + p / b - 1
        res = n / cnt * p % mod
        n %= cnt
        x = a
        y = b
        while n:
            if x < y:
                x += a
            else:
                y += b
            n -= 1
        return (res + min(x, y)) % mod
    
    def gcd(self, x, y):
        while y:
            x, y = y, x % y
        return x
```
