---
title: "29. 两数相除"
aliases: ["yiduobo的每日leetcode 29.两数相除"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/118652269"
zhihu_id: "118652269"
zhihu_title: "yiduobo的每日leetcode 29.两数相除"
question_id: "29"
question: "两数相除"
problem_url: "https://leetcode.cn/problems/divide-two-integers/"
created: "2020-03-27T22:07:08+08:00"
updated: "2020-03-27T22:07:08+08:00"
upvotes: 0
comments: 0
---

# 29. 两数相除

> **[yiduobo的每日leetcode 29.两数相除](https://zhuanlan.zhihu.com/p/118652269) · 知乎 · 2020-03-27 · 赞同 0**
> 力扣：[29. 两数相除](https://leetcode.cn/problems/divide-two-integers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

29.两数相除<https://leetcode-cn.com/problems/divide-two-integers/>

不允许用除法的除法，那么就使用减法来代替除法。对于n/k，每次减k的话效率太低，例如100000000/1这种情况，需要做一亿次，减到猴年马月都减不完，于是在这里可以利用倍增的思路。简单来说，不妨设答案为ans，那么将ans写成二进制的形式，那么就是

（1）n \= k \* (1 \* p[0] + 2 \* p[1] + 4 \* p[2] + 8 \* p[3] + ... + 2^l \* p[l]) + m

其中括号中代表ans按二进制展开后的形式，最高位为l，且p[l]为1，其他的p都可能是0或者1。

那么把（1）的括号拆开后按从大到小的顺序排好，就有

（2）n \= 2^l \* p[l] \* k + 2^(l - 1) \* p[l - 1] \* k + ... + 2 \* p[1] \* k + p[0] \* k + m

于是，我们可以预先计算出所有2^l \* k，然后从大到小判断当前的p[l]是0还是1，在通过（1）中括号部分的计算方式就能还原出ans了。

另外还需要特别注意边界的判断。

最后附上python代码，其中f数组代表（2）中的2^l \* k，weight数组代表（1）中的2^l：

```python
class Solution(object):
    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """

        max_int = 2147483647
        min_int = -2147483648

        if dividend == min_int and divisor == -1:
            return max_int

        negative = False
        sign = False
        if dividend > 0 and divisor < 0:
            negative = True
            sign = True
            dividend = -dividend
        elif dividend < 0 and divisor > 0:
            negative = True
            sign = True
            divisor = -divisor
        elif dividend < 0 and divisor < 0:
            negative = True

        f = [0, divisor]
        pos = 1
        while (negative and min_int - f[pos] <= f[pos] and dividend - f[pos] <= f[pos]) or (not negative and max_int - f[pos] >= f[pos] and dividend - f[pos] >= f[pos]):
            f.append(f[pos] + f[pos])
            pos += 1

        weight = [0, 1]
        for index in range(2, len(f)):
            weight.append(weight[index -1] + weight[index - 1])
        
        ans = 0
        while dividend != 0:
            for index in range(len(f) - 1, -1, -1):
                if (negative and f[index] >= dividend) or (not negative and f[index] <= dividend):
                    break

            if index == 0:
                break

            ans += weight[index]
            dividend -= f[index]

        if sign:
            ans = -ans
        return ans
```
