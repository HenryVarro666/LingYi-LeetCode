---
title: "2304. 网格中的最小路径代价"
aliases: ["yiduobo的每日leetcode 2304.网格中的最小路径代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554997067"
zhihu_id: "554997067"
zhihu_title: "yiduobo的每日leetcode 2304.网格中的最小路径代价"
question_id: "2304"
question: "网格中的最小路径代价"
problem_url: "https://leetcode.cn/problems/minimum-path-cost-in-a-grid/"
difficulty: "Medium"
rating: 1658
created: "2022-08-18T01:16:34+08:00"
updated: "2022-08-18T01:16:34+08:00"
upvotes: 0
comments: 0
---

# 2304. 网格中的最小路径代价

> **[yiduobo的每日leetcode 2304.网格中的最小路径代价](https://zhuanlan.zhihu.com/p/554997067) · 知乎 · 2022-08-18 · 赞同 0**
> 力扣：[2304. 网格中的最小路径代价](https://leetcode.cn/problems/minimum-path-cost-in-a-grid/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推，再到 O(1) 空间！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2304.网格中的最小路径代价

[力扣](https://leetcode.cn/problems/minimum-path-cost-in-a-grid/)

经典的动态规划问题。令f[i][j]表示以grid[i][j]为终点的路径的最小代价，那么对于f[i][j]，当i \= 0时，f[i][j]就等于grid[i][j]。当i > 0时，grid[i][j]可以从i - 1层的任何一个位置走过来，因此需要枚举上一层的起点k。从grid[i - 1][k]走到grid[i][j]的代价是

moveCost\[grid\[i - 1\]\[k\]\]\[j\]

除此之外，还需要额外加上grid[i][j]自身的权重，因此就有

f\[i\]\[j\] \= min(f\[i\]\[j\], f\[i - 1\]\[k\] + moveCost\[grid\[i - 1\]\[k\]\]\[j\] + grid\[i\]\[j\])，这里的k满足0 \<\= k \< n

所有的f计算完成后，min(f[-1])就是最终答案。

另外，注意到f每一轮只与上一轮有关，因此可以使用滚动数组节省掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def minPathCost(self, grid, moveCost):
        """
        :type grid: List[List[int]]
        :type moveCost: List[List[int]]
        :rtype: int
        """

        f = grid[0][:]
        m = len(grid)
        n = len(grid[0])

        for i in range(1, m):
            g = []
            for j in range(n):
                g.append(None)
                for k in range(n):
                    if g[-1] is None or g[-1] > f[k] + moveCost[grid[i - 1][k]][j] + grid[i][j]:
                        g[-1] = f[k] + moveCost[grid[i - 1][k]][j] + grid[i][j]
            
            f = g[:]

        return min(f)
```
