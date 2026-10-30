---
title: "43. 字符串相乘"
aliases: ["yiduobo的每日leetcode 43.字符串相乘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/124315136"
zhihu_id: "124315136"
zhihu_title: "yiduobo的每日leetcode 43.字符串相乘"
question_id: "43"
question: "字符串相乘"
problem_url: "https://leetcode.cn/problems/multiply-strings/"
created: "2020-04-03T23:49:22+08:00"
updated: "2020-04-03T23:49:22+08:00"
upvotes: 0
comments: 0
---

# 43. 字符串相乘

> **[yiduobo的每日leetcode 43.字符串相乘](https://zhuanlan.zhihu.com/p/124315136) · 知乎 · 2020-04-03 · 赞同 0**
> 力扣：[43. 字符串相乘](https://leetcode.cn/problems/multiply-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

43.字符串相乘<https://leetcode-cn.com/problems/multiply-strings/>

经典的高精度乘法问题，朴素的做法是一位一位乘，然后再加起来，平方的复杂度。

当然，使用FFT和DFT可以将时间复杂度优化到O(nlogn)。

对于一个n位数x，可以理解成以x为底的n - 1次多项式

f(x) \= a[n - 1] \* x^(n - 1) + a[n - 2] \* x^(n - 2) + ... + a[1] \* x + a[0]

取x\=10时的特殊情况。对于上面这个多项式，也可以通过n个点(x[0], f(x[0]))，(x[1], f(x[1]))，...，(x[n -1], f(x[n -1]))来表示。

于是具体思路就是：

1、将多项式表示下的数变成点表示的数

2、通过点之间的乘法等到结果的点表示

3、将结果的点表示再转换回多项式表示

正常来说步骤1和3都是平方的复杂度，而步骤2中的乘法操作也会是平方的复杂度，但是当取特殊的x时，例如复数域下单位圆的2的幂次单位根时，多项式与点之间的转换复杂度可以优化到O(nlogn)，点的乘积则是优化到O(n)。

由于具体实现非常复杂，这里最后还是选择了朴素的做法。

最后附上python代码：

```python
class Solution(object):
    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """

        if num1 == '0' or num2 == '0':
            return '0'

        m = len(num1)
        n = len(num2)
        res = [0] * (m + n)

        xpos = 0
        for i in range(m - 1, -1, -1):
            x = int(num1[i])
            ypos = 0
            for j in range(n - 1, -1, -1):
                y = int(num2[j])
                tmp = res[xpos + ypos] + x * y
                res[xpos + ypos] = tmp % 10
                res[xpos + ypos + 1] += tmp / 10
                ypos += 1
            xpos += 1

        tmp = 0
        for index in range(xpos + ypos):
            res[index] += tmp
            tmp = res[index] / 10
            res[index] %= 10

        zero_flag = True
        res_str = ''
        for index in range(xpos + ypos - 1, -1, -1):
            if res[index] == 0 and zero_flag:
                continue
            zero_flag = False
            res_str += str(res[index])

        return res_str
```
