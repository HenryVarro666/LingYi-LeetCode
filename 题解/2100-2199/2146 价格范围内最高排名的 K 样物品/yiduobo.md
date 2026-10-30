---
title: "2146. 价格范围内最高排名的K样物品"
aliases: ["yiduobo的每日leetcode 2146.价格范围内最高排名的K样物品"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/queue", "leetcode/sorting", "leetcode/bfs", "题单/网格图", "题单/网格图/二-网格图-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/529866677"
zhihu_id: "529866677"
zhihu_title: "yiduobo的每日leetcode 2146.价格范围内最高排名的K样物品"
question_id: "2146"
question: "价格范围内最高排名的 K 样物品"
problem_url: "https://leetcode.cn/problems/k-highest-ranked-items-within-a-price-range/"
difficulty: "Medium"
rating: 1837
created: "2022-06-16T22:05:32+08:00"
updated: "2022-06-16T22:05:32+08:00"
upvotes: 0
comments: 0
---

# 2146. 价格范围内最高排名的K样物品

> **[yiduobo的每日leetcode 2146.价格范围内最高排名的K样物品](https://zhuanlan.zhihu.com/p/529866677) · 知乎 · 2022-06-16 · 赞同 0**
> 力扣：[2146. 价格范围内最高排名的 K 样物品](https://leetcode.cn/problems/k-highest-ranked-items-within-a-price-range/) · Medium · 灵茶山艾府：[分层 BFS 的同时排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2146.价格范围内最高排名的K样物品

[力扣](https://leetcode.cn/problems/k-highest-ranked-items-within-a-price-range/)

题目要求从距离、价格、行坐标和列坐标四个角度来评价一个物品，在这里后面三样都是直接可以拿到的，那么为了得到距离，就需要从start开始进行一次bfs，找出从start开始到达每样物品的距离。

在bfs的过程中，每接触到一样价格在范围内的物品，就将其按距离、价格、行坐标、列坐标的顺序打包加入到候选答案中。bfs完成后，将候选答案按四个关键字从小到达进行排序，然后取top k就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def highestRankedKItems(self, grid, pricing, start, k):
        """
        :type grid: List[List[int]]
        :type pricing: List[int]
        :type start: List[int]
        :type k: int
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])

        q = [start]
        used = set([start[0] * n + start[1]])
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        step = 0
        candidate = []

        l = 0
        r = 1
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                if grid[nowx][nowy] >= pricing[0] and grid[nowx][nowy] <= pricing[1]:
                    candidate.append([step, grid[nowx][nowy], nowx, nowy])
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] > 0 and x * n + y not in used:
                        q.append([x, y])
                        used.add(x * n + y)
            
            l, r = r, len(q)
        
        return [[x, y] for _, _, x, y in sorted(candidate)[:k]]
```
