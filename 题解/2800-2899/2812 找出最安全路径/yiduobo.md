---
title: "2812. 找出最安全路径"
aliases: ["yiduobo的每日leetcode 2812.找出最安全路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/union-find", "题单/二分算法", "题单/常用数据结构", "题单/网格图", "题单/二分算法/二-二分答案", "题单/常用数据结构/七-并查集", "题单/网格图/二-网格图-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658179304"
zhihu_id: "658179304"
zhihu_title: "yiduobo的每日leetcode 2812.找出最安全路径"
question_id: "2812"
question: "找出最安全路径"
problem_url: "https://leetcode.cn/problems/find-the-safest-path-in-a-grid/"
difficulty: "Medium"
rating: 2154
created: "2023-09-25T05:11:50+08:00"
updated: "2023-09-25T05:11:50+08:00"
upvotes: 1
comments: 0
---

# 2812. 找出最安全路径

> **[yiduobo的每日leetcode 2812.找出最安全路径](https://zhuanlan.zhihu.com/p/658179304) · 知乎 · 2023-09-25 · 赞同 1**
> 力扣：[2812. 找出最安全路径](https://leetcode.cn/problems/find-the-safest-path-in-a-grid/) · Medium · 灵茶山艾府：[接近 O(n^2) 的做法：多源BFS+倒序枚举答案+并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2812.找出最安全路径

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-safest-path-in-a-grid/)

越安全的路径越难找，那么在这里就可以通过二分最终的安全系数，然后判断是否存在一条所有单元格的安全系数都大于等于mid的路径。

对于单个单元格而言，其安全系数是离该单元格最近的小偷到该单元格的距离，那么就可以先从所有小偷开始进行一次bfs，计算出每个单元格到达最近的小偷的距离。

接下来开始二分答案。二分的下界自然是0，而上界则是(0, 0)和(m - 1, n - 1)这两个位置安全系数的较小值，这样就能保证对于任意二分到的安全系数，起点和终点都是合法的。对于当前二分到的安全系数mid，从(0, 0)开始通过bfs寻找一条到达(m - 1, n - 1)的路径，这里有一个限制条件就是目标单元格的安全系数必然大于等于mid。若存在一条这样一条路径，也就是路径上的单元格安全系数都大于等于mid，那么就调整二分下界为mid，否则调整二分上界为mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maximumSafenessFactor(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        thief_dis = [[None] * n for _ in range(m)]

        q = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    q.append([i, j])
                    thief_dis[i][j] = 0
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and thief_dis[x][y] is None:
                        thief_dis[x][y] = thief_dis[nowx][nowy] + 1
                        q.append([x, y])
            
            head, tail = tail, len(q)
        

        left = 0
        right = min(thief_dis[0][0], thief_dis[m - 1][n - 1])
        while left < right:
            mid = (left + right + 1) / 2
            q = [[0, 0]]
            vis = [[False] * n for _ in range(m)]
            head, tail = 0, 1
            while head < tail:
                nowx, nowy = q[head]
                head += 1
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and thief_dis[x][y] >= mid and not vis[x][y]:
                        vis[x][y] = True
                        q.append([x, y])
                        tail += 1
                
                if vis[m - 1][n - 1]:
                    break
            
            if vis[m - 1][n - 1]:
                left = mid
            else:
                right = mid - 1
        
        return left
```
