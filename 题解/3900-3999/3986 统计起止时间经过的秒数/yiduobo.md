---
title: "3986. 统计起止时间经过的秒数"
aliases: ["yiduobo的每日leetcode 3986.统计起止时间经过的秒数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2059684499861116137"
zhihu_id: "2059684499861116137"
zhihu_title: "yiduobo的每日leetcode 3986.统计起止时间经过的秒数"
question_id: "3986"
question: "统计起止时间经过的秒数"
problem_url: "https://leetcode.cn/problems/number-of-elapsed-seconds-between-two-times/"
difficulty: "Easy"
created: "2026-07-12T17:07:32+08:00"
updated: "2026-07-12T17:07:33+08:00"
upvotes: 2
comments: 0
---

# 3986. 统计起止时间经过的秒数

> **[yiduobo的每日leetcode 3986.统计起止时间经过的秒数](https://zhuanlan.zhihu.com/p/2059684499861116137) · 知乎 · 2026-07-12 · 赞同 2**
> 力扣：[3986. 统计起止时间经过的秒数](https://leetcode.cn/problems/number-of-elapsed-seconds-between-two-times/) · Easy · 灵茶山艾府：[解析时分秒（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3986.统计起止时间经过的秒数

<https://leetcode.cn/problems/number-of-elapsed-seconds-between-two-times/description/>

题目给出两个有效时间startTime和endTime，均以字符串形式表示，格式为"HH:MM:SS"。保证endTime不早于startTime。

要求返回startTime到endTime经过的秒数，包含两个端点。

对于startTime和endTime，先将小时、分钟、秒数分离出来，然后计算出这个时间是当天的第几秒，最后将二者相减即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def secondsBetweenTimes(self, startTime, endTime):
        """
        :type startTime: str
        :type endTime: str
        :rtype: int
        """
        
        def calc(t):
            h, m, s = t.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)

        return calc(endTime) - calc(startTime)
```
