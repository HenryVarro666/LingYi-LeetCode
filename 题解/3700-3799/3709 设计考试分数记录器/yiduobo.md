---
title: "3709. 设计考试分数记录器"
aliases: ["yiduobo的每日leetcode 3709.设计考试分数记录器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961185964048232832"
zhihu_id: "1961185964048232832"
zhihu_title: "yiduobo的每日leetcode 3709.设计考试分数记录器"
question_id: "3709"
question: "设计考试分数记录器"
problem_url: "https://leetcode.cn/problems/design-exam-scores-tracker/"
difficulty: "Medium"
rating: 1648
created: "2025-10-13T21:56:39+08:00"
updated: "2025-10-13T21:56:43+08:00"
upvotes: 1
comments: 0
---

# 3709. 设计考试分数记录器

> **[yiduobo的每日leetcode 3709.设计考试分数记录器](https://zhuanlan.zhihu.com/p/1961185964048232832) · 知乎 · 2025-10-13 · 赞同 1**
> 力扣：[3709. 设计考试分数记录器](https://leetcode.cn/problems/design-exam-scores-tracker/) · Medium · 灵茶山艾府：[前缀和 + 二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3709.设计考试分数记录器

[3709. 设计考试分数记录器 - 力扣（LeetCode）](https://leetcode.cn/problems/design-exam-scores-tracker/description/)

题目要求实现一个ExamTracker类，用来记录考试分数，并计算特定时间段内的分数总和。

这个类支持两种操作，分别为

record(time, score)：表示在时间time参加了一次考试，分数为score

totalScore(startTime, endTime)：返回startTime到endTime之间参加的所有考试的分数之和，若时间区间内没有参加任何考试，则返回0

题目保证record的调用按照time递增，同时所有totalScore都满足startTime \<\= endTime \<\= t，其中t是最近这次record中对应的时间time

题目实际上是区间和问题，将其转化为前缀和就能轻松解决。需要注意的是，由于本题是在线的，因此需要先对查询的起始和终止时间在record记录的时间序列中二分，得到区间的起点和终点，然后再使用前缀和之差计算对应的区间和。

最后附上python代码：

```python
class ExamTracker(object):

    def __init__(self):
        self.s = [(0, 0)]

    def record(self, time, score):
        """
        :type time: int
        :type score: int
        :rtype: None
        """
        self.s.append((time, self.s[-1][1] + score))

    def get(self, t):
        left = 0
        right = len(self.s) - 1
        while left < right:
            mid = (left + right + 1) // 2
            if self.s[mid][0] > t:
                right = mid - 1
            else:
                left = mid
        
        return self.s[left][1]

    def totalScore(self, startTime, endTime):
        """
        :type startTime: int
        :type endTime: int
        :rtype: int
        """
        
        return self.get(endTime) - self.get(startTime - 1)

# Your ExamTracker object will be instantiated and called as such:
# obj = ExamTracker()
# obj.record(time,score)
# param_2 = obj.totalScore(startTime,endTime)
```
