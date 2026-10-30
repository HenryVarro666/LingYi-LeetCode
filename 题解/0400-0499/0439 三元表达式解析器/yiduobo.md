---
title: "439. 三元表达式解析器"
aliases: ["yiduobo的每日leetcode 439.三元表达式解析器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599770048"
zhihu_id: "599770048"
zhihu_title: "yiduobo的每日leetcode 439.三元表达式解析器"
question_id: "439"
question: "三元表达式解析器"
problem_url: "https://leetcode.cn/problems/ternary-expression-parser/"
created: "2023-01-17T23:26:59+08:00"
updated: "2023-01-17T23:26:59+08:00"
upvotes: 0
comments: 0
---

# 439. 三元表达式解析器

> **[yiduobo的每日leetcode 439.三元表达式解析器](https://zhuanlan.zhihu.com/p/599770048) · 知乎 · 2023-01-17 · 赞同 0**
> 力扣：[439. 三元表达式解析器](https://leetcode.cn/problems/ternary-expression-parser/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

439.三元表达式解析器

[力扣](https://leetcode.cn/problems/ternary-expression-parser/)

从头开始解析这个表达式，使用一个遍历p记录当前解析的下标。可以发现，一个表达式只有可能以单个值，或者a?b:c的形式出现。

对于单个数值的情况，可以是T、F或者单个数字，也就是expression[p]为数值，或者expression[p]为T或F，且expression[p + 1]不是问号。这种情况下，直接返回expression[p]就行了。

另一种情况则是a?b:c的形式，这里的expression[p]为T或者F，同时expression[p + 1]必须是问号。接下来，若expression[p]为T，那么答案就相当于b的解析结果，否则就相当于c的解析结果。

对于前者，只需将p移动到p + 2就行了。

对于后者，则需要将p移动到其对应的冒号后方。在这里需要注意的是，对应的冒号可能处于非常后面的位置，因为可能存在表达式的嵌套。在这里可以使用类似于括号匹配的处理方法，为expression[p + 1]这个位置上的问号寻找其对应的冒号。

最后附上python代码：

```python
class Solution(object):
    def parseTernary(self, expression):
        """
        :type expression: str
        :rtype: str
        """

        p = 0
        n = len(expression)
        while True:
            if expression[p] == 'T':
                if p + 1 < n and expression[p + 1] == '?':
                    p += 2
                else:
                    return 'T'
            elif expression[p] == 'F':
                if p + 1 < n and expression[p + 1] == '?':
                    cnt = 0
                    p += 2
                    while p + 1 < n:
                        if cnt == 0 and expression[p + 1] == ':':
                            break
                        p += 1
                        if expression[p] == '?':
                            cnt += 1
                        elif expression[p] == ':':
                            cnt -= 1
                    p += 2
                else:
                    return 'F'
            else:
                return expression[p]
```
