---
title: "1462. 课程表IV"
aliases: ["yiduobo的每日leetcode 1462.课程表IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412923786"
zhihu_id: "412923786"
zhihu_title: "yiduobo的每日leetcode 1462.课程表IV"
question_id: "1462"
question: "课程表IV"
problem_url: "https://leetcode.cn/problems/course-schedule-iv/"
created: "2021-09-22T23:44:03+08:00"
updated: "2021-09-22T23:44:03+08:00"
upvotes: 0
comments: 0
---

# 1462. 课程表IV

> **[yiduobo的每日leetcode 1462.课程表IV](https://zhuanlan.zhihu.com/p/412923786) · 知乎 · 2021-09-22 · 赞同 0**
> 力扣：[1462. 课程表IV](https://leetcode.cn/problems/course-schedule-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1462.课程表IV

[力扣](https://leetcode-cn.com/problems/course-schedule-iv/)

最标准的拓扑排序问题，使用f[x]表示课程x的所有前置课程，接下来执行拓扑排序。对于课程x，若其有直接的后置课程y，那么在处理到课程x时，需要将y的入度减去1，此时也可以顺便使用f[y]来更新f[x]。

拓扑排序完成后，对于每个query通过f检测是否具有前置关系即可。

最后附上python代码：

```python
class Solution(object):
    def checkIfPrerequisite(self, numCourses, prerequisites, queries):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        g = {}
        ind = [0] * numCourses
        for x, y in prerequisites:
            if x not in g:
                g[x] = set()
            g[x].add(y)
            ind[y] += 1
        
        q = []
        f = [set() for _ in range(numCourses)]
        for index in range(numCourses):
            if ind[index] == 0:
                q.append(index)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                f[next] |= f[now]
                f[next].add(now)
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return [x in f[y] for x, y in queries]
```
