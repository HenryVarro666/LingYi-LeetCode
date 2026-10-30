---
title: "1056. 易混淆数"
aliases: ["yiduobo的每日leetcode 1056.易混淆数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607024109"
zhihu_id: "607024109"
zhihu_title: "yiduobo的每日leetcode 1056.易混淆数"
question_id: "1056"
question: "易混淆数"
problem_url: "https://leetcode.cn/problems/confusing-number/"
created: "2023-02-17T01:22:11+08:00"
updated: "2023-02-17T01:22:11+08:00"
upvotes: 0
comments: 0
---

# 1056. 易混淆数

> **[yiduobo的每日leetcode 1056.易混淆数](https://zhuanlan.zhihu.com/p/607024109) · 知乎 · 2023-02-17 · 赞同 0**
> 力扣：[1056. 易混淆数](https://leetcode.cn/problems/confusing-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1056.易混淆数

[力扣](https://leetcode.cn/problems/confusing-number/)

从最低位开始逐位分离n的数位，并将这个数位翻转后加入到新的数当中。若期间出现了无法翻转的情况，直接返回false。若顺利得到了新的数，则需要对比新数与原数是否相同，若不同则返回true否则返回false。

最后附上python代码：

```python
class Solution(object):
    def confusingNumber(self, n):
        """
        :type n: int
        :rtype: bool
        """

        r = 0

        same = set([0, 1, 8])
        invalid = set([2, 3, 4, 5, 7])

        tmp = n
        while tmp:
            digit = tmp % 10
            tmp /= 10
            if digit in invalid:
                return False
            
            if digit in same:
                r = r * 10 + digit
            else:
                r = r * 10 + 15 - digit

        return r != n
```
