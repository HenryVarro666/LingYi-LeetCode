---
title: "2503. 矩阵查询可获得的最大分数"
aliases: ["yiduobo的每日leetcode 2503.矩阵查询可获得的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/七-并查集", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634307933"
zhihu_id: "634307933"
zhihu_title: "yiduobo的每日leetcode 2503.矩阵查询可获得的最大分数"
question_id: "2503"
question: "矩阵查询可获得的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-points-from-grid-queries/"
difficulty: "Hard"
rating: 2196
created: "2023-06-03T00:08:33+08:00"
updated: "2023-06-03T00:08:33+08:00"
upvotes: 0
comments: 0
---

# 2503. 矩阵查询可获得的最大分数

> **[yiduobo的每日leetcode 2503.矩阵查询可获得的最大分数](https://zhuanlan.zhihu.com/p/634307933) · 知乎 · 2023-06-03 · 赞同 0**
> 力扣：[2503. 矩阵查询可获得的最大分数](https://leetcode.cn/problems/maximum-number-of-points-from-grid-queries/) · Hard · 灵茶山艾府：[两种写法：离线询问 + 并查集 / 最小堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2503.矩阵查询可获得的最大分数

[力扣](https://leetcode.cn/problems/maximum-number-of-points-from-grid-queries/)

题目要求对于queries数组中的每个询问都queries[i]，都求出从(0, 0)开始，只经过数值不超过queries[i]的可到达位置的数量。由于数据规模比较大，因此直接枚举每个queries[i]然后进行bfs显然是不行，必须进行优化。

对于两个询问queries[i]以及queries[j]，不妨设queries[i] \< queries[j]，那么对于前一个询问，其可到达的位置必然就是对于后一个询问的子集。有了这个结论，就可以利用这种类似单调性的性质，将queries从小到大进行排序逐个求解，每次都在上一个询问的前提下继续往外扩展。

具体实现上，随着queries的逐渐增大，每一轮都需要将当前连通块的边界上所有值小于这个最新的queries[i]的位置加入到连同分量中，此时就还需要使用一个堆来维护这些还未到达的位置的数值，这样才能高效地找出每一轮新扩展的节点。

最后附上python代码：

```python
class Solution(object):
    def maxPoints(self, grid, queries):
        """
        :type grid: List[List[int]]
        :type queries: List[int]
        :rtype: List[int]
        """

        heap = [[grid[0][0], 0, 0]]
        cnt = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        m = len(grid)
        n = len(grid[0])
        vis = [[False] * n for _ in range(m)]
        res = [0] * len(queries)

        for threshold, index in sorted(zip(queries, range(len(queries)))):
            while heap and heap[0][0] < threshold:
                v, nowx, nowy = heapq.heappop(heap)
                if not vis[nowx][nowy]:
                    vis[nowx][nowy] = True
                    cnt += 1
                    for d in range(4):
                        x = nowx + dx[d]
                        y = nowy + dy[d]
                        if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                            heapq.heappush(heap, [grid[x][y], x, y])
            
            res[index] = cnt

        
        return res
```
