---
title: "224. 基本计算器"
aliases: ["yiduobo的每日leetcode 224.基本计算器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149070203"
zhihu_id: "149070203"
zhihu_title: "yiduobo的每日leetcode 224.基本计算器"
question_id: "224"
question: "基本计算器"
problem_url: "https://leetcode.cn/problems/basic-calculator/"
created: "2020-06-17T23:46:31+08:00"
updated: "2020-06-17T23:50:25+08:00"
upvotes: 1
comments: 0
---

# 224. 基本计算器

> **[yiduobo的每日leetcode 224.基本计算器](https://zhuanlan.zhihu.com/p/149070203) · 知乎 · 2020-06-17 · 赞同 1**
> 力扣：[224. 基本计算器](https://leetcode.cn/problems/basic-calculator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

224.基本计算器<https://leetcode-cn.com/problems/basic-calculator/>

根据题目描述，抛去空格之后这个算式只有加号、减号、括号以及非负整数构成，于是一个自然的想法就是直接从左往右一趟算过来就好了。但是这样做的话需要想办法处理括号中的情况，简单来说就是A - (B + C - D)的情况。

一种可行的做法是记录当前括号的层数以及受到减号影响的数目，本着奇变偶不变的原则修正当前的运算符号，但是这样需要精确匹配到每个右括号对应的左括号前面是什么符号，需要使用栈来储存。既然用到了栈，那干脆就全部都丢进去好了，即碰到括号时将当前的运算结果以及运算符压入栈中，然后从0开始计算括号中的结果，计算完毕后从栈顶弹出之前的运算符和运算结果继续计算，这样就省去了判断符号个数的步骤。

最后附上python代码：

```python
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        sign = 1
        now = 0
        stack = []

        for char in s:
            if char == '+':
                res += sign * now
                sign = 1
                now = 0
            elif char == '-':
                res += sign* now
                sign = -1
                now = 0
            elif char.isdigit():
                now = now * 10 + int(char)
            elif char == '(':
                stack.append(res)
                stack.append(sign)
                res = 0
                sign = 1
            elif char == ')':
                res += sign * now
                res *= stack.pop()
                res += stack.pop()
                now = 0

        return res + sign * now
```
