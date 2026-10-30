---
title: "639. 解码方法2"
aliases: ["yiduobo的每日leetcode 639.解码方法2"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/272229668"
zhihu_id: "272229668"
zhihu_title: "yiduobo的每日leetcode 639.解码方法2"
question_id: "639"
question: "解码方法2"
problem_url: "https://leetcode.cn/problems/decode-ways-ii/"
created: "2020-11-02T23:20:38+08:00"
updated: "2020-11-03T22:33:19+08:00"
upvotes: 0
comments: 0
---

# 639. 解码方法2

> **[yiduobo的每日leetcode 639.解码方法2](https://zhuanlan.zhihu.com/p/272229668) · 知乎 · 2020-11-02 · 赞同 0**
> 力扣：[639. 解码方法2](https://leetcode.cn/problems/decode-ways-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

639.解码方法2

[力扣](https://leetcode-cn.com/problems/decode-ways-ii/)

首先需要注意，题目描述中说到星号可以表示1到9这些数字，那么星号是不能表示0。对于单个星号的情况，可以表示1到9这9个数字；对于连续两个星号，则可以表示11到19，以及21到26这一共15个数字。

具体的做法还是动态规划。f[i]表示s中的前i个字符有多少种解码方法：

1、边界条件，当i为0时

1）若s[i] \= '0'，那么f[i] \= 0

2）若s[i] \= '\*'，那么f[i] \= 9

3）其他情况下f[i] \= 1

2、i > 0，且s[i] \= '\*'：

首先单独解码s[i]，那么就有f[i] \= f[i - 1] \* 9

接下来考察s[i - 1]，尝试组合解码s[i - 1]与s[i]：

1）若s[i - 1] \= '\*'，那么可以有15中解码方式，于是f[i] +\= f[i - 2] \* 15

2）若s[i - 1] \= '1'，那么可以有11到19这9种解码方式，于是f[i] +\= f[i - 2] \* 9

3）若s[i - 1] \= '2'，那么可以由21到26这6种解码方式，于是f[i] +\= f[i - 2] \* 6

其他情况下，无法将s[i - 1]与s[i]作为一个整体来进行解码

3、i > 0，且s[i]不为'\*'：

首先依然是单调解码s[i]，若s[i] \= '0'，那么无法单独解码，此时f[i] \= 0，否则有唯一一种解码法方式，于是有f[i] \= f[i - 1] \* 1 \= f[i - 1]

接下来考察s[i - 1]，尝试组合解码：

1）若s[i - 1] \= '\*'，且s[i] \<\= '6'，那么此时s[i - 1]可以代表1和2，于是有f[i] +\= f[i - 2] \* 2

2）若s[i - 1] \= '\*'，且s[i] > '6'，那么此时s[i - 1]只能代表1，于是有f[i] +\= f[i - 2] \* 1

3）若s[i - 1] \= '1'，那么此时有唯一一种组合解码的方式，于是有f[i] +\= f[i - 2] \* 1

4）若s[i - 2] \= '2'，且s[i] \<\= '6'，那么同时，也是f[i] +\= f[i - 2] \* 1

其他情况下，无法将s[i - 1]与s[i]作为一个整体来进行解码

有了上面的转移方程，从头到尾一趟扫描求解出f[n - 1]即可。注意到这里f的值只跟f[i - 1]以及f[i - 2]有关，那么可以使用三个变量来进行滚动计算节省空间。

最后附上python代码：

```python
class Solution(object):
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """

        l = len(s)
        mod = 10 ** 9 + 7
        a = 1
        if s[0] == '*':
            b = 9
        elif s[0] == '0':
            b = 0
        else:
            b = 1

        for index in range(1, l):
            if s[index] == '*':
                c = b * 9 % mod
                if s[index - 1] == '*':
                    c = (c + a * 15) % mod
                elif s[index - 1] == '1':
                    c = (c + a * 9) % mod
                elif s[index - 1] == '2':
                    c = (c + a * 6) % mod
            else:
                if s[index] == '0':
                    c = 0
                else:
                    c = b

                if s[index - 1] == '*':
                    if s[index] <= '6':
                        c = (c + a * 2) % mod
                    else:
                        c = (c + a) % mod
                elif s[index - 1] == '1':
                    c = (c + a) % mod
                elif s[index - 1] == '2' and s[index] <= '6':
                    c = (c + a) % mod

            a = b
            b = c

        return b
```
