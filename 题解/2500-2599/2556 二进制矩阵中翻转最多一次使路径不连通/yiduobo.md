---
title: "2556. 二进制矩阵中翻转最多一次使路径不连通"
aliases: ["yiduobo的每日leetcode 2556.二进制矩阵中翻转最多一次使路径不连通"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/网格图", "题单/贪心算法", "题单/网格图/五-综合应用", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638959175"
zhihu_id: "638959175"
zhihu_title: "yiduobo的每日leetcode 2556.二进制矩阵中翻转最多一次使路径不连通"
question_id: "2556"
question: "二进制矩阵中翻转最多一次使路径不连通"
problem_url: "https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/"
difficulty: "Medium"
rating: 2369
created: "2023-06-26T18:47:44+08:00"
updated: "2023-06-26T18:47:44+08:00"
upvotes: 0
comments: 0
---

# 2556. 二进制矩阵中翻转最多一次使路径不连通

> **[yiduobo的每日leetcode 2556.二进制矩阵中翻转最多一次使路径不连通](https://zhuanlan.zhihu.com/p/638959175) · 知乎 · 2023-06-26 · 赞同 0**
> 力扣：[2556. 二进制矩阵中翻转最多一次使路径不连通](https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/) · Medium · 灵茶山艾府：[转换成求轮廓是否相交（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2556.二进制矩阵中翻转最多一次使路径不连通

[力扣](https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/)

首先，将0翻转成为1是没有任何意义的，对于本题只需要考虑将1变为0的情况。那么如果将本题中的每个位置视为图中的一个点，那么实际上问的就是图中是否存在割点。

一开始以为本题可以往上下左右四个方向行走，那么这就是一个经典的无向图求割点的问题，直接使用tarjan算法一趟dfs就行了。

不过本题实际上只允许向下和向右两个方向，就变成了求有向图中的割点，并不是那么简单了。

注意到本题给出的是一个二维的网格，我在这里采用了一种比较取巧的处理方法。

令f[i][j]表示从(0, 0)走到位置(i, j)的方案数，g[i][j]表示从(m - 1, n - 1)反向走到(i, j)的方案数，那么f[i][j] \* g[i][j]就是从(0, 0)出发，经过(i, j)，最后走到(m - 1, n - 1)的方案数。另一方面，f[m - 1][n - 1]就是从(0, 0)走到(m - 1, n - 1)的方案数，那么若存在某个非起点和终点的位置(i, j)，满足f[i][j] \* g[i][j] \= f[m - 1][n - 1]，那么就说明每一条从(0, 0)到(m - 1, n - 1)的路径都会经过(i, j)，因此翻转掉(i, j)就必然使得(0, 0)无法再到达(m - 1, n - 1)，此时返回true。若不存在这样的点，答案就是false。

需要注意的是，上面这种计算方式f和g的值都会非常大，如果语言不支持大整数类型的话就需要自己实现大数加法和乘法。

最后附上python代码：

```python
class Solution(object):
    def isPossibleToCutPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        f[0][0] = 1
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    if i == 0:
                        if j == 0:
                            f[i][j] = 1
                        else:
                            f[i][j] = f[i][j - 1]
                    elif j == 0:
                        f[i][j] = f[i - 1][j]
                    else:
                        f[i][j] = f[i - 1][j] + f[i][j - 1]
        
        g = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 1:
                    if i == m - 1:
                        if j == n - 1:
                            g[i][j] =  1
                        else:
                            g[i][j] = g[i][j + 1]
                    elif j == n - 1:
                        g[i][j] = g[i + 1][j]
                    else:
                        g[i][j] = g[i + 1][j] + g[i][j + 1]
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                if i == m - 1 and j == n - 1:
                    continue
                if f[i][j] * g[i][j] == f[m - 1][n - 1]:
                    return True
        
        return False
```
