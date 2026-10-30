---
title: "207. 课程表"
aliases: ["yiduobo的每日leetcode 207.课程表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "题单/图论算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/图论算法/一-图的遍历", "题单/LeetCode-热题-100/图论", "题单/面试经典-150-题/图"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147047752"
zhihu_id: "147047752"
zhihu_title: "yiduobo的每日leetcode 207.课程表"
question_id: "207"
question: "课程表"
problem_url: "https://leetcode.cn/problems/course-schedule/"
difficulty: "Medium"
created: "2020-06-09T21:52:13+08:00"
updated: "2020-06-09T21:52:13+08:00"
upvotes: 0
comments: 0
---

# 207. 课程表

> **[yiduobo的每日leetcode 207.课程表](https://zhuanlan.zhihu.com/p/147047752) · 知乎 · 2020-06-09 · 赞同 0**
> 力扣：[207. 课程表](https://leetcode.cn/problems/course-schedule/) · Medium · 灵茶山艾府：[DFS 三色标记法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

207.课程表<https://leetcode-cn.com/problems/course-schedule/>

图论中的拓扑排序问题。

首先想办法构图。如果想学习课程A，必须先学习课程B，那么加入一条B到A的边。这样一来，所有的课程关系就能构成一张有向图，同时我们可以记录下来每门课程当前有多少条边指向进来，这个在图论中称为入度。

接下来，将所有入度为0，即不需要前置课程的点加入到队列中，开始进行bfs。设当前遍历到了课程now，接下来遍历从now出发的每一条边，将边另一端的入度减一。若某个点的入度减到了0，说明这门课程的前置课程已经被遍历完，可以开始学习了，因此将这个点加入到bfs的队列尾即可。

若可以bfs完整个图，那么说明可以完成所有课程的学习，否则就不能。

最后附上python代码，其中ind代表入度：

```python
class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """

        g = {index : [] for index in range(numCourses)}
        ind = [0] * numCourses

        for pre_lesson, now in prerequisites:
            ind[now] += 1
            g[pre_lesson].append(now)

        q = [index for index, x in enumerate(ind) if x == 0]
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

        return r == numCourses
```
