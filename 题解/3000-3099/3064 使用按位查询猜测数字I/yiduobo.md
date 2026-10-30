---
title: "3064. 使用按位查询猜测数字I"
aliases: ["yiduobo的每日leetcode 3064.使用按位查询猜测数字I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696864203"
zhihu_id: "696864203"
zhihu_title: "yiduobo的每日leetcode 3064.使用按位查询猜测数字I"
question_id: "3064"
question: "使用按位查询猜测数字I"
problem_url: "https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-i/"
created: "2024-05-09T22:37:42+08:00"
updated: "2024-05-09T22:37:42+08:00"
upvotes: 1
comments: 0
---

# 3064. 使用按位查询猜测数字I

> **[yiduobo的每日leetcode 3064.使用按位查询猜测数字I](https://zhuanlan.zhihu.com/p/696864203) · 知乎 · 2024-05-09 · 赞同 1**
> 力扣：[3064. 使用按位查询猜测数字I](https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3064.使用按位查询猜测数字I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/guess-the-number-using-bitwise-questions-i/description/)

题目给出一个整数n以及一个函数commonSetBits，函数接收一个整数num作为输入，返回n和num在二进制表示中同时为1的数位有多少个，现在需要通过调用commonSetBits来确定n的大小。

由于commonSetBits返回的是二进制位上同时为1的数量，那么如果输入的num是2的幂次，就可以通过这个函数值是否为1来确定n在这一位上是否为1。

由于题目保证了n最多只有30位，那么就可以从最低位开始逐位向上考虑。使用一个变量v记录当前位对应的幂次值，每一轮都通过调用commonSetBits(v)来判断n的这一位是否为1，如果是，就将v累加到n当中，如果不是则不需要进行操作。无论是否为1，最后都需要将v倍增，然后继续考虑下一位。

最后附上python代码：

```python
# Definition of commonSetBits API.
# def commonSetBits(num):
#     """
#     :type num: int
#     :rtype: int
#     """

class Solution(object):
    def findNumber(self):
        """
        :rtype: int
        """
        
        res = 0
        v = 1
        for index in range(30):
            if commonSetBits(v):
                res += v
            v += v
        
        return res
```
