---
title: "1118. 一月有多少天"
aliases: ["yiduobo的每日leetcode 1118.一月有多少天"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609597727"
zhihu_id: "609597727"
zhihu_title: "yiduobo的每日leetcode 1118.一月有多少天"
question_id: "1118"
question: "一月有多少天"
problem_url: "https://leetcode.cn/problems/number-of-days-in-a-month/"
created: "2023-02-26T17:38:56+08:00"
updated: "2023-02-26T17:38:56+08:00"
upvotes: 0
comments: 0
---

# 1118. 一月有多少天

> **[yiduobo的每日leetcode 1118.一月有多少天](https://zhuanlan.zhihu.com/p/609597727) · 知乎 · 2023-02-26 · 赞同 0**
> 力扣：[1118. 一月有多少天](https://leetcode.cn/problems/number-of-days-in-a-month/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1118.一月有多少天

[力扣](https://leetcode.cn/problems/number-of-days-in-a-month/)

比较基础的题目，注意不要遗漏了闰年二月的情况。

最后附上python代码：

```python
class Solution(object):
    def numberOfDays(self, year, month):
        """
        :type year: int
        :type month: int
        :rtype: int
        """

        d = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        res = d[month]
        if month == 2 and (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)):
            res += 1
        return res
```
