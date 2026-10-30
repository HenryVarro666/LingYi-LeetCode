---
title: "2050. 并行课程III"
aliases: ["yiduobo的每日leetcode 2050.并行课程III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/topological-sort", "leetcode/dynamic-programming", "leetcode/bfs", "leetcode/graph-theory", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/图论算法", "题单/动态规划/十三-图-DP", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/511859020"
zhihu_id: "511859020"
zhihu_title: "yiduobo的每日leetcode 2050.并行课程III"
question_id: "2050"
question: "并行课程 III"
problem_url: "https://leetcode.cn/problems/parallel-courses-iii/"
difficulty: "Hard"
rating: 2084
created: "2022-05-10T00:24:45+08:00"
updated: "2022-05-10T00:24:46+08:00"
upvotes: 0
comments: 0
---

# 2050. 并行课程III

> **[yiduobo的每日leetcode 2050.并行课程III](https://zhuanlan.zhihu.com/p/511859020) · 知乎 · 2022-05-10 · 赞同 0**
> 力扣：[2050. 并行课程 III](https://leetcode.cn/problems/parallel-courses-iii/) · Hard · 灵茶山艾府：[拓扑排序+动态规划（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2050.并行课程III

[力扣](https://leetcode.cn/problems/parallel-courses-iii/)

非常标准的根据拓扑序进行动态规划的问题。

题目的样例已经给出了建图的方案，即从前置课程引出一条有向边指向后置课程。为了方便进行拓扑排序，需要使用一个数组ind统计每个课程的入度，在本题中就是有多少门前置课程。

在完成了建图以及ind的统计后，可以令f[now]表示完成课程now的最早时间，接下来选出所有入度为0的课程。由于这部分课程不需要前置课程可以直接开始学习，因此完成这些课程的最早时间就是其对应需要学习的时间，即使用对应的time去更新f。除此之外，还需要将这些课程加入到拓扑排序的队列中，准备开始进行拓扑排序。

对于当前处理的课程now，遍历其所有的后置课程next。

对于每个next，首先使用f[next] \= max(f[next], f[now])来更新f[next]，表示在开始学习next之前必须先等待now完成学习。另一方面，需要将ind[next]减去1，表示已经考虑过now对next的影响了。在某一次减一时ind[next]将等于0，此时说明已经考虑过next所有的前置课程了，之后可以开始学习next，因此需要将f[next]再加上time[next]，得到next学习完成的时间，同时将next加入到拓扑排序的队列中以继续更新后续课程的学习时间。

拓扑排序完成后，f中的最大值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, n, relations, time):
        """
        :type n: int
        :type relations: List[List[int]]
        :type time: List[int]
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
        
        f = {}
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
                f[index] = time[index]
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in f:
                    f[next] = f[now]
                else:
                    f[next] = max(f[next], f[now])

                ind[next] -= 1
                if ind[next] == 0:
                    f[next] += time[next]
                    q.append(next)
                    r += 1
        
        return max(f.values())
```
