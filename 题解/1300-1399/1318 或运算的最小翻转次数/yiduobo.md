---
title: "1318. 或运算的最小翻转次数"
aliases: ["yiduobo的每日leetcode 1318.或运算的最小翻转次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/393198226"
zhihu_id: "393198226"
zhihu_title: "yiduobo的每日leetcode 1318.或运算的最小翻转次数"
question_id: "1318"
question: "或运算的最小翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-flips-to-make-a-or-b-equal-to-c/"
created: "2021-07-26T12:14:52+08:00"
updated: "2021-07-26T12:14:52+08:00"
upvotes: 1
comments: 0
---

# 1318. 或运算的最小翻转次数

> **[yiduobo的每日leetcode 1318.或运算的最小翻转次数](https://zhuanlan.zhihu.com/p/393198226) · 知乎 · 2021-07-26 · 赞同 1**
> 力扣：[1318. 或运算的最小翻转次数](https://leetcode.cn/problems/minimum-flips-to-make-a-or-b-equal-to-c/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1318.或运算的最小翻转次数

[力扣](https://leetcode-cn.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/)

由于题目中是或运算，因此对于c中的某一位，其结果就取决于a和b中对应位置的值，更具体的来说，对于c中的某一位：

1、若该位为0，那么a和b中对应的位必须为0

2、若该位为1，那么a和b中对应的位至少有一个为1

根据以上两点，我们可以从低位开始向高位扫描，每次考察c中当前位的值。

若c当前位为1，且a和b对应的位都为0，那么需要一次操作，将a或b中对应的位变为1。

若c当前位为0，若a对应的位为1，需要一次操作；若b对应的位为1，需要一次操作。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, a, b, c):
        """
        :type a: int
        :type b: int
        :type c: int
        :rtype: int
        """

        res = 0
        while a or b or c:
            if c % 2 == 1:
                if a % 2 == 0 and b % 2 == 0:
                    res += 1
            else:
                if a % 2 == 1:
                    res += 1
                if b % 2 == 1:
                    res += 1
            
            a /= 2
            b /= 2
            c /= 2
        
        return res
```
