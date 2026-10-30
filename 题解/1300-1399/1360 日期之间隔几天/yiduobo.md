---
title: "1360. 日期之间隔几天"
aliases: ["yiduobo的每日leetcode 1360.日期之间隔几天"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399221127"
zhihu_id: "399221127"
zhihu_title: "yiduobo的每日leetcode 1360.日期之间隔几天"
question_id: "1360"
question: "日期之间隔几天"
problem_url: "https://leetcode.cn/problems/number-of-days-between-two-dates/"
created: "2021-08-12T23:14:37+08:00"
updated: "2021-08-12T23:14:37+08:00"
upvotes: 1
comments: 0
---

# 1360. 日期之间隔几天

> **[yiduobo的每日leetcode 1360.日期之间隔几天](https://zhuanlan.zhihu.com/p/399221127) · 知乎 · 2021-08-12 · 赞同 1**
> 力扣：[1360. 日期之间隔几天](https://leetcode.cn/problems/number-of-days-between-two-dates/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1360.日期之间隔几天

[力扣](https://leetcode-cn.com/problems/number-of-days-between-two-dates/)

经典的计算日期题。注意到题目给出的两个日期都大于1971年1月1日，因此我选择分别计算两个日期到1971年1月1日的间隔日期数目，然后相减得出答案。

注意闰月日期的计算。

最后附上python代码：

```python
class Solution(object):
    def daysBetweenDates(self, date1, date2):
        """
        :type date1: str
        :type date2: str
        :rtype: int
        """

        return abs(self.get_cnt(date1) - self.get_cnt(date2))
    
    def get_cnt(self, date):
        year, month, day = [int(x) for x in date.split('-')]
        cnt = 0
        for y in range(1971, year):
            cnt += 365
            if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
                cnt += 1
        
        m_cnt = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            m_cnt[2] += 1
        
        for m in range(1, month):
            cnt += m_cnt[m]
        
        cnt += day
        return cnt
```
