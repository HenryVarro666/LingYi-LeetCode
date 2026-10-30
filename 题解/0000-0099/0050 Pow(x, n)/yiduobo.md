---
title: "50. Pow(x, n)"
aliases: ["yiduobo的每日leetcode 50.Pow(x, n)"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/math", "题单/面试经典-150-题", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/126359415"
zhihu_id: "126359415"
zhihu_title: "yiduobo的每日leetcode 50.Pow(x, n)"
question_id: "50"
question: "Pow(x, n)"
problem_url: "https://leetcode.cn/problems/powx-n/"
difficulty: "Medium"
created: "2020-04-06T23:22:40+08:00"
updated: "2020-04-06T23:22:40+08:00"
upvotes: 0
comments: 0
---

# 50. Pow(x, n)

> **[yiduobo的每日leetcode 50.Pow(x, n)](https://zhuanlan.zhihu.com/p/126359415) · 知乎 · 2020-04-06 · 赞同 0**
> 力扣：[50. Pow(x, n)](https://leetcode.cn/problems/powx-n/) · Medium · 灵茶山艾府：[【图解】一张图秒懂快速幂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

50.Pow(x, n)<https://leetcode-cn.com/problems/powx-n/>

经典的快速幂问题，有两种思路。

思路一：对于x^n，若n为偶数，那么可以认为是x^(n / 2)的平方；若n为奇数，那么就是x^(n/2)的平方再乘上一个x。递归的计算x^(n/2)知道幂为1时停止，那么一共需要计算logn次，即最终的时间复杂度为O(logn)。

思路二：将n看做二进制的数，那么二进制表示下某一位为1，则需要乘上对应的x关于2的幂次，例如x^10，10在二进制下为1010，那么从低到高位分别就是

0 \* x^1

1 \* x^2

0 \* x^4

1 \* x^8

于是只需要预先计算好x关于2的幂次，然后按n的二进制位情况乘起来即可。

上面这两种方法的本质是一样的，我在这里采用的第一种方法。

另外，题目中n可能为负数，那么直接按照题目的处理方法，即取x \= 1/x，n \= -n即可。

最后附上python代码：

```python
class Solution(object):
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """

        if x == 0:
            return 0

        if n == 0:
            return 1

        if x < 0:
            if n % 2 == 1:
                symbol_flag = -1
            else:
                symbol_flag = 1
            x = -x
        else:
            symbol_flag = 1

        if n < 0:
            x = 1 / x
            n = -n
        
        return symbol_flag * self.calc(x, n)

    def calc(self, x, n):
        if n == 1:
            return x

        tmp = self.calc(x, n / 2)
        if n % 2 == 1:
            return tmp * tmp * x
        else:
            return tmp * tmp
```
