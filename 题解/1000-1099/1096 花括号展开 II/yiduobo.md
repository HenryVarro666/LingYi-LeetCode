---
title: "1096. 花括号展开II"
aliases: ["yiduobo的每日leetcode 1096.花括号展开II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/recursion", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374276461"
zhihu_id: "374276461"
zhihu_title: "yiduobo的每日leetcode 1096.花括号展开II"
question_id: "1096"
question: "花括号展开 II"
problem_url: "https://leetcode.cn/problems/brace-expansion-ii/"
difficulty: "Hard"
rating: 2349
created: "2021-05-22T00:01:48+08:00"
updated: "2021-05-22T00:01:48+08:00"
upvotes: 0
comments: 0
---

# 1096. 花括号展开II

> **[yiduobo的每日leetcode 1096.花括号展开II](https://zhuanlan.zhihu.com/p/374276461) · 知乎 · 2021-05-22 · 赞同 0**
> 力扣：[1096. 花括号展开 II](https://leetcode.cn/problems/brace-expansion-ii/) · Hard · 灵茶山艾府：[两种写法：递归 / 用栈模拟递归（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1096.花括号展开II

[力扣](https://leetcode-cn.com/problems/brace-expansion-ii/)

题目中已经多处明示这里应该使用集合来表示最终的结果，那么我们在处理的过程中就至少需要一个集合和一个字符串，分别表示当前得到的集合以及正在处理的字符串。当碰到一个括号或者逗号时，可能触发合并或者笛卡尔积操作，那么按一般做法需要将当前处理的字符串和集合保存下来，处理完逗号之后或者括号里面的内容之后再进行合并或者求笛卡尔积。由于需要的是最近一次的集合和字符串，那么显然应当使用栈来保存当前结果。另外，注意到这里可能有连续合并以及连续笛卡尔积的操作，因此在这里将栈按照括号同步分层是比较有利于处理优先级相关的问题。

这样一来，解决问题的雏形就有了。

一趟扫描，使用一个集合now_set和一个字符串now_s表示当前正在处理的集合以及字符串，并使用一个栈来储存上文。对于当前的字符：

1、若当前字符为左括号：

这里首先需要判断now_s是否为空。若now_s不为空，由于碰到了左括号，说明now_s已经结束，变成了now_set中的一项，那么需要将now_s加入到now_set当中，并将now_s置为空字符串。

接下来考察now_set是否为空。若now_set不为空，那么说明这里触发了笛卡尔积操作，双方分别为now_set以及当前字符与后续配对的右括号形成的括号对之间的内容。那么按之前所说，应当将now_set压入栈中，并设置操作符为乘法，然后将now_set置为空集。

最后由于是遇到了新的左括号，因此需要在栈中新加入一层。

2、若当前字符为右括号：

此时栈中最后一层需要收拢成为一个集合，那么同样是首先判断now_s是否为空。若now_s不为空，由于碰到了右括号，说明now_s已经结束，变成了now_set中的一项，那么需要将now_s加入到now_set当中，并将now_s置为空字符串。

接下里需要对栈的最后一层以及now_set进行运算，使用一个集合res来储存中间结果。若此时栈的最后一层不为空，那么弹出最后一层的栈顶集合v与对应的运算符symbol，然后与当前now_set进行运算。此时根据symbol的值又分为两种情况：

2-1）此时需要执行乘法操作：那么应当对v和now_set执行笛卡尔积，并将计算结果覆盖到now_set上。

2-2）此时需要执行加法操作：那么应当将now_set加入到res当中，但需要注意的是此时v有可能与更前面的内容触发运算操作，因此需要将now_set置为v。举个例子，对于{{a, b}c, d}这种情况，当我们处理到d时，此时栈中应当是[(a, b)乘法，(c)加法]，那么首先碰到(c)加法时，我们需要将d加入到中间结果集合res当中，然后将now_set置为c，这样才能正确触发后续的（a, b)乘法(c)操作。

重复上面的过程直到当前层的栈为空，此时将now_set置为res，然后将栈的最后一层删去，表示最后这一组括号里的内容处理完毕。

3、若当前字符为逗号：

与上面类似，首先还是判断now_s是否为空。若now_s不为空，由于碰到了逗号，说明now_s已经结束，变成了now_set中的一项，那么需要将now_s加入到now_set当中，并将now_s置为空字符串。

接下里由于是碰到了逗号，说明触发的是加法操作，因此需要将now_set压入栈中，并设置操作符为加法，然后将now_set置为空集。

需要注意的是，这里由于是逗号，因此并不需要在栈中新加一层。

4、其他情况：

此时遇到的都是小写字符，那么若此时的now_set不为空，说明触发了乘法，因此需要将now_set压入栈中，并设置操作符为乘法，然后将now_set置为空集。

接下来将当前字符添加到now_s的末尾即可。

全部扫描完成后，将now_set中的字符串排序后输出即可。

最后附上python代码：

```python
class Solution(object):
    def braceExpansionII(self, expression):
        """
        :type expression: str
        :rtype: List[str]
        """

        expression = '{' + expression + '}'

        stack = [[]]
        now_s = ''
        now_set = set()
        for char in expression:
            if char == '{':
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                if len(now_set) > 0:
                    stack[-1].append(now_set)
                    stack[-1].append('*')
                    now_set = set()
                stack.append([])

            elif char == '}':
                res = set()
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                while stack[-1]:
                    symbol = stack[-1].pop()
                    v = stack[-1].pop()
                    if symbol == '*':
                        tmp = set()
                        for x in v:
                            for y in now_set:
                                tmp.add(x + y)
                        now_set = tmp
                    else:
                        res.update(now_set)
                        now_set = v
                now_set.update(res)
                stack.pop()

            elif char == ',':
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                stack[-1].append(now_set)
                stack[-1].append('+')
                now_set = set()
            
            else:
                if len(now_set) > 0:
                    stack[-1].append(now_set)
                    stack[-1].append('*')
                    now_set = set()
                
                now_s += char

        return sorted(list(now_set))
```
