---
title: "385. 迷你语法分析器"
aliases: ["yiduobo的每日leetcode 385.迷你语法分析器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/168792676"
zhihu_id: "168792676"
zhihu_title: "yiduobo的每日leetcode 385.迷你语法分析器"
question_id: "385"
question: "迷你语法分析器"
problem_url: "https://leetcode.cn/problems/mini-parser/"
created: "2020-08-06T00:14:27+08:00"
updated: "2020-08-06T00:14:27+08:00"
upvotes: 1
comments: 0
---

# 385. 迷你语法分析器

> **[yiduobo的每日leetcode 385.迷你语法分析器](https://zhuanlan.zhihu.com/p/168792676) · 知乎 · 2020-08-06 · 赞同 1**
> 力扣：[385. 迷你语法分析器](https://leetcode.cn/problems/mini-parser/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

385.迷你语法分析器<https://leetcode-cn.com/problems/mini-parser/>

这类问题一般做法就是弄一个栈，在碰到某些特定字符时将当前结果压入栈中，然后继续往后处理，直到碰到另一个特定字符时就将栈中的值弹出进行某些运算。之前有几道表达式求值的问题也是同样的处理方法。

回到问题当中。这里的特殊符号包括左括号、右括号以及逗号。

1、遇到左括号时，表示之后的内容属于一个NestedInteger，于是new一个NestedInteger并将其压入栈中。

2、遇到右括号时，表示当前的NestedInteger完结。如果最后一项是数字，那么需要先将这个数字添加到NestedInteger中，然后逐个弹栈将嵌套情况合并成一个NestedInteger的list。当栈弹空时，表示第一个左括号已经被弹出，即整个NestedInteger完结，此时可以直接返回结果，否则就需要将合并后的结果再次压入栈中。

3、遇到逗号时，表示当前NestedInteger的list中产生了新的一项，若其为数字，同样需要将其添加到NestedInteger中，若其不是数字（例如\[\[\],\[\]\]这种情况中的逗号），那么无事发生。

另外，需要注意样例一这样的特殊情况。此时只会得到一个数字，那么在最后返回即可。

题目中虽然没说，但是数字也可能出现负数，因此还需要维护一个符号标记。

最后附上python代码：

```python
# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger(object):
#    def __init__(self, value=None):
#        """
#        If value is not specified, initializes an empty list.
#        Otherwise initializes a single integer equal to value.
#        """
#
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
#        """
#
#    def add(self, elem):
#        """
#        Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
#        :rtype void
#        """
#
#    def setInteger(self, value):
#        """
#        Set this NestedInteger to hold a single integer equal to value.
#        :rtype void
#        """
#
#    def getInteger(self):
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        :rtype int
#        """
#
#    def getList(self):
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        :rtype List[NestedInteger]
#        """
class Solution(object):
    def deserialize(self, s):
        """
        :type s: str
        :rtype: NestedInteger
        """

        stack = []
        now = None
        sign = 1

        for char in s:
            if char == '[':
                stack.append(NestedInteger())

            elif ord(char) >= 48 and ord(char) <= 57:
                if now is None:
                    now = int(char)
                else:
                    now = now * 10 + int(char)

            elif char == ',':
                if now is not None:
                    stack[-1].add(NestedInteger(sign * now))
                now = None
                sign = 1

            elif char == '-':
                sign = -1

            elif char == ']':
                if now is not None:
                    stack[-1].add(NestedInteger(sign * now))
                tmp = stack.pop()
                if not stack:
                    return tmp
                else:
                    stack[-1].add(tmp)
                now = None
                sign = 1

        return NestedInteger(sign * now)
```
