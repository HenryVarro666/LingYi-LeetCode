---
title: "1904. 你完成的完整对局数"
aliases: ["yiduobo的每日leetcode 1904.你完成的完整对局数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/481623761"
zhihu_id: "481623761"
zhihu_title: "yiduobo的每日leetcode 1904.你完成的完整对局数"
question_id: "1904"
question: "你完成的完整对局数"
problem_url: "https://leetcode.cn/problems/the-number-of-full-rounds-you-have-played/"
difficulty: "Medium"
created: "2022-03-15T23:50:17+08:00"
updated: "2022-03-15T23:50:17+08:00"
upvotes: 0
comments: 0
---

# 1904. 你完成的完整对局数

> **[yiduobo的每日leetcode 1904.你完成的完整对局数](https://zhuanlan.zhihu.com/p/481623761) · 知乎 · 2022-03-15 · 赞同 0**
> 力扣：[1904. 你完成的完整对局数](https://leetcode.cn/problems/the-number-of-full-rounds-you-have-played/) · Medium · 灵茶山艾府：[简洁写法，避免计算出 -1](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1904.你完成的完整对局数

[力扣](https://leetcode-cn.com/problems/the-number-of-full-rounds-you-have-played/)

为了统一单位，首先应该将小时转化为分钟。

接下来则有两种情况，若起始时间小于结束时间，那么就是在同一天内的起始时间到结束时间，否则就是起始时间到第二天零点，在加上第二天零点到结束时间。

具体计算上，由于题目要求的是按15分钟整来计算，那么起始时间就应该除以15向上取整，而结束时间则应该除以15向下取整。如果使用这种计算方式，有一个需要特别注意的地方是当出现起始时和结束时间在同一个十五分钟内，且两个时间都没有踩上整15分钟的点的话，此时的答案就应该为0，但是如果直接向上向下取整来算的话，会得到-1这样奇怪的答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfRounds(self, loginTime, logoutTime):
        """
        :type loginTime: str
        :type logoutTime: str
        :rtype: int
        """

        login_hour, login_minute = loginTime.split(':')
        start = int(login_hour) * 60 + int(login_minute)
        logout_hour, logout_minute = logoutTime.split(':')
        end = int(logout_hour) * 60 + int(logout_minute)
        if start <= end:
            return self.calc(start, end)
        else:
            return self.calc(start, 1440) + self.calc(0, end)
    
    def calc(self, start, end):
        if start % 15 != 0:
            start = start / 15 * 15 + 15
        end = end / 15 * 15
        return max(0, (end - start) / 15)
```
