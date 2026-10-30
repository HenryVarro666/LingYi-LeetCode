---
title: "3393. 统计异或值为给定值的路径数目"
aliases: ["yiduobo的每日leetcode 3393.统计异或值为给定值的路径数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30355455359"
zhihu_id: "30355455359"
zhihu_title: "yiduobo的每日leetcode 3393.统计异或值为给定值的路径数目"
question_id: "3393"
question: "统计异或值为给定值的路径数目"
problem_url: "https://leetcode.cn/problems/count-paths-with-the-given-xor-value/"
difficulty: "Medium"
rating: 1573
created: "2025-03-15T01:05:14+08:00"
updated: "2025-03-15T01:05:14+08:00"
upvotes: 1
comments: 0
---

# 3393. 统计异或值为给定值的路径数目

> **[yiduobo的每日leetcode 3393.统计异或值为给定值的路径数目](https://zhuanlan.zhihu.com/p/30355455359) · 知乎 · 2025-03-15 · 赞同 1**
> 力扣：[3393. 统计异或值为给定值的路径数目](https://leetcode.cn/problems/count-paths-with-the-given-xor-value/) · Medium · 灵茶山艾府：[网格图 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3393.统计异或值为给定值的路径数目

[3393. 统计异或值为给定值的路径数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-paths-with-the-given-xor-value/)

题目给出一个大小为m \* n的二维整数数组grid以及一个整数k，grid中的元素以及k的大小都在0到15之间。

现在要求计算从左上角(0, 0)出发，每一步只能向下或者向右走且不能越界，最终走到右下角(m - 1, n - 1)，且路径上元素的异或值恰好等于k的路径数量。

如果不考虑异或值的限制，这就是经典的动态规划问题。

令f[i][j]表示从(0, 0)走到(i, j)的合法路径数目，然后f[i][j]可以通过上方单元格或者左侧单元格走过来，即f[i][j] \= f[i - 1][j] + f[i][j - 1]。另外对于边界的情况特殊处理就行了。

而对于路径元素异或值这一限制，由于题目保证了grid中的元素的大小都在0到15之间，那么无论怎么走，路径上元素值的异或值也只会在0到15之间，于是可以在状态表示上再加上一维v，即f[i][j][v]表示从(0, 0)走到(i, j)，且路径上异或值为v时的合法路径数目。

那么对于f\[i\]\[j\]\[v\]，依然是从上方单元格或者左侧单元格走过来，即f\[i\]\[j\]\[v\] \= f\[i - 1\]\[j\]\[v ^ grid\[i\]\[j\]\] + f\[i\]\[j - 1\]\[v ^ grid\[i\]\[j\]\]。对于边界情况同样需要特殊处理。

计算完成后，f[-1][-1][k]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countPathsWithXorValue(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])
        mod = 10 ** 9 + 7

        f = [[[0] * 16 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j][grid[i][j]] = 1
                elif i == 0:
                    for v in range(16):
                        f[i][j][v] += f[i][j - 1][v ^ grid[i][j]]
                elif j == 0:
                    for v in range(16):
                        f[i][j][v] += f[i - 1][j][v ^ grid[i][j]]
                else:
                    for v in range(16):
                        f[i][j][v] = (f[i][j - 1][v ^ grid[i][j]] + f[i - 1][j][v ^ grid[i][j]]) % mod
        
        return f[-1][-1][k]
```
