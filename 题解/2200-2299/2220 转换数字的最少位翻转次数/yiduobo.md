---
title: "2220. 转换数字的最少位翻转次数"
aliases: ["yiduobo的每日leetcode 2220.转换数字的最少位翻转次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542196086"
zhihu_id: "542196086"
zhihu_title: "yiduobo的每日leetcode 2220.转换数字的最少位翻转次数"
question_id: "2220"
question: "转换数字的最少位翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-bit-flips-to-convert-number/"
difficulty: "Easy"
rating: 1282
created: "2022-07-15T23:53:33+08:00"
updated: "2022-07-15T23:53:33+08:00"
upvotes: 0
comments: 0
---

# 2220. 转换数字的最少位翻转次数

> **[yiduobo的每日leetcode 2220.转换数字的最少位翻转次数](https://zhuanlan.zhihu.com/p/542196086) · 知乎 · 2022-07-15 · 赞同 0**
> 力扣：[2220. 转换数字的最少位翻转次数](https://leetcode.cn/problems/minimum-bit-flips-to-convert-number/) · Easy · 灵茶山艾府：[一行（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2220.转换数字的最少位翻转次数

[力扣](https://leetcode.cn/problems/minimum-bit-flips-to-convert-number/)

由于每次只能翻转一位，那么实际上就是问start和goal不同的位有多少，那么可以将二者异或，再计算异或结果中1的数目。

最后附上python代码：

```python
class Solution(object):
    def minBitFlips(self, start, goal):
        """
        :type start: int
        :type goal: int
        :rtype: int
        """

        res = 0
        diff = start ^ goal
        while diff:
            res += 1
            diff -= diff & -diff
        
        return res
```
