---
title: "772. 基本计算器III"
aliases: ["yiduobo的每日leetcode 772.基本计算器III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606392458"
zhihu_id: "606392458"
zhihu_title: "yiduobo的每日leetcode 772.基本计算器III"
question_id: "772"
question: "基本计算器III"
problem_url: "https://leetcode.cn/problems/basic-calculator-iii/"
created: "2023-02-15T00:48:07+08:00"
updated: "2023-02-15T00:48:07+08:00"
upvotes: 1
comments: 2
---

# 772. 基本计算器III

> **[yiduobo的每日leetcode 772.基本计算器III](https://zhuanlan.zhihu.com/p/606392458) · 知乎 · 2023-02-15 · 赞同 1**
> 力扣：[772. 基本计算器III](https://leetcode.cn/problems/basic-calculator-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

772.基本计算器III

[力扣](https://leetcode.cn/problems/basic-calculator-iii/)

经典的表达式求值问题，常用的处理方法是使用两个栈分别记录表达式中的数值以及运算符，并通过后续的运算符与栈中运算符的优先级关系来决定如何进行运算。

这样处理的理由是在从左向右遍历的过程中，对于一个运算符而言，当下不直接执行运算的原因可能有两点。第一点是还未的知运算对象，第二点则是可能无法确定优先级。基于这两点考虑，就需要将其储存到栈中。而对于一个新到来的运算符，其可能确立了栈顶运算符的优先级以及运算对象，因此就可以将栈顶运算符未完成的运算给完成掉，而栈顶剩余的无法完成的运算则说明还需要后续更多的信息才知道该运算应该如何进行。

具体来说，从左向右遍历表达式s，对于当前遍历到的字符s[p]：

1、s[p]是一个数字：

这个数字可能是多位数，因此需要从p开始向右一直遍历到表达式末尾或者首个不是数字的位置，期间遍历的这一段就是这个多位数，将其加入到数值栈中

2、s[p]是加号或者减号：

根据运算优先级的关系，如果当前操作符的栈顶是加、减、乘、除这四种符号之一，那么就可以立即执行操作符栈顶对应的操作，而运算的双方则为数值栈顶的两个元素。

重复此过程直到操作符栈为空或者是栈顶符号是左括号为止。

3、s[p]是乘号或者除号：

相对于情况2，此时就只能在操作符栈顶是乘号或者除号的情况时进行运算操作了。

重复此过程直到操作符栈为空或者栈顶符号不是乘号或除号为止。

4、s[p]是左括号：

此时直接将s[p]加入到栈中即可

5、s[p]是右括号：

s[p]对应的左括号为栈中最靠顶部的左括号。此时可以不断执行运算直到符号栈的栈顶元素为左括号为止。

全部遍历完成后，若此时符号栈非空，则还需要不断执行运算直到符号栈为空为止，此时数值栈中唯一的元素即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

        num_stack = []
        op_stack = []
        n = len(s)
        p = 0

        def calc(x, y, op):
            if op == '+':
                return x + y
            elif op == '-':
                return x - y
            elif op == '*':
                return x * y
            else:
                print x, y
                if x < 0:
                    if y < 0:
                        return x / y
                    else:
                        return -(-x / y)
                elif y < 0:
                    return -(x / -y)
                else:
                    return x / y

        while p < n:
            if '0' <= s[p] <= '9':
                now = 0
                while p < n and '0' <= s[p] <= '9':
                    now = now * 10 + int(s[p])
                    p += 1
                num_stack.append(now)

            elif s[p] == '+' or s[p] == '-':
                while op_stack and op_stack[-1] != '(' and op_stack[-1] != ')':
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '*' or s[p] == '/':
                while op_stack and (op_stack[-1] == '*' or op_stack[-1] == '/'):
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '(':
                op_stack.append(s[p])
                p += 1
            else:
                while op_stack[-1] != '(':
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                op_stack.pop()
                p += 1

        while op_stack:
            y, x = num_stack.pop(), num_stack.pop()
            op = op_stack.pop()
            num_stack.append(calc(x, y, op))
        
        return num_stack[-1]
```
