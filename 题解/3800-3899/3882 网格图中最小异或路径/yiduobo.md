---
title: "3882. 网格图中最小异或路径"
aliases: ["yiduobo的每日leetcode 3882.网格图中最小异或路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/动态规划", "题单/网格图/五-综合应用", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022072413551108894"
zhihu_id: "2022072413551108894"
zhihu_title: "yiduobo的每日leetcode 3882.网格图中最小异或路径"
question_id: "3882"
question: "网格图中最小异或路径"
problem_url: "https://leetcode.cn/problems/minimum-xor-path-in-a-grid/"
difficulty: "Medium"
rating: 1771
created: "2026-03-30T22:14:17+08:00"
updated: "2026-03-30T22:14:17+08:00"
upvotes: 1
comments: 0
---

# 3882. 网格图中最小异或路径

> **[yiduobo的每日leetcode 3882.网格图中最小异或路径](https://zhuanlan.zhihu.com/p/2022072413551108894) · 知乎 · 2026-03-30 · 赞同 1**
> 力扣：[3882. 网格图中最小异或路径](https://leetcode.cn/problems/minimum-xor-path-in-a-grid/) · Medium · 灵茶山艾府：[网格图 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3882.网格图中最小异或路径

<https://leetcode.cn/problems/minimum-xor-path-in-a-grid/description/>

题目给出一个大小为m \* n的二维整数数组grid，其中元素大小在0到1023之间。

现在要求从左上角的单元格(0, 0)出发，到达右下角的单元格(m - 1, n - 1)。

在每一步移动中，都可以向右或者向下走。路径的代价定义为路径上所有单元格的值按位异或。

问从(0, 0)走到(m - 1, n - 1)的所有有效路径中最小的可能异或值是多少。

经典的动态规划问题的变形，但是在这里不能沿用之前f[i][j]表示走到(i, j)的最小路径值，因为路径值是通过异或操作计算得到的，上一步的最小可能无法得到这一步的最小。

注意到grid中的元素值在0到1023之间，因此在这里就可以改成带着值进行计算。

令f[i][j]表示走到(i, j)时所有可能的异或结果集合，那么对于f[i][j]中的异或结果v，若i + 1 \< m，那么就可以将v ^ grid[i + 1][j]加入到f[i + 1][j]；同理，若j + 1 \< n，那么就可以将v ^ grid[i][j + 1]加入到f[i][j + 1]。

计算结束后，f[-1][-1]中的最小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        f = [[set() for _ in range(n)] for _ in range(m)]
        f[0][0].add(grid[0][0])
        for i in range(m):
            for j in range(n):
                for v in f[i][j]:
                    if i + 1 < m:
                        f[i + 1][j].add(v ^ grid[i + 1][j])
                    if j + 1 < n:
                        f[i][j + 1].add(v ^ grid[i][j + 1])
        
        res = None
        for v in f[-1][-1]:
            if res is None or res > v:
                res = v
        return res
```
