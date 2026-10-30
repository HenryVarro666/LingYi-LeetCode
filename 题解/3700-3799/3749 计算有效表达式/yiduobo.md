---
title: "3749. 计算有效表达式"
aliases: ["yiduobo的每日leetcode 3749.计算有效表达式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976001528478323880"
zhihu_id: "1976001528478323880"
zhihu_title: "yiduobo的每日leetcode 3749.计算有效表达式"
question_id: "3749"
question: "计算有效表达式"
problem_url: "https://leetcode.cn/problems/evaluate-valid-expressions/"
created: "2025-11-23T20:18:43+08:00"
updated: "2025-11-23T20:18:43+08:00"
upvotes: 1
comments: 0
---

# 3749. 计算有效表达式

> **[yiduobo的每日leetcode 3749.计算有效表达式](https://zhuanlan.zhihu.com/p/1976001528478323880) · 知乎 · 2025-11-23 · 赞同 1**
> 力扣：[3749. 计算有效表达式](https://leetcode.cn/problems/evaluate-valid-expressions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3749.计算有效表达式

[3749. 计算有效表达式 - 力扣（LeetCode）](https://leetcode.cn/problems/evaluate-valid-expressions/description/)

题目给出一个字符串形式的有效表达式expression，表示简化形式嵌套的数学表达式。

有效表达式要么是一个整数字面量，要么是一个形如op(a, b)的字符串，其中op为"add"、"sub"、"mul"、"div"之一，分表表示加、减、乘、整除，而a和b则都为有效表达式。

要求返回s的计算结果。

经典的表达式求值问题。本题中只有四种运算符，而且运算的形式是op(a, b)的形式，也就是说在这里无需考虑运算的优先级，一旦明确了某个运算中的a和b的具体数值，就可以直接进行运算了。

于是只需使用一个变量p，从头开始向后移动，在这个过程中使用栈来记录待运算的运算符以及还没有确定对应的b的a。对于当前遍历到的字符expression[p]：

1、若其是a、s、m、d之一：

此时expression[p: p+3]对应的就是一个运算符，应该将对应的运算符加入到栈中，然后将p向后移动4位。这里移动4位的理由是在运算符后面会紧接着一个左括号，因此需要额外多移动一位。

2、若其是数字或者负号：

此时expression[p]就是某个数字的开头，此时可以使用另一个q从p + 1开始向后遍历，直到q来到expression末尾或者expression[q]不是数字为止，那么expression[p: q]对应的就是这个参与运算的数字，将其提取出来，不妨记为y。

接下来，若此时栈非空，且栈顶元素是数字，就说明此时栈顶的两个元素分别为a以及op，而此时的y就是b，因此需要将栈顶的数字，也就是a，以及第二个元素，也就是操作符op，从栈中弹出，然后根据op的类型计算此次运算的结果，然后将y置为这个结果。

需要注意的是，由于表达式可能嵌套，因此以上过程可能需要执行多次，也就是说需要重复以上的步骤，直到栈为空，或者栈顶元素为操作符为止。计算完成后，还需要将此时的y加入到栈中，然后将p移动到q。

3、若其是逗号或者右括号：

此时直接将p向后移动一位即可。

全部计算完成后，栈中应该仅存一个元素，这个元素就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def evaluateExpression(self, expression):
        """
        :type expression: str
        :rtype: int
        """
        
        stack = []
        p = 0
        op = set(['a', 's', 'm', 'd'])
        while p < len(expression):
            if '0' <= expression[p] <= '9' or expression[p] == '-':
                q = p + 1
                while q < len(expression) and '0' <= expression[q] <= '9':
                    q += 1
                y = int(expression[p: q])
                while stack and stack[-1] not in op:
                    x = stack.pop()
                    o = stack.pop()
                    if o == 'a':
                        x += y
                    elif o == 's':
                        x -= y
                    elif o == 'm':
                        x *= y
                    else:
                        x //= y
                    y = x
                
                stack.append(y)
                p = q + 1

            elif expression[p] == ')' or expression[p] == ',':
                p += 1
            else:
                stack.append(expression[p])
                p += 4
        
        return stack[-1]
```
