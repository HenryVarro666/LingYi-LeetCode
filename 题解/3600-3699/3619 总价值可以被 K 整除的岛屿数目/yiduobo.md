---
title: "3619. 总价值可以被K整除的岛屿数目"
aliases: ["yiduobo的每日leetcode 3619.总价值可以被K整除的岛屿数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944164478653559878"
zhihu_id: "1944164478653559878"
zhihu_title: "yiduobo的每日leetcode 3619.总价值可以被K整除的岛屿数目"
question_id: "3619"
question: "总价值可以被 K 整除的岛屿数目"
problem_url: "https://leetcode.cn/problems/count-islands-with-total-value-divisible-by-k/"
difficulty: "Medium"
rating: 1461
created: "2025-08-27T22:33:16+08:00"
updated: "2025-08-27T22:33:16+08:00"
upvotes: 1
comments: 0
---

# 3619. 总价值可以被K整除的岛屿数目

> **[yiduobo的每日leetcode 3619.总价值可以被K整除的岛屿数目](https://zhuanlan.zhihu.com/p/1944164478653559878) · 知乎 · 2025-08-27 · 赞同 1**
> 力扣：[3619. 总价值可以被 K 整除的岛屿数目](https://leetcode.cn/problems/count-islands-with-total-value-divisible-by-k/) · Medium · 灵茶山艾府：[网格图 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3619.总价值可以被K整除的岛屿数目

[3619. 总价值可以被 K 整除的岛屿数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-islands-with-total-value-divisible-by-k/description/)

题目给出一个m \* n的矩阵grid以及一个正整数k，一个岛屿指的是有正整数(表示陆地)组成的，且陆地间四周连通。一个岛屿的总价值是该岛屿中所有单元格的值之和，问总价值可以被k整除的岛屿数量。

找岛屿相关的问题，可以直接照搬之前200题的处理方法，利用floodfill来寻找矩阵中的岛屿。

[yiduobo的每日leetcode 200.岛屿数量](https://zhuanlan.zhihu.com/p/146198826)

对于本题，同样是利用floodfill找出矩阵中的所有岛屿，在这个过程中顺便计算岛屿的总价值，然后判断其是否可以被k整除即可。

最后附上python代码：

```python
class Solution(object):
    def countIslands(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        res = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    s = grid[i][j]
                    grid[i][j] = 0
                    q = [(i, j)]
                    head, tail = 0, 1
                    while head < tail:
                        for x, y in q[head : tail]:
                            for d in range(4):
                                xx = x + dx[d]
                                yy = y + dy[d]
                                if 0 <= xx < m and 0 <= yy < n and grid[xx][yy] > 0:
                                    s += grid[xx][yy]
                                    grid[xx][yy] = 0
                                    q.append((xx, yy))
                        
                        head, tail = tail, len(q)
                    
                    if s % k == 0:
                        res += 1
        
        return res
```
