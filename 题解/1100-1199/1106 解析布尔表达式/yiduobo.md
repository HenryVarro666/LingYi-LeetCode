---
title: "1106. 解析布尔表达式"
aliases: ["yiduobo的每日leetcode 1106.解析布尔表达式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374546015"
zhihu_id: "374546015"
zhihu_title: "yiduobo的每日leetcode 1106.解析布尔表达式"
question_id: "1106"
question: "解析布尔表达式"
problem_url: "https://leetcode.cn/problems/parsing-a-boolean-expression/"
created: "2021-05-23T12:56:14+08:00"
updated: "2021-05-23T12:56:14+08:00"
upvotes: 0
comments: 0
---

# 1106. 解析布尔表达式

> **[yiduobo的每日leetcode 1106.解析布尔表达式](https://zhuanlan.zhihu.com/p/374546015) · 知乎 · 2021-05-23 · 赞同 0**
> 力扣：[1106. 解析布尔表达式](https://leetcode.cn/problems/parsing-a-boolean-expression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1106.解析布尔表达式

[力扣](https://leetcode-cn.com/problems/parsing-a-boolean-expression/)

题目涉及到与或非这三种布尔运算，那么首先可以分析一下这三种运算的特点。

1、非运算：

非运算是单目运算，只要当运算对象的值确定下来就可以立即得到运算结果。不过题目这里可能出现运算嵌套的情况，因此也还是要按常规做法保留上文。

2、与运算：

与运算要求每个参与运算的对象都为真，最终结果才为真，否则就为假。那么我们可以在每确定一个运算对象的值的时候就进行检测，若值为假，那么最终的计算结果就为假，可以省略掉解析后续对象的操作。另外，由于题目给出的运算表达式都很规整，在运算符后面都有一对闭合的括号，那么当出现某个值为假时，我们就可以利用括号匹配来跳过后续的操作。

例如样例三中的&(t, f, t)这一段，在遇到f时我们就可以确定整个表达式的值为假，那么我们可以从f开始进行括号匹配，找到与&后面这个左括号匹配的右括号，并跳过f与这个右括号之间的所有内容。

当然，若中途没有跳出，那么说明每个参与运算的对象都为真，那么自然结束的情况下，也就是正常走到闭合括号时，表达式的值就必然为真。

3、或运算：

或运算要求每个参与运算的对象都为假，最终结果才为假，否则就为真。那么这里也可以参考与运算的情况，若中间出现的值为真的项，那么表达式的值就是真，并可以跳过后续的部分。若自然结束，表达式的值就是假。

接下来回到本题，依然是常见的一趟扫描，维护当前处理的运算符symbol，并利用栈来辅助进行运算。这里不需要维护当前运算的中间结果，因为根据上面的三点结论，没得到一个运算对象的值时，要么可以立即得出运算结果，要么对运算结果没有影响，因此没有必要保存当前运算的中间结果。

1、若当前字符为与、或、非运算符当中之一：

若当前的运算符symbol不为空，说明出现了运算嵌套的情况，那么需要将当前的symbol压入栈中，同时置symbol为当前字符，并将向后移动两个字符。移动两个字符的原因是运算符后面必然跟着一个左括号，可以跳过。

2、若当前字符为t或者f：

设其对应的值为v，那么依据上面的结论，若当前的运算符和v可以立即得出运算结果，那么我们就将v置为运算结果并依据括号匹配跳过后续不需要解析的部分，然后置symbol为栈顶的运算符并弹出栈顶，直到栈为空或者无法立即得出结果。

若执行完上面的操作之后，栈为空且可以理解得出运算结果，说明整个表达式已经求出了结果，那么依然是依据上面的结论返回对应的结果即可。

3、若当前字符为右括号：

说明当前的表达式自然结束。由于自然结束的表达式只有可能是与或者非，那么若此时的symbol是与，那么运算结果就是真，否则运算结果就是假。设这个结果为v。

若此时的栈为空，说明表达式已经解析完毕，返回v即可。否则就依然按情况2中的做法，将symbol置为栈顶运算符并弹出栈顶运算符，然后判断新的symbol和v是否能立即得出结果，则重复这个过程直到无法立即得出结果或者栈为空。

若执行完上面的操作之后，栈为空且可以理解得出运算结果，说明整个表达式已经求出了结果，那么依然是依据上面的结论返回对应的结果即可。

4、其他情况：

此时的字符应该是逗号，直接跳过即可。

本题依然是常规的利用栈保留上文的表达式解析类的问题，但是这里由于是布尔运算，因此无需保留中间结果的，同时可以跳过部分不需要进行的解析操作，简化了整体的流程。

最后附上python代码：

```python
class Solution(object):
    def parseBoolExpr(self, expression):
        """
        :type expression: str
        :rtype: bool
        """

        n = len(expression)
        p = 0
        v = None
        symbol = None
        stack = []
        while p < n:
            if expression[p] in ['!', '|', '&']:
                if symbol is not None:
                    stack.append(symbol)
                symbol = expression[p]
                p += 2
            elif expression[p] in ['t', 'f']:
                if expression[p] == 't':
                    v = True
                else:
                    v = False
                p += 1
                while stack and (symbol == '!' or (v and symbol == '|') or (not v and symbol == '&')):
                    if symbol == '!':
                        v = not v
                    cnt = 1
                    while cnt > 0:
                        if expression[p] == '(':
                            cnt += 1
                        elif expression[p] == ')':
                            cnt -= 1
                        p += 1

                    symbol = stack[-1]
                    stack.pop()
                
                if symbol == '!' or (v and symbol == '|') or (not v and symbol == '&'):
                    if symbol == '!':
                        return not v
                    else:
                        return v

            elif expression[p] == ')':
                p += 1
                if symbol == '|':
                    v = False
                else:
                    v = True
                if stack:
                    symbol = stack[-1]
                    stack.pop()
                else:
                    return v
                
                while stack and (symbol == '!' or (v and symbol == '|') or (not v and symbol == '&')):
                    if symbol == '!':
                        v = not v
                    cnt = 1
                    while cnt > 0:
                        if expression[p] == '(':
                            cnt += 1
                        elif expression[p] == ')':
                            cnt -= 1
                        p += 1
                    symbol = stack[-1]
                    stack.pop()
                
                if symbol == '!' or (v and symbol == '|') or (not v and symbol == '&'):
                    if symbol == '!':
                        return not v
                    else:
                        return v

            else:
                p += 1
```
