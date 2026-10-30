---
title: "778. 水位上升的泳池中游泳"
aliases: ["yiduobo的每日leetcode 778.水位上升的泳池中游泳"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-search", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/二分算法", "题单/常用数据结构", "题单/网格图", "题单/图论算法", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/七-并查集", "题单/网格图/五-综合应用", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340226722"
zhihu_id: "340226722"
zhihu_title: "yiduobo的每日leetcode 778.水位上升的泳池中游泳"
question_id: "778"
question: "水位上升的泳池中游泳"
problem_url: "https://leetcode.cn/problems/swim-in-rising-water/"
difficulty: "Hard"
rating: 2097
created: "2020-12-28T22:53:11+08:00"
updated: "2020-12-28T22:53:11+08:00"
upvotes: 0
comments: 0
---

# 778. 水位上升的泳池中游泳

> **[yiduobo的每日leetcode 778.水位上升的泳池中游泳](https://zhuanlan.zhihu.com/p/340226722) · 知乎 · 2020-12-28 · 赞同 0**
> 力扣：[778. 水位上升的泳池中游泳](https://leetcode.cn/problems/swim-in-rising-water/) · Hard · 灵茶山艾府：[两种方法：二分答案 / Dijkstra 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

778.水位上升的泳池中游泳

[力扣](https://leetcode-cn.com/problems/swim-in-rising-water/)

如果把格子两两之间使用有向边相连，以终点的水位作为有向边的权重，问题应该是可以转化成某种另类的最短路径问题，不过这里的最短是路径上最大权重边最小。

想想还是有点复杂，所以我用的是另一种做法。

一个很自然的想法就是从最低的高度开始往上枚举高度，然后通过bfs检测当前枚举到的高度能否从起点到达终点。如果可以，那么当前高度就是最终答案，否则继续向上枚举。

不过，这里的高度可能很高，所以整体的时间复杂度无法接受，但是注意到高度越高就越有可能使得起点和终点连通，换言之，这里的高度满足二分的性质，于是可以先记录所有格子中最高和最低的高度，然后二分最终答案的高度并通过bfs检测，这样一来，总体的时间复杂度就降下来了。

bfs的过程平平无奇，就是经典的从当前格子往上下左右四个方向尝试游动。

最后附上python代码：

```python
class Solution(object):
    def swimInWater(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        max_h = 0
        for i in range(m):
            for j in range(n):
                max_h = max(max_h, grid[i][j])
        min_h = max(grid[0][0], grid[-1][-1])

        used = [[None] * n for _ in range(m)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while min_h < max_h:
            mid = (min_h + max_h) >> 1
            q = [[0, 0]]
            used[0][0] = mid
            l = 0
            r = 1
            while l < r:
                nowx, nowy = q[l]
                l += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] <= mid and used[x][y] != mid:
                        q.append([x, y])
                        used[x][y] = mid
                        r += 1

            if used[m - 1][n - 1] == mid:
                max_h = mid
            else:
                min_h = mid + 1
            
        return min_h
```
