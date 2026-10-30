---
title: "263. 丑数"
aliases: ["yiduobo的每日leetcode 263.丑数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/151431946"
zhihu_id: "151431946"
zhihu_title: "yiduobo的每日leetcode 263.丑数"
question_id: "263"
question: "丑数"
problem_url: "https://leetcode.cn/problems/ugly-number/"
difficulty: "Easy"
created: "2020-06-28T22:39:31+08:00"
updated: "2020-06-28T22:39:31+08:00"
upvotes: 0
comments: 0
---

# 263. 丑数

> **[yiduobo的每日leetcode 263.丑数](https://zhuanlan.zhihu.com/p/151431946) · 知乎 · 2020-06-28 · 赞同 0**
> 力扣：[263. 丑数](https://leetcode.cn/problems/ugly-number/) · Easy · 灵茶山艾府：[利用位运算优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

263.丑数<https://leetcode-cn.com/problems/ugly-number/>

比较基础的题目。首先当num小于等于0时，其一定不是丑数。否则就对num不断除上2、3、5，如果除剩下来的数不为1，那么就不是丑数，否则就是丑数。

最后附上python代码：

```python
class Solution(object):
    def isUgly(self, num):
        """
        :type num: int
        :rtype: bool
        """

        if num <= 0:
            return False

        while num % 2 == 0:
            num /= 2
        while num % 3 == 0:
            num /= 3
        while num % 5 == 0:
            num /= 5

        return num == 1
```
