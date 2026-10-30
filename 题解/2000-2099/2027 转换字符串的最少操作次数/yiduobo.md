---
title: "2027. 转换字符串的最少操作次数"
aliases: ["yiduobo的每日leetcode 2027.转换字符串的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/string", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/507867746"
zhihu_id: "507867746"
zhihu_title: "yiduobo的每日leetcode 2027.转换字符串的最少操作次数"
question_id: "2027"
question: "转换字符串的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-convert-string/"
difficulty: "Easy"
rating: 1346
created: "2022-04-30T21:51:38+08:00"
updated: "2022-04-30T21:51:38+08:00"
upvotes: 0
comments: 0
---

# 2027. 转换字符串的最少操作次数

> **[yiduobo的每日leetcode 2027.转换字符串的最少操作次数](https://zhuanlan.zhihu.com/p/507867746) · 知乎 · 2022-04-30 · 赞同 0**
> 力扣：[2027. 转换字符串的最少操作次数](https://leetcode.cn/problems/minimum-moves-to-convert-string/) · Easy · 灵茶山艾府：[贪心模拟 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2027.转换字符串的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-moves-to-convert-string/)

首先，对于当前字符串中最左侧的X，必须执行一次操作。为了使得这次操作尽可能惠及到后面的位置，那么现在应该将从该位置开始的三个字符变为O。于是可以一趟遍历，若当前字符为X，那么更新答案，并将遍历的位置向后移动三位，若不为X，那么答案不变，然后将遍历的位置向后移动一位。

最后附上python代码：

```python
class Solution(object):
    def minimumMoves(self, s):
        """
        :type s: str
        :rtype: int
        """

        p = 0
        res = 0
        while p < len(s):
            if s[p] == 'X':
                res += 1
                p += 3
            else:
                p += 1
        
        return res
```
