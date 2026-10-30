---
title: "630. 课程表III"
aliases: ["yiduobo的每日leetcode 630.课程表III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270456461"
zhihu_id: "270456461"
zhihu_title: "yiduobo的每日leetcode 630.课程表III"
question_id: "630"
question: "课程表 III"
problem_url: "https://leetcode.cn/problems/course-schedule-iii/"
difficulty: "Hard"
rating: 2000
created: "2020-10-31T00:21:44+08:00"
updated: "2020-10-31T00:21:44+08:00"
upvotes: 0
comments: 0
---

# 630. 课程表III

> **[yiduobo的每日leetcode 630.课程表III](https://zhuanlan.zhihu.com/p/270456461) · 知乎 · 2020-10-31 · 赞同 0**
> 力扣：[630. 课程表 III](https://leetcode.cn/problems/course-schedule-iii/) · Hard · 灵茶山艾府：[贪心还能反悔？（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

630.课程表III<https://leetcode-cn.com/problems/course-schedule-iii/>

题目里面没有规定课程必须的起始时间，而每门课程的重要程度也是一致的，那么对于任意两门课程，如果可以同时选择，我们就应该优先学习截止时间较早的。如果不能同时选择，那么我们就应该选择耗费时间较少的。

于是我们可以先按照截止时间从小到大进行排序，然后一趟扫描，若当前的课程可以学习，那么就学习当前课程。若当前课程无法学习，我们就从已经学习的课程中找出耗费时间最多的那一门课程，若这门课程的耗时比当前课程要多，那么我们可以放弃耗时较多的这门课程，转而学习当前课程。这里有一个隐藏条件就是，若已学习的课程耗时为t1，截止时间为d1，当前课程耗时为t2，截止时间为t2，若t1 > t2，由于此时必然有d1 \<\= d2，因此我们可以利用原本t1的时间来学习t2的课程，此时的结束时间必然小于d1，因此也必然小于d2，即若耗时最多的课程耗时大于当前课程的耗时，那么必然是可以使用当前课程替代耗时最多的课程的。

在这个过程中，需要维护已学习课程的最大耗时，因此可以使用堆来储存已学习课程的耗时。

最后附上python代码：

```python
import heapq

class Solution(object):
    def scheduleCourse(self, courses):
        """
        :type courses: List[List[int]]
        :rtype: int
        """

        courses = sorted(courses, key=lambda d:d[1])
        heap = []
        now = 0
        res = 0
        for course in courses:
            t, d = course
            if now + t <= d:
                heapq.heappush(heap, -t)
                now += t
                res += 1
            elif heap:
                max_t = -heapq.heappop(heap)
                if max_t > t:
                    now -= max_t - t
                    heapq.heappush(heap, -t)
                else:
                    heapq.heappush(heap, -max_t)

        return res
```
