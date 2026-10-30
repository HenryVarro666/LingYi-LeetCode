---
title: "2533. 好二进制字符串的数量"
aliases: ["yiduobo的每日leetcode 2533.好二进制字符串的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637171265"
zhihu_id: "637171265"
zhihu_title: "yiduobo的每日leetcode 2533.好二进制字符串的数量"
question_id: "2533"
question: "好二进制字符串的数量"
problem_url: "https://leetcode.cn/problems/number-of-good-binary-strings/"
created: "2023-06-15T01:05:13+08:00"
updated: "2023-06-15T01:05:13+08:00"
upvotes: 0
comments: 0
---

# 2533. 好二进制字符串的数量

> **[yiduobo的每日leetcode 2533.好二进制字符串的数量](https://zhuanlan.zhihu.com/p/637171265) · 知乎 · 2023-06-15 · 赞同 0**
> 力扣：[2533. 好二进制字符串的数量](https://leetcode.cn/problems/number-of-good-binary-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2533.好二进制字符串的数量

[力扣](https://leetcode.cn/problems/number-of-good-binary-strings/)

动态规划的题目。令f[i]表示长度为i的好字符串数目。初始状况下有f[0] \= 1，接下来对于i > 0：

1、若i >\= oneGroup，那么就可以将这个字符串的最后oneGroup个字符设置为1，因此就有f[i] +\= f[i - oneGroup]

2、若i >\= zeroGroup，那么就可以将这个字符串的最后zeroGroup个字符设置为0，因此就有f[i] +\= f[i - zeroGroup]

一趟遍历，计算完f[1]到f[maxLength]后，将f[minLength]到f[maxLength]累加起来即为最终答案。

最后附上python代码：

```
class Solution(object):
    def goodBinaryStrings(self, minLength, maxLength, oneGroup, zeroGroup):
        """
        :type minLength: int
        :type maxLength: int
        :type oneGroup: int
        :type zeroGroup: int
        :rtype: int
        """

        f = [0] * (maxLength + 1)
        f[0] = 1
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, maxLength + 1):
            if index >= oneGroup:
                f[index] += f[index - oneGroup]
                if f[index] >= mod:
                    f[index] -= mod
            
            if index >= zeroGroup:
                f[index] += f[index - zeroGroup]
                if f[index] >= mod:
                    f[index] -= mod
            
            if index >= minLength:
                res += f[index]
                if res >= mod:
                    res -= mod
        
        return res
```
