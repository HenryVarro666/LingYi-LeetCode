---
title: "1631. 最小体力消耗路径"
aliases: ["yiduobo的每日leetcode 1631.最小体力消耗路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/437826666"
zhihu_id: "437826666"
zhihu_title: "yiduobo的每日leetcode 1631.最小体力消耗路径"
question_id: "1631"
question: "最小体力消耗路径"
problem_url: "https://leetcode.cn/problems/path-with-minimum-effort/"
created: "2021-11-25T23:09:19+08:00"
updated: "2021-11-25T23:09:19+08:00"
upvotes: 1
comments: 0
---

# 1631. 最小体力消耗路径

> **[yiduobo的每日leetcode 1631.最小体力消耗路径](https://zhuanlan.zhihu.com/p/437826666) · 知乎 · 2021-11-25 · 赞同 1**
> 力扣：[1631. 最小体力消耗路径](https://leetcode.cn/problems/path-with-minimum-effort/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1631.最小体力消耗路径

[力扣](https://leetcode-cn.com/problems/path-with-minimum-effort/)

由于题目中的最小体力消耗指的是路径上所有边消耗的最大值，那么可以明确的一点是，当最小体力消耗越大时，每个点能走的相邻点就越多，换言之就是越有可能从起点走到终点。

那么一个自然的想法就是直接二分答案，然后从起点开始进行bfs，并根据能否走到终点来调整二分的边界。

当然，由于这里路径的权重都非负，且满足三角形不等式，那么在这里使用dijkstra算法也是可行的。由于题目边的规模是O(mn)的，因此使用dijkstra的时间复杂度应该比二分答案的时间复杂度稍微好点。

最后附上python代码，我在这里采用的是二分答案的做法：

```python
class Solution(object):
    def minimumEffortPath(self, heights):
        """
        :type heights: List[List[int]]
        :rtype: int
        """

        l = 0
        r = 1000000
        m = len(heights)
        n = len(heights[0])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            mid = (l + r) >> 1
            q = [(0, 0)]
            used = set([(0, 0)])
            head = 0
            tail = 1
            while head < tail:
                nowx, nowy = q[head]
                head += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and abs(heights[x][y] - heights[nowx][nowy]) <= mid and (x, y) not in used:
                        q.append((x, y))
                        used.add((x, y))
                        tail += 1
            
            if (m - 1, n - 1) in used:
                r = mid
            else:
                l = mid + 1
        
        return l
```
