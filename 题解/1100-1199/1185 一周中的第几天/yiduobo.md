---
title: "1185. 一周中的第几天"
aliases: ["yiduobo的每日leetcode 1185.一周中的第几天"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/api"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380210045"
zhihu_id: "380210045"
zhihu_title: "yiduobo的每日leetcode 1185.一周中的第几天"
question_id: "1185"
question: "一周中的第几天"
problem_url: "https://leetcode.cn/problems/day-of-the-week/"
difficulty: "Easy"
created: "2021-06-12T18:26:23+08:00"
updated: "2021-06-12T18:26:23+08:00"
upvotes: 0
comments: 0
---

# 1185. 一周中的第几天

> **[yiduobo的每日leetcode 1185.一周中的第几天](https://zhuanlan.zhihu.com/p/380210045) · 知乎 · 2021-06-12 · 赞同 0**
> 力扣：[1185. 一周中的第几天](https://leetcode.cn/problems/day-of-the-week/) · Easy · 灵茶山艾府：[各种语言的库函数写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1185.一周中的第几天

[力扣](https://leetcode-cn.com/problems/day-of-the-week/)

比较基础的题目，注意判断闰年的情况即可。另外，查日历可知1997年的元旦是星期五。

最后附上python代码：

```python
class Solution(object):
    def dayOfTheWeek(self, day, month, year):
        """
        :type day: int
        :type month: int
        :type year: int
        :rtype: str
        """

        date = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        d = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        num = 4
        for y in range(1971, year):
            num += 365
            if y % 400 == 0 or (y % 100 != 0 and y % 4 == 0):
                num += 1
        
        if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
            d[1] += 1

        for m in range(1, month):
            num += d[m - 1]
        
        num += day - 1

        num %= 7

        return date[num]
```
