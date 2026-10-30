---
title: "371. 两整数之和"
aliases: ["yiduobo的每日leetcode 371.两整数之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165143514"
zhihu_id: "165143514"
zhihu_title: "yiduobo的每日leetcode 371.两整数之和"
question_id: "371"
question: "两整数之和"
problem_url: "https://leetcode.cn/problems/sum-of-two-integers/"
created: "2020-07-29T22:20:08+08:00"
updated: "2020-07-29T22:20:08+08:00"
upvotes: 0
comments: 0
---

# 371. 两整数之和

> **[yiduobo的每日leetcode 371.两整数之和](https://zhuanlan.zhihu.com/p/165143514) · 知乎 · 2020-07-29 · 赞同 0**
> 力扣：[371. 两整数之和](https://leetcode.cn/problems/sum-of-two-integers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

371.两整数之后<https://leetcode-cn.com/problems/sum-of-two-integers/>

我在这里采用的是位运算的做法。

首先，异或运算可以认为是不进位的加法运算，于是对于两个整数a和b，我们可以先通过异或得出没有进位的各位之后。对于进位的那些位，需要满足a和b在那一位上都为1，于是可以通过与运算取出这些位，然后左移一位就是进位的结果了。

此时，我们有了不进位的加法和以及进位的值，需要将二者相加，那么直接重复上面这个过程直到进位为0即可。

需要注意的是，如果使用python来实现的话，由于整数无上界，因此对于越界以及负数的情况需要进行特别处理。我在这里是多给了一位，即按照2^32来划定边界，然后判断最终结果与2^31 - 1的大小来确定符合并反向映射回整数的范围之内。

最后附上python代码：

```python
class Solution(object):
    def getSum(self, a, b):
        """
        :type a: int
        :type b: int
        :rtype: int
        """

        while a:
            tmp = a ^ b
            a &= b
            a <<= 1
            b = tmp
            a %= 4294967296
            b %= 4294967296

        if b > 2147483647:
            return ~((b % 2147483648) ^ 2147483647)
        else:
            return b
```
