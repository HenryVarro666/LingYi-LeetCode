---
title: "678. 有效的括号字符串"
aliases: ["yiduobo的每日leetcode 678.有效的括号字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/300100190"
zhihu_id: "300100190"
zhihu_title: "yiduobo的每日leetcode 678.有效的括号字符串"
question_id: "678"
question: "有效的括号字符串"
problem_url: "https://leetcode.cn/problems/valid-parenthesis-string/"
created: "2020-11-18T23:16:53+08:00"
updated: "2020-11-18T23:16:53+08:00"
upvotes: 1
comments: 0
---

# 678. 有效的括号字符串

> **[yiduobo的每日leetcode 678.有效的括号字符串](https://zhuanlan.zhihu.com/p/300100190) · 知乎 · 2020-11-18 · 赞同 1**
> 力扣：[678. 有效的括号字符串](https://leetcode.cn/problems/valid-parenthesis-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

678.有效的括号字符串

[力扣](https://leetcode-cn.com/problems/valid-parenthesis-string/)

经典的括号匹配问题，不过这里多出了星号可以代表左括号、右括号或者空字符。

我们首先回忆没有星号的时候的做法：使用一个变量cnt记录当前左括号的数量，从左往右一趟扫描，若遇到左括号则cnt加一，否则cnt减一。若过程中cnt小于0，那么就无法匹配。若扫描完成后cnt不等于0，那么也无法匹配。

到了这里，由于星号的不确定性，我们可以使用两个变量max和min来记录当前最多可能有多少个左括号，以及最少可能有多少个左括号。那么对于当前字符char：

1、若char为'('：

此时max +\= 1，min +\= 1

2、若char为')'：

此时max -\= 1，min -\= 1。

若max小于0，说明即使之前的星号全部变成左括号，左括号的数量还是不够，因此可以直接返回false。

若max大于等于0，而min小于0，说明此时我们必须调整之前某个星号，从而使得不出现右括号数量大于左括号数量的情况。

3、若char为'\*'：

此时max +\= 1，min -\= 1。

若min小于0，则同样将其置为0。

在扫描完成后，若此时的min不为0，说明右括号的数量不足，返回false，否则返回true。

需要注意的是，这里的min不为0并不意味着所有的星号都变成了右括号。例如 \*)( 这种情况，其中\*为了适配右括号，必须变成左括号，因此max和min的变化过程分别为

max：1 -> 0 -> 1

min：0 -> 0 -> 1

最终的min不为0，意味着右括号数量不足。

最后附上python代码：

```python
class Solution(object):
    def checkValidString(self, s):
        """
        :type s: str
        :rtype: bool
        """

        ma = mi = 0
        for char in s:
            if char == '(':
                ma += 1
                mi += 1
            elif char == ')':
                ma -= 1
                mi -= 1
                if mi < 0:
                    mi = 0
            else:
                ma += 1
                mi -= 1
                if mi < 0:
                    mi = 0
            
            if ma < 0:
                return False

        if mi > 0:
            return False

        return True
```
