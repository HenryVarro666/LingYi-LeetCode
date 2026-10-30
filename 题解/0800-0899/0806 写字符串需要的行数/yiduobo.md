---
title: "806. 写字符串需要的行数"
aliases: ["yiduobo的每日leetcode 806.写字符串需要的行数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343235936"
zhihu_id: "343235936"
zhihu_title: "yiduobo的每日leetcode 806.写字符串需要的行数"
question_id: "806"
question: "写字符串需要的行数"
problem_url: "https://leetcode.cn/problems/number-of-lines-to-write-string/"
created: "2021-01-10T16:11:43+08:00"
updated: "2021-01-10T16:11:43+08:00"
upvotes: 0
comments: 0
---

# 806. 写字符串需要的行数

> **[yiduobo的每日leetcode 806.写字符串需要的行数](https://zhuanlan.zhihu.com/p/343235936) · 知乎 · 2021-01-10 · 赞同 0**
> 力扣：[806. 写字符串需要的行数](https://leetcode.cn/problems/number-of-lines-to-write-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

806.写字符串需要的行数

[力扣](https://leetcode-cn.com/problems/number-of-lines-to-write-string/)

直接按照题目设定来模拟计算，使用一个变量now来记录当前行已经使用的宽度。对于当前字符，先获取其宽度width，若now + width \<\= 100，那么就将该字符写在当前行，同时将now加上width，否则另起一行开始写并设置now为width。

最后附上python代码：

```python
class Solution(object):
    def numberOfLines(self, widths, s):
        """
        :type widths: List[int]
        :type s: str
        :rtype: List[int]
        """

        now = 0
        line = 1
        for char in s:
            width = widths[ord(char) - 97]
            if now + width <= 100:
                now += width
            else:
                line += 1
                now = width
        
        return [line, now]
```
