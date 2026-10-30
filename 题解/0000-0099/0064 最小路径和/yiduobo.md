---
title: "64. 最小路径和"
aliases: ["yiduobo的每日leetcode 64.最小路径和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/二-网格图-DP", "题单/LeetCode-热题-100/多维动态规划", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129879387"
zhihu_id: "129879387"
zhihu_title: "yiduobo的每日leetcode 64.最小路径和"
question_id: "64"
question: "最小路径和"
problem_url: "https://leetcode.cn/problems/minimum-path-sum/"
difficulty: "Medium"
created: "2020-04-13T21:59:54+08:00"
updated: "2020-04-13T21:59:54+08:00"
upvotes: 0
comments: 0
---

# 64. 最小路径和

> **[yiduobo的每日leetcode 64.最小路径和](https://zhuanlan.zhihu.com/p/129879387) · 知乎 · 2020-04-13 · 赞同 0**
> 力扣：[64. 最小路径和](https://leetcode.cn/problems/minimum-path-sum/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

64.最小路径和<https://leetcode-cn.com/problems/minimum-path-sum/>

前面两题的改版，同样是用动态规划求解。

令f[i][j]表示走到第i行第j列的最小路径和，那么：

1、i和j都为0。此时为起点，f[i][j] \= grid[i][j]。

2、i为0，j不为0。此时只能从左侧的格子走过来，因此有f[i][j] \= f[i][j - 1] + grid[i][j]。

3、i不为0，j为0。此时只能从上边的格子走过来，因此有f[i][j] \= f[i - 1][j] + grid[i][j]。

4、i和j都不为0。此时可以从左侧或者上边走过来，因此有f[i][j] \= min(f[i - 1][j], f[i][j - 1]) + grid[i][j]

同样的，这里也可以用滚动数组或者直接在grid上计算来节省空间。

最后附上python代码：

```python
class Solution(object):
    def minPathSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        grid[i][j] += grid[i][j - 1]
                elif j == 0:
                    grid[i][j] += grid[i - 1][j]
                else:
                    grid[i][j] += min(grid[i][j - 1], grid[i - 1][j])
        return grid[m - 1][n - 1]
```
