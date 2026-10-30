---
title: "479. 最大回文数乘积"
aliases: ["yiduobo的每日leetcode 479.最大回文数乘积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/243394830"
zhihu_id: "243394830"
zhihu_title: "yiduobo的每日leetcode 479.最大回文数乘积"
question_id: "479"
question: "最大回文数乘积"
problem_url: "https://leetcode.cn/problems/largest-palindrome-product/"
created: "2020-09-14T22:03:09+08:00"
updated: "2020-09-14T22:03:09+08:00"
upvotes: 0
comments: 0
---

# 479. 最大回文数乘积

> **[yiduobo的每日leetcode 479.最大回文数乘积](https://zhuanlan.zhihu.com/p/243394830) · 知乎 · 2020-09-14 · 赞同 0**
> 力扣：[479. 最大回文数乘积](https://leetcode.cn/problems/largest-palindrome-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

479.最大回文数乘积<https://leetcode-cn.com/problems/largest-palindrome-product/>

看上去应该有通用的数学方法，但是暂时没什么思路，最后还是使用的暴力做法。

首先，两个n位数的乘积最多为2n位，那么最大可能的回文数就是9999...999一共2n个9，此时就是999..998899.999，接下来是999..997799..999。可以发现，每次从9999...999减去的数也是回文数，具体为1100...00，2200..00，...，100100...00，111100...00，122100..00。我的做法就是从999..99开始往下逐个枚举，然后判断其是否可能被两个n为的数相乘得到。另外，在枚举乘数时，其某位必然为奇数，且必然不为5，因此每次从9到7到3到1这样枚举下来可以在一定程度上优化运算效率。

对于n为偶数的情况，有一个下界是(10 \*\* n - 1) \* (10 \*\* n - 10 \*\* (n/2) + 1)，即

99..99 \* 99..9900..01，解出括号就有

10^2n - 10^(1.5n) + 10^n - 10^n + 10^(0.5n) - 1，可以发现前面两项与后面两项恰好形成了2n个9，而中间两项抵消。

目前不知道如何证明这是上界，另外对于n为奇数的情况暂时没找到类似的下界。

最后附上python代码：

```python
class Solution(object):
    def largestPalindrome(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 9

        

        #if n % 2 == 0:
        #    return (10 ** n - 1) * (10 ** n - 10 ** (n/2) + 1) % 1337

        base = 10 ** (n + n) - 1
        max = 10 ** n - 1
        delta = 1
        while True:
            tmp = delta_num = delta
            delta += 1
            l = 0
            while tmp:
                l += 1
                delta_num = delta_num * 10 + tmp % 10
                tmp /= 10
            delta_num *= 10 ** (n - l)
            candidate = base - delta_num

            x = max
            flag = 0
            while x * x >= candidate:
                if candidate % x == 0:
                    return candidate % 1337
                if flag == 0:
                    x -= 2
                    flag = 1
                elif flag == 1:
                    x -= 4
                    flag = 2
                elif flag == 2:
                    x -= 2
                    flag = 3
                else:
                    x -= 2
                    flag = 0
```
