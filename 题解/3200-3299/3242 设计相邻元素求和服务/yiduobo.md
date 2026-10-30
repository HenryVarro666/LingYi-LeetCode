---
title: "3242. 设计相邻元素求和服务"
aliases: ["yiduobo的每日leetcode 3242.设计相邻元素求和服务"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721007879"
zhihu_id: "721007879"
zhihu_title: "yiduobo的每日leetcode 3242.设计相邻元素求和服务"
question_id: "3242"
question: "设计相邻元素求和服务"
problem_url: "https://leetcode.cn/problems/design-neighbor-sum-service/"
difficulty: "Easy"
created: "2024-09-20T00:32:58+08:00"
updated: "2024-09-20T00:32:58+08:00"
upvotes: 1
comments: 0
---

# 3242. 设计相邻元素求和服务

> **[yiduobo的每日leetcode 3242.设计相邻元素求和服务](https://zhuanlan.zhihu.com/p/721007879) · 知乎 · 2024-09-20 · 赞同 1**
> 力扣：[3242. 设计相邻元素求和服务](https://leetcode.cn/problems/design-neighbor-sum-service/) · Easy · 灵茶山艾府：[预处理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3242.设计相邻元素求和服务

[. - 力扣（LeetCode）](https://leetcode.cn/problems/design-neighbor-sum-service/description/)

题目给出一个大小为n \* n的二维矩阵grid，其中包含了0到n^2 - 1之间的不同元素。

接下来要求实现neighborSum类，要求adjacentSum(value)以及diagonalSum(value)两个方法。其中adjacentSum用来计算在元素value左侧、右侧、上方、下方四个相邻元素之和，而diagonalSum则用来计算在元素value左上、右上、左下、右下四个相邻元素之和。

题目要求实现的两个方法都是基于元素值value的，且需要计算的都是value相邻的元素，因此需要能高效定位到value，也就是说需要使用一个哈希表记录每个元素值所在的坐标。

另一方面，为了避免多次求解同一个value带来的复杂度，可以使用另外两个哈希表分别用来缓存value在水平竖直方向上以及对角线方向上相邻元素之和。若一开始哈希表中没有对应的value，那么就先找到value在矩阵中的位置，然后计算相邻元素之和，否则直接返回哈希表中对应的值即可。

最后附上python代码：

```python
class NeighborSum(object):

    def __init__(self, grid):
        """
        :type grid: List[List[int]]
        """
        n = len(grid)
        self.n = n
        self.pos = [[] for _ in range(n * n)]
        self.grid = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.grid[i].append(grid[i][j])
                self.pos[grid[i][j]] = (i, j)
        self.adj_sum = [None] * (n * n)
        self.diag_sum = [None] * (n * n)

    def calc(self, x, y, t):
        if t == 0:
            dx = [0, 1, 0, -1]
            dy = [1, 0, -1, 0]
        else:
            dx = [-1, -1, 1, 1]
            dy = [-1, 1, -1, 1]
        
        s = 0
        for d in range(4):
            xx = x + dx[d]
            yy = y + dy[d]
            if 0 <= xx < self.n and 0 <= yy < self.n:
                s += self.grid[xx][yy]
        
        return s

    def adjacentSum(self, value):
        """
        :type value: int
        :rtype: int
        """
        if self.adj_sum[value] is None:
            x, y = self.pos[value]
            self.adj_sum[value] = self.calc(x, y, 0)
        
        return self.adj_sum[value]

    def diagonalSum(self, value):
        """
        :type value: int
        :rtype: int
        """
        
        if self.diag_sum[value] is None:
            x, y = self.pos[value]
            self.diag_sum[value] = self.calc(x, y, 1)
        
        return self.diag_sum[value]

# Your NeighborSum object will be instantiated and called as such:
# obj = NeighborSum(grid)
# param_1 = obj.adjacentSum(value)
# param_2 = obj.diagonalSum(value)
```
