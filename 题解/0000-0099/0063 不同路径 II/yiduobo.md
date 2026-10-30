---
title: "63. 不同路径II"
aliases: ["yiduobo的每日leetcode 63.不同路径II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/二-网格图-DP", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129368314"
zhihu_id: "129368314"
zhihu_title: "yiduobo的每日leetcode 63.不同路径II"
question_id: "63"
question: "不同路径 II"
problem_url: "https://leetcode.cn/problems/unique-paths-ii/"
difficulty: "Medium"
created: "2020-04-12T23:07:38+08:00"
updated: "2020-04-12T23:07:38+08:00"
upvotes: 0
comments: 0
---

# 63. 不同路径II

> **[yiduobo的每日leetcode 63.不同路径II](https://zhuanlan.zhihu.com/p/129368314) · 知乎 · 2020-04-12 · 赞同 0**
> 力扣：[63. 不同路径 II](https://leetcode.cn/problems/unique-paths-ii/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

63.不同路径II<https://leetcode-cn.com/problems/unique-paths-ii/>

上一题的升级版本，如果继续用组合数学的方法似乎用母函数能做（不确定），于是还是老老实实用dp来处理来得方便。

f[i][j]表示到达第i行，第j列一共有多少种走法。

那么对于格子i行j列的某个格子：

1、如果是障碍物，那么f[i][j] \= 0。

2、如果不是障碍物，且i和j都为0，说明这是最原始的位置，因此f[i][j] \= 1。

3、如果不是障碍物，且i为0，j不为0，说明这是第一行，只能从同一行左边的位置走过来，因此有f[i][j] \= f[i][j - 1]。

4、如果不是障碍物，且i不为0，j为0，说明这是第一列，只能从同一列上边的位置走过来，因此有f[i][j] \= f[i - 1][j]。

5、如果不是障碍物，且i和j都不为0，那么此时可能从上一行的同一列走过来，或者从同一行的左边一格走过来，于是就有f[i][j] \= f[i - 1][j] + f[i][j - 1]。

由于这里的f总是由上一行和本行得到的，因此可以用滚动数组来替代f，或者也可以直接在原矩阵上做dp，不额外开f数组。

最后附上python代码：

```python
class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        """

        if not obstacleGrid:
            return 0

        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    obstacleGrid[i][j] = 0
                elif i == 0:
                    if j == 0:
                        obstacleGrid[i][j] = 1
                    else:
                        obstacleGrid[i][j] = obstacleGrid[i][j - 1]
                elif j == 0:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j]
                else:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]
        return obstacleGrid[m - 1][n - 1]
```
