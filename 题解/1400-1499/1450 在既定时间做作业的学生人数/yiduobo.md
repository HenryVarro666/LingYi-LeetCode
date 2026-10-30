---
title: "1450. 在既定时间做作业的学生人数"
aliases: ["yiduobo的每日leetcode 1450.在既定时间做作业的学生人数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411552857"
zhihu_id: "411552857"
zhihu_title: "yiduobo的每日leetcode 1450.在既定时间做作业的学生人数"
question_id: "1450"
question: "在既定时间做作业的学生人数"
problem_url: "https://leetcode.cn/problems/number-of-students-doing-homework-at-a-given-time/"
difficulty: "Easy"
created: "2021-09-17T22:46:32+08:00"
updated: "2021-09-17T22:46:32+08:00"
upvotes: 0
comments: 0
---

# 1450. 在既定时间做作业的学生人数

> **[yiduobo的每日leetcode 1450.在既定时间做作业的学生人数](https://zhuanlan.zhihu.com/p/411552857) · 知乎 · 2021-09-17 · 赞同 0**
> 力扣：[1450. 在既定时间做作业的学生人数](https://leetcode.cn/problems/number-of-students-doing-homework-at-a-given-time/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1450.在既定时间做作业的学生人数

[力扣](https://leetcode-cn.com/problems/number-of-students-doing-homework-at-a-given-time/)

比较基础的题目，直接一趟扫描，对于当前学生判断queryTime是否处于其起始和结束时间之内即可。

最后附上python代码：

```python
class Solution(object):
    def busyStudent(self, startTime, endTime, queryTime):
        """
        :type startTime: List[int]
        :type endTime: List[int]
        :type queryTime: int
        :rtype: int
        """

        n = len(startTime)
        res = 0
        for index in range(n):
            if queryTime >= startTime[index] and queryTime <= endTime[index]:
                res += 1
        
        return res
```
