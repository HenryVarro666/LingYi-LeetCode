---
title: "210. 课程表II"
aliases: ["yiduobo的每日leetcode 210.课程表II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147368613"
zhihu_id: "147368613"
zhihu_title: "yiduobo的每日leetcode 210.课程表II"
question_id: "210"
question: "课程表II"
problem_url: "https://leetcode.cn/problems/course-schedule-ii/"
created: "2020-06-10T22:40:28+08:00"
updated: "2020-06-10T22:40:28+08:00"
upvotes: 0
comments: 0
---

# 210. 课程表II

> **[yiduobo的每日leetcode 210.课程表II](https://zhuanlan.zhihu.com/p/147368613) · 知乎 · 2020-06-10 · 赞同 0**
> 力扣：[210. 课程表II](https://leetcode.cn/problems/course-schedule-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

210.课程表II <https://leetcode-cn.com/problems/course-schedule-ii/>

207题的升级版（传送门在这里[yiduobo：yiduobo的每日leetcode 207.课程表](https://zhuanlan.zhihu.com/p/147047752)），虽然是升级版，但是也只是要输出具体的课程顺序，实际上在使用bfs实现拓扑排序的过程中，bfs的队列就是一种可行的课程顺序。于是执行一次拓扑排序，输出bfs的队列即可。

最后附上python代码：

```python
class Solution(object):
    def findOrder(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: List[int]
        """

        if numCourses == 0:
            return 0

        g = [[] for _ in range(numCourses)]
        ind = [0] * numCourses
        for lesson, pre_lesson in prerequisites:
            g[pre_lesson].append(lesson)
            ind[lesson] += 1

        q = [index for index in range(numCourses) if ind[index] == 0]
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next_lesson in g[now]:
                ind[next_lesson] -= 1
                if ind[next_lesson] == 0:
                    q.append(next_lesson)
                    r += 1
        
        if len(q) == numCourses:
            return q
        else:
            return []
```
