---
title: "227. 基本计算器II"
aliases: ["yiduobo的每日leetcode 227.基本计算器II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149532042"
zhihu_id: "149532042"
zhihu_title: "yiduobo的每日leetcode 227.基本计算器II"
question_id: "227"
question: "基本计算器II"
problem_url: "https://leetcode.cn/problems/basic-calculator-ii/"
created: "2020-06-19T21:39:38+08:00"
updated: "2020-06-19T21:39:38+08:00"
upvotes: 0
comments: 0
---

# 227. 基本计算器II

> **[yiduobo的每日leetcode 227.基本计算器II](https://zhuanlan.zhihu.com/p/149532042) · 知乎 · 2020-06-19 · 赞同 0**
> 力扣：[227. 基本计算器II](https://leetcode.cn/problems/basic-calculator-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

227.基本计算器II <https://leetcode-cn.com/problems/basic-calculator-ii/>

224题的升级版，这里有了乘号和除号，但是不再有括号出现。由于乘号和除号的出现，这里不能再直接计算了，因为如果碰到a + b \* c这种形式，如果直接算了a + b那就是有问题的。

考虑到乘法与除法需要优先计算，那么被乘数与被除数，以及在乘法和除法之前的算式结果就需要保存起来。还是上面这个例子，a + b \* c，在遇到乘号之前，a和b都需要保存起来。因此，栈是一个很好地选择，因为取被乘数与被除数都是取最近的那个，正好是后进先出。

另外，如果把整个式子看做若干个整数以及若干组乘法和若干组除法的加和，那么也会便于理解一些。以样例来说明：

样例一：3 + 2 \* 2

可以看做整数3，乘法算式2 \* 2的加和

样例二：3 / 2

可以看做除法算式3 / 2的加和

样例三：3 + 5 / 2

可以看做整数3，除法算式5 / 2的加和

当遇到减法时，则可以将其看作是负数的运算。例如3 - 5 / 2

可以看成整数3，除法算式-5 / 2的加和

于是题目就变成了先各自计算出乘法与除法的结果，然后统一加和即可。从左往右扫描整个式子，若当前char为某个符号时，式子一定是sign X char的形式，其中X为数值部分，sign是X前的运算符，而char是X之后的运算符。此时，我们需要对于sign分情况进行讨论。

1、若sign是加号或者减号，那么将X附上sign一起入栈。

2、若sign是乘号，说明sign之前一定有一个整数或者一个算式，不管是哪样，其一定存储在栈中，于是弹栈之后将其与X相乘再入栈即可。

3、如果sign是除号，做法与乘法一样，不过需要除数与被除数不要搞反了。

处理完整个式子之后，输出栈中元素的和即可。

最后附上python代码：

```python
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

        stack = []
        sign = '+'
        now = 0
        for index, char in enumerate(s):
            if char.isdigit():
                now = now * 10 + int(char)
            if char in '+-*/' or index == len(s) - 1:
                if sign == '+':
                    stack.append(now)
                elif sign == '-':
                    stack.append(-now)
                elif sign == '*':
                    stack.append(stack.pop() * now)
                elif sign == '/':
                    x = stack.pop()
                    if x < 0:
                        stack.append(-(-x / now))
                    else:
                        stack.append(x / now)
                
                sign = char
                now = 0

        return sum(stack)
```
