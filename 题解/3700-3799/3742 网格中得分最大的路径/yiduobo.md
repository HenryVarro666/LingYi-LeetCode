---
title: "3742. 网格中得分最大的路径"
aliases: ["yiduobo的每日leetcode 3742.网格中得分最大的路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1970891866921740113"
zhihu_id: "1970891866921740113"
zhihu_title: "yiduobo的每日leetcode 3742.网格中得分最大的路径"
question_id: "3742"
question: "网格中得分最大的路径"
problem_url: "https://leetcode.cn/problems/maximum-path-score-in-a-grid/"
difficulty: "Medium"
rating: 1804
created: "2025-11-10T21:45:36+08:00"
updated: "2025-11-10T21:45:37+08:00"
upvotes: 1
comments: 0
---

# 3742. 网格中得分最大的路径

> **[yiduobo的每日leetcode 3742.网格中得分最大的路径](https://zhuanlan.zhihu.com/p/1970891866921740113) · 知乎 · 2025-11-10 · 赞同 1**
> 力扣：[3742. 网格中得分最大的路径](https://leetcode.cn/problems/maximum-path-score-in-a-grid/) · Medium · 灵茶山艾府：[网格图 DP + 优化循环次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3742.网格中得分最大的路径

[3742. 网格中得分最大的路径 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-path-score-in-a-grid/description/)

题目给出一个m \* n的网格grid，其中每个单元格为0、1或者2。m和n的大小都不超过200，另外grid[0][0]一定为0。

现在要求从左上角(0, 0)出发，目标是到达右下角(m - 1, n - 1)，每一步都只能向右或者向下移动。

对于值为v的单元格，走到这个单元格的得分为v，若v > 0，那么还需要额外花费1的代价。

给出一个整数k，大小不超过1000。问在总代价不超过k的前提下走到(m - 1, n - 1)可以获得的最大分数。若不存在合法的路径，则返回-1。

如果不考虑代价，那么本题就是非常经典的动态规划问题，使用f[i][j]表示走到(i, j)可以获得的最大分数。由于本题的数据规模不大，因此可以直接将k编码到状态表示中，令f[i][j][t]表示走到(i, j)且花费的代价为t时可以获得的最大分数，那么对于f[i][j][t]，若grid[i][j]为0，那么就有f[i][j][t] \= max(f[i - 1][j][t], f[i][j - 1][t])，反之若grid[i][j] > 0，则有f[i][j][t] \= max(f[i - 1][j][t - 1], f[i][j - 1][t - 1]) + grid[i][j]。

全部计算完成后，max(f[m - 1][n - 1])即为最终答案。

另外需要注意，与经典版本相同，本题也需要考虑i \= 0或者j \= 0时的特殊情况。

最后附上python代码：

```python
class Solution(object):
    def maxPathScore(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        f = [[[-1] * (k + 1) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    s = 1
                else:
                    s = 0
                for t in range(s, k + 1):
                    if i == 0:
                        if j == 0:
                            f[i][j][t] = 0
                        else:
                            if f[i][j - 1][t - s] != -1:
                                f[i][j][t] = f[i][j - 1][t - s] + grid[i][j]
                    elif j == 0:
                        if f[i - 1][j][t - s] != -1:
                            f[i][j][t] = f[i - 1][j][t - s] + grid[i][j]
                    else:
                        if f[i][j - 1][t - s] != -1:
                            f[i][j][t] = f[i][j - 1][t - s] + grid[i][j]
                        if f[i - 1][j][t - s] != -1 and (f[i][j][t] == -1 or f[i][j][t] < f[i - 1][j][t - s] + grid[i][j]):
                            f[i][j][t] = f[i - 1][j][t - s] + grid[i][j]
        
        return max(f[-1][-1])
```
