---
title: "3094. 使用按位查询猜测数字II"
aliases: ["yiduobo的每日leetcode 3094.使用按位查询猜测数字II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699511287"
zhihu_id: "699511287"
zhihu_title: "yiduobo的每日leetcode 3094.使用按位查询猜测数字II"
question_id: "3094"
question: "使用按位查询猜测数字II"
problem_url: "https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-ii/"
created: "2024-05-23T23:46:09+08:00"
updated: "2024-05-23T23:46:09+08:00"
upvotes: 1
comments: 0
---

# 3094. 使用按位查询猜测数字II

> **[yiduobo的每日leetcode 3094.使用按位查询猜测数字II](https://zhuanlan.zhihu.com/p/699511287) · 知乎 · 2024-05-23 · 赞同 1**
> 力扣：[3094. 使用按位查询猜测数字II](https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3094.使用按位查询猜测数字II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-ii/description/)

题目给出一个整数n以及一个函数commonBits，函数接收一个整数num作为输入，先计算n与num在二进制表示下值都为1的数位的数量count，然后修改n为n^num，再返回count。现在需要通过调用commonBits来确定n的大小。

最直观的处理方法还是检测所有2的幂次，对于某个2的幂次v，首先n中所有值为0的位将被计入count，另外就是这个唯一的1，如果n在这一位上也为1，那么count将额外加上1。换言之，如果知道在进行commonBits前n中0的数量zero，就可以通过commonBits(v)的结果是等于zero还是zero + 1来判断v对应的这一位是0还是1了。而为了获取n中最开始0的数量zero，则可以先调用commonBits(0)来获取到。

另外需要特别注意的是，当执行完一次commonBits(v)操作之后，v对应的这一位将会翻转，因此需要注意根据commonBits(v)的结果与zero的大小情况来更新zero的大小。

最后附上python代码：

```python
# Definition of commonBits API.
# def commonBits(num):
#     """
#     :type num: int
#     :rtype: int
#     """

class Solution(object):
    def findNumber(self):
        """
        :rtype: int
        """
        
        zero = commonBits(0)
        res = 0
        v = 1
        for index in range(30):
            if commonBits(v) > zero:
                res += v
                zero += 1
            else:
                zero -= 1
            v += v
        
        return res
```
