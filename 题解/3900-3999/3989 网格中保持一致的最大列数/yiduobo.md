---
title: "3989. 网格中保持一致的最大列数"
aliases: ["yiduobo的每日leetcode 3989.网格中保持一致的最大列数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2059696229198587568"
zhihu_id: "2059696229198587568"
zhihu_title: "yiduobo的每日leetcode 3989.网格中保持一致的最大列数"
question_id: "3989"
question: "网格中保持一致的最大列数"
problem_url: "https://leetcode.cn/problems/maximum-consistent-columns-in-a-grid/"
difficulty: "Hard"
rating: 1800
created: "2026-07-13T21:42:05+08:00"
updated: "2026-07-13T21:42:05+08:00"
upvotes: 1
comments: 0
---

# 3989. 网格中保持一致的最大列数

> **[yiduobo的每日leetcode 3989.网格中保持一致的最大列数](https://zhuanlan.zhihu.com/p/2059696229198587568) · 知乎 · 2026-07-13 · 赞同 1**
> 力扣：[3989. 网格中保持一致的最大列数](https://leetcode.cn/problems/maximum-consistent-columns-in-a-grid/) · Hard · 灵茶山艾府：[相邻相关型 DP + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3989.网格中保持一致的最大列数

<https://leetcode.cn/problems/maximum-consistent-columns-in-a-grid/>

题目给出一个大小为m \* n的二维整数数组grid，以及一个整数limit。其中m和n都不超250。

现在可以从网格中移除零个或者多个列，但必须至少保留一列。剩余列的相对顺序保持不变。

对于每一行index，以及每一对相连的剩余列a和b，其中a \< b，若|grid[i][b] - grid[i][a]| \<\= limit，那么就称网格是一致的。

问使得网格成为一致的所能保留的最大列数。

由于一致的检测只发生在相邻列之间，这也就意味着某一列是否可以选用，只取决于之前操作后剩下的最后一列。基于这一点，就可以很容易得到一种动态规划的做法。令f[index]表示下标为0到index的这些列中，保留index这一列的前提下可能保留的最大列数，那么对于f[index]：

1、可以仅保留这一列，其他的都不要，因此可以初始化f[index] \= 1。

2、也可以从0到index - 1枚举之前保留的最后一列pre，若index和pre这两列兼容，那么就有f[index] \= max(f[index], f[pre] + 1)。

全部计算完成后，最终答案就是max(f)，最终时间复杂度为O(m \* n^2)。

最后附上python代码：

```python
class Solution(object):
    def maxConsistentColumns(self, grid, limit):
        """
        :type grid: List[List[int]]
        :type limit: int
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])
        f = []

        def check(x, y):
            for index in range(m):
                if abs(grid[index][x] - grid[index][y]) > limit:
                    return False
            return True

        res = 0
        for index in range(n):
            f.append(1)
            for pre in range(index):
                if check(index, pre):
                    f[-1] = max(f[-1], f[pre] + 1)
            
        return max(f)
```
