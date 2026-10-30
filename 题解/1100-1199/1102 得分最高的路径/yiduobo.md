---
title: "1102. 得分最高的路径"
aliases: ["yiduobo的每日leetcode 1102.得分最高的路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609595752"
zhihu_id: "609595752"
zhihu_title: "yiduobo的每日leetcode 1102.得分最高的路径"
question_id: "1102"
question: "得分最高的路径"
problem_url: "https://leetcode.cn/problems/path-with-maximum-minimum-value/"
created: "2023-02-26T17:37:39+08:00"
updated: "2023-02-26T17:37:39+08:00"
upvotes: 0
comments: 0
---

# 1102. 得分最高的路径

> **[yiduobo的每日leetcode 1102.得分最高的路径](https://zhuanlan.zhihu.com/p/609595752) · 知乎 · 2023-02-26 · 赞同 0**
> 力扣：[1102. 得分最高的路径](https://leetcode.cn/problems/path-with-maximum-minimum-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1102.得分最高的路径

[力扣](https://leetcode.cn/problems/path-with-maximum-minimum-value/)

乍一看感觉是传统的动态规划，不过在这里使用贪心法应该也可以。具体来首，就是每一轮都选择当前可以到达的未访问过，且分数最高的节点，使用该节点的分数更新答案。重复此过程直到某一时刻到达右下角的节点为止。对于这个做法正确性的简单证明，可以针对某一轮分数最高的未访问节点(x, y)进行讨论：

1、若最终的路径经过了(x, y)，那么当前这一轮选择(x, y)是没有任何问题的

2、若最终的路径没有经过(x, y)，那么在当前这一轮就必然经过了其他未访问过的节点。而(x, y)是当前这一轮节点值最大的，因此最终答案必然小于等于(x, y)的值，因此在当前这一轮选择(x, y)并不会影响到最终结果

根据上面的结论，就可以使用一个堆来维护当前的未访问节点，每次选择堆顶节点进行访问，使用该节点的值更新最终答案，同时将该节点相邻的且未访问过的节点加入到堆中。重复此过程直到访问过了右下角节点为止。

最后附上python代码：

```python
class Solution(object):
    def maximumMinimumPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        heap = [[-grid[0][0], 0, 0]]
        res = grid[0][0]
        vis = set()
        while m * n - 1 not in vis:
            d, nowx, nowy = heapq.heappop(heap)
            if nowx * n + nowy not in vis:
                vis.add(nowx * n + nowy)
                res = min(res, -d)
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if 0 <= x < m and 0 <= y < n and x * n + y not in vis:
                        heapq.heappush(heap, [-grid[x][y], x, y])
        
        return res
```
