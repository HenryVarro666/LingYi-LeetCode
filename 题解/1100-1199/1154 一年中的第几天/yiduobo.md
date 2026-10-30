---
title: "1154. 一年中的第几天"
aliases: ["yiduobo的每日leetcode 1154.一年中的第几天"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378052158"
zhihu_id: "378052158"
zhihu_title: "yiduobo的每日leetcode 1154.一年中的第几天"
question_id: "1154"
question: "一年中的第几天"
problem_url: "https://leetcode.cn/problems/day-of-the-year/"
difficulty: "Easy"
created: "2021-06-05T00:09:20+08:00"
updated: "2021-06-05T00:09:20+08:00"
upvotes: 0
comments: 0
---

# 1154. 一年中的第几天

> **[yiduobo的每日leetcode 1154.一年中的第几天](https://zhuanlan.zhihu.com/p/378052158) · 知乎 · 2021-06-05 · 赞同 0**
> 力扣：[1154. 一年中的第几天](https://leetcode.cn/problems/day-of-the-year/) · Easy · 灵茶山艾府：[各种语言的库函数写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1154.一年中的第几天

[力扣](https://leetcode-cn.com/problems/day-of-the-year/)

比较基础的题目，需要特别注意闰年2月的天数。

最后附上python代码：

```python
class Solution(object):
    def dayOfYear(self, date):
        """
        :type date: str
        :rtype: int
        """

        days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
        y, m, d = date.split('-')
        y = int(y)
        if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
            days[2] += 1
        
        return sum(days[:int(m)]) + int(d)
```
