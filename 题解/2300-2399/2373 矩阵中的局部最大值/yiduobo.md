---
title: "2373. 矩阵中的局部最大值"
aliases: ["yiduobo的每日leetcode 2373.矩阵中的局部最大值"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563657128"
zhihu_id: "563657128"
zhihu_title: "yiduobo的每日leetcode 2373.矩阵中的局部最大值"
question_id: "2373"
question: "矩阵中的局部最大值"
problem_url: "https://leetcode.cn/problems/largest-local-values-in-a-matrix/"
difficulty: "Easy"
created: "2022-09-12T17:57:11+08:00"
updated: "2022-09-12T17:57:11+08:00"
upvotes: 0
comments: 0
---

# 2373. 矩阵中的局部最大值

> **[yiduobo的每日leetcode 2373.矩阵中的局部最大值](https://zhuanlan.zhihu.com/p/563657128) · 知乎 · 2022-09-12 · 赞同 0**
> 力扣：[2373. 矩阵中的局部最大值](https://leetcode.cn/problems/largest-local-values-in-a-matrix/) · Easy · 灵茶山艾府：[原地修改](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2373.矩阵中的局部最大值

[力扣](https://leetcode.cn/problems/largest-local-values-in-a-matrix/)

由于题目的数据规模很小，因此可以直接枚举所有的3\*3矩阵然后计算其中的最大值。我在这里采用了分两步的做法。首先令f[i][j]表示以(i, j)为左上角的2\*2矩阵中的最大值，那么

f[i][j] \= max(grid[i][j], grid[i][j +1], grid[i + 1][j], grid[i +1][j + 1])

接下来再令g[i][j]表示以(i, j)为左上角的3\*3矩阵中的最大值，那么

g[i][j] \= max(f[i][j], f[i][j + 1], f[i +1][j], f[i + 1][j + 1])

而这里的g就是题目的最终答案

最后附上python代码：

```python
class Solution(object):
    def largestLocal(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """

        n = len(grid)
        f = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(n - 1):
            for j in range(n - 1):
                f[i][j] = max(grid[i][j], grid[i + 1][j], grid[i][j + 1], grid[i + 1][j + 1])
        
        g = [[0] * (n - 2) for _ in range(n - 2)]
        for i in range(n - 2):
            for j in range(n - 2):
                g[i][j] = max(f[i][j], f[i + 1][j], f[i][j + 1], f[i + 1][j + 1])
        
        return g
```
