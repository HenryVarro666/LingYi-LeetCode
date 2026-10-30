---
title: "1136. 并行课程"
aliases: ["yiduobo的每日leetcode 1136.并行课程"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610558953"
zhihu_id: "610558953"
zhihu_title: "yiduobo的每日leetcode 1136.并行课程"
question_id: "1136"
question: "并行课程"
problem_url: "https://leetcode.cn/problems/parallel-courses/"
created: "2023-03-01T21:42:12+08:00"
updated: "2023-03-01T21:42:12+08:00"
upvotes: 0
comments: 0
---

# 1136. 并行课程

> **[yiduobo的每日leetcode 1136.并行课程](https://zhuanlan.zhihu.com/p/610558953) · 知乎 · 2023-03-01 · 赞同 0**
> 力扣：[1136. 并行课程](https://leetcode.cn/problems/parallel-courses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1136.并行课程

[力扣](https://leetcode.cn/problems/parallel-courses/)

非常标准的拓扑排序问题。

首先建图。将所有的课程视为有向图中节点，课程的依赖关系视为有向图中的边，建图的过程中顺便统计有向图中节点的入度。

接下来，从所有入度为0的节点开始进行拓扑排序。入度为0意味着这部分课程没有前置依赖，可以一上来就学习。在拓扑排序的过程中，枚举当前课程的所有下游课程，并将其对应的入度减去1。若某一课程的入度被减到0时，说明该课程的所有前置课程已经学习完毕，那么就可以将该课程加入到拓扑排序的队列中。

拓扑排序完成后，若完成学习的课程数目，也就是拓扑排序队列的长度等于n，说明可以学习完所有的课程，此时拓扑排序的轮次就是最终答案。反之，说明课程间存在环无法全部学习，应该返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumSemesters(self, n, relations):
        """
        :type n: int
        :type relations: List[List[int]]
        :rtype: int
        """

        ind = [0] * n
        g = {}

        for x, y in relations:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = set()
            
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
        
        head, tail = 0, len(q)
        res = 0
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
            
            head, tail = tail, len(q)
        
        if len(q) == n:
            return res
        
        return -1
```
