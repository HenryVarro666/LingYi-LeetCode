---
title: "415. 字符串相加"
aliases: ["yiduobo的每日leetcode 415.字符串相加"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/190262567"
zhihu_id: "190262567"
zhihu_title: "yiduobo的每日leetcode 415.字符串相加"
question_id: "415"
question: "字符串相加"
problem_url: "https://leetcode.cn/problems/add-strings/"
created: "2020-08-19T23:47:41+08:00"
updated: "2020-08-19T23:47:41+08:00"
upvotes: 0
comments: 0
---

# 415. 字符串相加

> **[yiduobo的每日leetcode 415.字符串相加](https://zhuanlan.zhihu.com/p/190262567) · 知乎 · 2020-08-19 · 赞同 0**
> 力扣：[415. 字符串相加](https://leetcode.cn/problems/add-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

415.字符串相加<https://leetcode-cn.com/problems/add-strings/>

经典的高精度加法问题，从低到高位逐位执行加法即可。过程中需要注意维护进位的情况。

最后附上python代码：

```python
class Solution(object):
    def addStrings(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """

        l1 = len(num1)
        l2 = len(num2)

        x = 0
        res = []
        for index in range(max(l1, l2)):
            if index < l1:
                x += int(num1[l1 - index - 1])
            if index < l2:
                x += int(num2[l2 - index - 1])
            if x >= 10:
                res.append(x - 10)
                x = 1
            else:
                res.append(x)
                x = 0

        if x:
            res.append(x)

        res.reverse()
        return ''.join([str(x) for x in res])
```
