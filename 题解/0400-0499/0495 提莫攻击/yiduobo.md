---
title: "495. 提莫攻击"
aliases: ["yiduobo的每日leetcode 495.提莫攻击"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/256370565"
zhihu_id: "256370565"
zhihu_title: "yiduobo的每日leetcode 495.提莫攻击"
question_id: "495"
question: "提莫攻击"
problem_url: "https://leetcode.cn/problems/teemo-attacking/"
created: "2020-09-20T18:31:50+08:00"
updated: "2020-09-20T18:31:50+08:00"
upvotes: 1
comments: 0
---

# 495. 提莫攻击

> **[yiduobo的每日leetcode 495.提莫攻击](https://zhuanlan.zhihu.com/p/256370565) · 知乎 · 2020-09-20 · 赞同 1**
> 力扣：[495. 提莫攻击](https://leetcode.cn/problems/teemo-attacking/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

495.提莫攻击<https://leetcode-cn.com/problems/teemo-attacking/>

看着题目描述花里胡哨的，但是实际上就是区间合并的问题，而且这里区间已经天然按左边界排好序了，于是只需要一趟扫描，判断当前区间的左边界是否在上一个区间的右边界内。如果是，那么合并当前区间与上一个区间，将区间右边界置为当前区间的右边界。如果不是，那么计算上一个区间的长度，将其累加到答案中，同时当前区间就成为新的上一个区间。

另外，不要忘记在扫描完成之后最后这个区间的长度也需要计算进去。

最后附上python代码：

```python
class Solution(object):
    def findPoisonedDuration(self, timeSeries, duration):
        """
        :type timeSeries: List[int]
        :type duration: int
        :rtype: int
        """

        if not timeSeries:
            return 0

        res = 0
        start = timeSeries[0]
        now = timeSeries[0] + duration - 1
        for time in timeSeries[1:]:
            if now < time:
                res += now - start + 1
                start = time
            now = time + duration - 1

        return res + now - start + 1
```
