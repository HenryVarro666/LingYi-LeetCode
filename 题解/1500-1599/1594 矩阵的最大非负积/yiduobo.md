---
title: "1594. 矩阵的最大非负积"
aliases: ["yiduobo的每日leetcode 1594.矩阵的最大非负积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432285819"
zhihu_id: "432285819"
zhihu_title: "yiduobo的每日leetcode 1594.矩阵的最大非负积"
question_id: "1594"
question: "矩阵的最大非负积"
problem_url: "https://leetcode.cn/problems/maximum-non-negative-product-in-a-matrix/"
difficulty: "Medium"
rating: 1807
created: "2021-11-11T23:42:08+08:00"
updated: "2021-11-11T23:42:08+08:00"
upvotes: 1
comments: 2
---

# 1594. 矩阵的最大非负积

> **[yiduobo的每日leetcode 1594.矩阵的最大非负积](https://zhuanlan.zhihu.com/p/432285819) · 知乎 · 2021-11-11 · 赞同 1**
> 力扣：[1594. 矩阵的最大非负积](https://leetcode.cn/problems/maximum-non-negative-product-in-a-matrix/) · Medium · 灵茶山艾府：[记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1594.矩阵的最大非负积

[力扣](https://leetcode-cn.com/problems/maximum-non-negative-product-in-a-matrix/)

经典的动态规划问题。不妨先回顾一下矩阵中没有负数的情况。此时状态f[i][j]表示以第i行第j列结尾的路径的最大乘积，那么就有f[i][j] \= max(f[i - 1][j], f[i][j - 1]) \* grid[i][j]。

观察这个转移方程，若此时的grid[i][j]为正数，那么效果是不变的；若grid[i][j]为负数，那么此时照搬上面转移方程得到的反而是以第i行第j列结尾的路径的最小乘积，是不符合要求的。对于grid[i][j]为负数的情况，显然是希望以第i行第j - 1列为结尾，或者第i - 1行，第j列为结尾的路径乘积为负数，且尽可能地小，那么类似于f[i][j]，可以记这个最小值为g[i][j]，那么：

1、当grid[i][j] > 0时：

f[i][j]不变，依然是f[i][j] \= max(f[i - 1][j], f[i][j - 1]) \* grid[i][j]

为了使得g[i][j]尽可能小，在grid[i][j]为正数的前提下就希望其路径的上一步尽可能小，因此就有g[i][j] \= min(g[i - 1][j], g[i][j - 1]) \* grid[i][j]

2、当grid[i][j] \= 0时：

此时无论怎么走都有f[i][j] \= g[i][j] \= 0

3、当grid[i][j] \< 0时：

为了使得f[i][j]尽可能大，在grid[i][j]为负数的前提下就希望其路径的上一步尽可能小，因此就有f[i][j] \= min(g[i - 1][j], g[i][j - 1]) \* grid[i][j]

类似的，对于g[i][j]就有g[i][j] \= max(f[i - 1][j], f[i][j - 1]) \* grid[i][j]

最后附上python代码：

```python
class Solution(object):
    def maxProductPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        f = [[None] * n for _ in range(m)]
        g = [[None] * n for _ in range(m)]
        
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = g[i][j] = grid[i][j]
                    else:
                        f[i][j] = g[i][j] = f[i][j - 1] * grid[i][j]
                elif j == 0:
                    f[i][j] = g[i][j] = f[i - 1][j] * grid[i][j]
                elif grid[i][j] > 0:
                    f[i][j] = max(f[i][j - 1], f[i - 1][j]) * grid[i][j]
                    g[i][j] = min(g[i][j - 1], g[i - 1][j]) * grid[i][j]
                elif grid[i][j] < 0:
                    f[i][j] = min(g[i][j - 1], g[i - 1][j]) * grid[i][j]
                    g[i][j] = max(f[i][j - 1], f[i - 1][j]) * grid[i][j]
                else:
                    f[i][j] = g[i][j] = 0
        
        if f[-1][-1] < 0:
            return -1
        
        return f[-1][-1] % (10 ** 9 + 7)
```
