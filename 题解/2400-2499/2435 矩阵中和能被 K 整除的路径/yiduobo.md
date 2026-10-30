---
title: "2435. 矩阵中和能被K整除的路径"
aliases: ["yiduobo的每日leetcode 2435.矩阵中和能被K整除的路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583428508"
zhihu_id: "583428508"
zhihu_title: "yiduobo的每日leetcode 2435.矩阵中和能被K整除的路径"
question_id: "2435"
question: "矩阵中和能被 K 整除的路径"
problem_url: "https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/"
difficulty: "Hard"
rating: 1952
created: "2022-11-14T22:22:10+08:00"
updated: "2022-11-14T22:22:10+08:00"
upvotes: 1
comments: 0
---

# 2435. 矩阵中和能被K整除的路径

> **[yiduobo的每日leetcode 2435.矩阵中和能被K整除的路径](https://zhuanlan.zhihu.com/p/583428508) · 知乎 · 2022-11-14 · 赞同 1**
> 力扣：[2435. 矩阵中和能被 K 整除的路径](https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/) · Hard · 灵茶山艾府：[动态规划：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2435.矩阵中和能被K整除的路径

[力扣](https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/description/)

经典动态规划问题的加强版，那么一个自然的想法就是在原有算法的基础上把这个加强的部分给适配进去。

令f[i][j][r]表示从左上角走到第i行第j列这个单元格，且当前路径上的数字之和模k余r时可行的路径数量。

对于f[i][j][r]，可以尝试向右走或向下走，即通过f[i][j][r]分别更新f[i][j + 1][(r + grid[i][j + 1]) % k]和f[i +1][j][(r + grid[i + 1][j]) % k]。

全部处理完成后，f[-1][-1][0]就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def numberOfPaths(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        f = [[[0] * k for j in range(n)] for i in range(m)]

        f[0][0][grid[0][0] % k] = 1
        mod = 10 ** 9 + 7
        for i in range(m):
            for j in range(n):
                for r in range(k):
                    if f[i][j][r] > 0:
                        f[i][j][r] %= mod
                        if i + 1 < m:
                            f[i + 1][j][(r + grid[i + 1][j]) % k] += f[i][j][r]
                        if j + 1 < n:
                            f[i][j + 1][(r + grid[i][j + 1]) % k] += f[i][j][r]
        
        return f[-1][-1][0]
```
