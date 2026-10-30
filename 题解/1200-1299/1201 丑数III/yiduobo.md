---
title: "1201. 丑数III"
aliases: ["yiduobo的每日leetcode 1201.丑数III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/381682561"
zhihu_id: "381682561"
zhihu_title: "yiduobo的每日leetcode 1201.丑数III"
question_id: "1201"
question: "丑数III"
problem_url: "https://leetcode.cn/problems/ugly-number-iii/"
created: "2021-06-17T23:49:24+08:00"
updated: "2021-06-17T23:49:24+08:00"
upvotes: 0
comments: 0
---

# 1201. 丑数III

> **[yiduobo的每日leetcode 1201.丑数III](https://zhuanlan.zhihu.com/p/381682561) · 知乎 · 2021-06-17 · 赞同 0**
> 力扣：[1201. 丑数III](https://leetcode.cn/problems/ugly-number-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1201.丑数III

[力扣](https://leetcode-cn.com/problems/ugly-number-iii/)

经典的容斥原理的题目。

首先，设a和b的最小公倍数为lab，a和c的最小公倍数为lac，b和c的最小公倍数为lbc，三者的最小公倍数为labc。那么在1到labc当中：

有labc / a个数可以被a整除

有labc / b个数可以被b整除

有labc / c个数可以被c整除

有labc / lab个数可以同时被a和b整除

有labc / lac个数可以同时被a和c整除

有labc / lbc个数可以同时被b和c整除

另外labc自身可以同时被a、b、c整除

那么对于1到labc之间，丑数的数量就是

k \= labc / a + labc / b + labc / c - labc / lab - labc / lac - labc / lbc + labc / labc

这样计算的理由是在计算可以被a整除和可以被b整除的数时，可以同时被a和b整除的数被计算了两次。类似的，可以同时被a和c整除以及可以同时被b和c整除的数也都计算了两次，因此需要减去重复计算的次数。但是，这其中有个特例就是labc，其被计算了三次，也被减去了三次，因此最后需要加上一个1。

也就是说，从1开始，每labc个数当中有k个丑数。设p \= n / k，那么我们就可以从labc \* p开始寻找第n % k个丑数。当然，这里的也还是不能直接枚举，不过我们可以利用上面的结论，二分答案。

此时相当于从min(a, b, c)到labc之间寻找第k个丑数，那么我们可以二分答案mid，根据上面计算k的式子计算min(a, b, c)到mid之间有多少个丑数，然后修正上下界直到找到最终答案。需要注意的是，由于这里的上界必然是小于labc的，因此在计算丑数的数量时最后的1不应该加上。

最后附上python代码：

```python
class Solution(object):
    def nthUglyNumber(self, n, a, b, c):
        """
        :type n: int
        :type a: int
        :type b: int
        :type c: int
        :rtype: int
        """

        lab = a / self.gcd(a, b) * b
        lac = a / self.gcd(a, c) * c
        lbc = b / self.gcd(b, c) * c
        labc = lab / self.gcd(lab, lac) * lac

        k = labc / a + labc / b + labc / c - labc / lab - labc / lac - labc / lbc + 1
        p = n / k
        n %= k
        offset = labc * p
        if n == 0:
            return offset
        l = min(a, b, c)
        r = labc
        while l < r:
            mid = (l + r) >> 1
            k = mid / a + mid / b + mid / c - mid / lab - mid / lac - mid / lbc
            if k < n:
                l = mid + 1
            else:
                r = mid
        
        return offset + l

    
    def gcd(self, x, y):
        if y == 0:
            return x
        return self.gcd(y, x % y)
```
