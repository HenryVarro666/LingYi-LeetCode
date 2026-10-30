---
title: "3938. 矩阵中最大共享路径和"
aliases: ["yiduobo的每日leetcode 3938.矩阵中最大共享路径和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043447267814794098"
zhihu_id: "2043447267814794098"
zhihu_title: "yiduobo的每日leetcode 3938.矩阵中最大共享路径和"
question_id: "3938"
question: "矩阵中最大共享路径和"
problem_url: "https://leetcode.cn/problems/maximum-path-intersection-sum-in-a-grid/"
difficulty: "Medium"
rating: 2252
created: "2026-05-28T21:59:11+08:00"
updated: "2026-05-28T21:59:17+08:00"
upvotes: 1
comments: 0
---

# 3938. 矩阵中最大共享路径和

> **[yiduobo的每日leetcode 3938.矩阵中最大共享路径和](https://zhuanlan.zhihu.com/p/2043447267814794098) · 知乎 · 2026-05-28 · 赞同 1**
> 力扣：[3938. 矩阵中最大共享路径和](https://leetcode.cn/problems/maximum-path-intersection-sum-in-a-grid/) · Medium · 灵茶山艾府：[最大子数组和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3938.矩阵中最大共享矩阵和

<https://leetcode.cn/problems/maximum-path-intersection-sum-in-a-grid/description/>

题目给出一个m \* n的整数矩阵grid。

两个玩家在矩阵中移动：

- 玩家1从左上角单元格(0, 0)出发，只能向右或者向下移动。他的目的地是右下角单元格(m - 1, n - 1)。
- 玩家2从左下角单元格(m - 1, 0)出发，只能向右或者向上移动。他的目的地是右上角单元格(0, n - 1)。

每个玩家都必须选择一条从各自起始单元格到目的地的有效路径。

如果一个单元格属于两条被选中的路径，则称该单元格为共享单元格。问所有共享单元格的值的最大可能总和。

首先可以明确的是，由于两个玩家的行进路径是两条交叉的折线，这也就意味着至多只会有一段路径重叠在一起。换言之，在这里只需要计算每一行和每一列中的最大子段和就行了。

不过以样例2来看，有一些特例，即处于最外层的子段长度必须大于等于2。对于这些特例，可以从图论的方面来帮助理解。

对于处于四条边且不处于角上的单元格，其度数总共为3，而两条路径都是一进一出，因此当某个单元式共享单元格时，两条路径必然会共享某个度，也就是共享这个方向上的相邻单元格，因此包含这些单元格上的子段长度必须大于等于2。

对于处于四个角上的单元格，这些单元格分别作为两条路径的起点和终点，因此两条路径如果在此交汇，至少需要3个度，但是这些单元格的度数为2，因此包含这些单元格的子段长度同样必须大于等于2。

最后对于其他的单元格，度数都为4，因此可以在容纳两条路径的进出不共享其他单元格。

基于上面的结论，就可以先遍历每一行和每一列，计算出这些行列上长度大于等于2的最大子段和来更新答案，然后再遍历所有非边界单元格，使用这些单元格的值更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        res = None
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if res is None or res < grid[i][j]:
                    res = grid[i][j]
        
        def calc(nums):
            ma = None
            now = nums[0]
            for v in nums[1:]:
                now += v
                if ma is None or ma < now:
                    ma = now
                if now < v:
                    now = v
            
            return ma

        for i in range(m):
            ma = calc(grid[i])
            if res is None or res < ma:
                res = ma
        
        for j in range(n):
            nums = [grid[i][j] for i in range(m)]
            ma = calc(nums)
            if res is None or res < ma:
                res = ma
        
        return res
```
