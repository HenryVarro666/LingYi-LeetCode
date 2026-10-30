---
title: "2684. 矩阵中移动的最大次数"
aliases: ["yiduobo的每日leetcode 2684.矩阵中移动的最大次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/breadth-first-search", "题单/网格图", "题单/动态规划", "题单/网格图/一-网格图-DFS", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649796409"
zhihu_id: "649796409"
zhihu_title: "yiduobo的每日leetcode 2684.矩阵中移动的最大次数"
question_id: "2684"
question: "矩阵中移动的最大次数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/"
difficulty: "Medium"
rating: 1626
created: "2023-08-13T22:56:32+08:00"
updated: "2023-08-13T22:56:32+08:00"
upvotes: 0
comments: 0
---

# 2684. 矩阵中移动的最大次数

> **[yiduobo的每日leetcode 2684.矩阵中移动的最大次数](https://zhuanlan.zhihu.com/p/649796409) · 知乎 · 2023-08-13 · 赞同 0**
> 力扣：[2684. 矩阵中移动的最大次数](https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/) · Medium · 灵茶山艾府：[两种方法：DFS / BFS（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2684.矩阵中移动的最大次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/description/)

经典的动态规划问题。令f[i][j]表示从第i行第j列这个单元格出发可移动的最大移动次数，那么对于f[i][j]，首先可以初始化所有的f[i][n - 1]为0，也就是位于最右侧这一列的所有位置都已经无法移动了。接下里对于从n - 2到0遍历j，对于当前的f[i][j]：

1、若i大于0，也就是当前不处于最上面这一行，同时grid[i][j] \< grid[i - 1][j + 1]，那么就有

f[i][j] \= max(f[i][j], f[i - 1][j + 1] + 1)

表示可以从当前位置出发走到右侧这一列的上方这一行

2、若grid[i][j] \< grid[i][j + 1]，那么就有

f[i][j] \= max(f[i][j], f[i][j + 1] + 1)

表示可以从当前位置出发走到右侧这一列的同一行

3、若i小于m - 1，也就是当前不处于最下面这一行，同时grid[i][j] \< grid[i + 1][j + 1]，那么就有

f[i][j] \= max(f[i][j], f[i + 1][j + 1] + 1)

表示可以从当前位置出发走到右侧这一列的下方这一行

动态规划计算结束后，第一列的f值，也就是f[0][0]、f[1][0]、...、f[m - 1][0]中的最大值即为最终答案。

另外，由于f每一轮都由上一轮转移过来，因此可以利用滚动数组省去j这一维。

最后附上python代码：

```python
class Solution(object):
    def maxMoves(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        f = [0] * m
        for j in range(n - 2, -1, -1):
            g = f[:]
            f = [0] * m
            for i in range(m):
                if i > 0 and grid[i][j] < grid[i - 1][j + 1]:
                    f[i] = max(f[i], g[i - 1] + 1)
                if grid[i][j] < grid[i][j + 1]:
                    f[i] = max(f[i], g[i] + 1)
                if i < m - 1 and grid[i][j] < grid[i + 1][j + 1]:
                    f[i] = max(f[i], g[i + 1] + 1)
            

        return max(f)
```
