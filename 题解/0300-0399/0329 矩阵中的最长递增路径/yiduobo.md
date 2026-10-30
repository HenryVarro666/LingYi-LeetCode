---
title: "329. 矩阵中的最长递增路径"
aliases: ["yiduobo的每日leetcode 329.矩阵中的最长递增路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161401676"
zhihu_id: "161401676"
zhihu_title: "yiduobo的每日leetcode 329.矩阵中的最长递增路径"
question_id: "329"
question: "矩阵中的最长递增路径"
problem_url: "https://leetcode.cn/problems/longest-increasing-path-in-a-matrix/"
created: "2020-07-18T01:42:34+08:00"
updated: "2020-07-18T01:42:34+08:00"
upvotes: 0
comments: 0
---

# 329. 矩阵中的最长递增路径

> **[yiduobo的每日leetcode 329.矩阵中的最长递增路径](https://zhuanlan.zhihu.com/p/161401676) · 知乎 · 2020-07-18 · 赞同 0**
> 力扣：[329. 矩阵中的最长递增路径](https://leetcode.cn/problems/longest-increasing-path-in-a-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

329.矩阵中的最长递增路径<https://leetcode-cn.com/problems/longest-increasing-path-in-a-matrix/>

经典的记忆化搜索问题，设f[i][j]表示以matrix[i][j]为起点的路径最长可以有多长，那么对于其上、下、左、右这四个点，若满足在矩阵之内，且值小于matrix[i][j]，那么说明matrix[i][j]接下来可以往这里走，于是有

matrix[i][j] \= max(matrix[x][y]) + 1

其中(x，y)的取值范围在

(i + 1， j)，(i - 1， j)，(i， j + 1)以及(i， j - 1)之间，且(x，y)在矩阵内，同时matrix[x][y] \< matrix[i][j]

由于每个节点只会被搜索到一次，那么最终的时间复杂度就是O(mn)。

另外，这个问题通过节点值构造有向图，然后在有向图中做拓扑排序也是可以的，图中节点数量为m \* n个，因此最终的时间复杂度同样是O(mn)。

最后附上python代码：

```python
class Solution(object):
    def longestIncreasingPath(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        f = [[None] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                if f[i][j] is None:
                    res = max(res, self.dfs(i, j, matrix, f))
        
        return res

    def dfs(self, x, y, matrix, f):
        if f[x][y] is not None:
            return f[x][y]

        res = 1
        if x > 0 and matrix[x - 1][y] < matrix[x][y]:
            res = max(res, self.dfs(x - 1, y, matrix, f) + 1)
        if x < len(matrix) - 1 and matrix[x + 1][y] < matrix[x][y]:
            res = max(res, self.dfs(x + 1, y, matrix, f) + 1)
        if y > 0 and matrix[x][y - 1] < matrix[x][y]:
            res = max(res, self.dfs(x, y - 1, matrix, f) + 1)
        if y < len(matrix[0]) - 1 and matrix[x][y + 1] < matrix[x][y]:
            res = max(res, self.dfs(x, y + 1, matrix, f) + 1)
        f[x][y] = res
        return f[x][y]
```
