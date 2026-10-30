---
title: "3665. 统计镜子反射路径数目"
aliases: ["yiduobo的每日leetcode 3665.统计镜子反射路径数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950310283898750914"
zhihu_id: "1950310283898750914"
zhihu_title: "yiduobo的每日leetcode 3665.统计镜子反射路径数目"
question_id: "3665"
question: "统计镜子反射路径数目"
problem_url: "https://leetcode.cn/problems/twisted-mirror-path-count/"
difficulty: "Medium"
rating: 1883
created: "2025-09-18T02:16:21+08:00"
updated: "2025-09-18T02:16:23+08:00"
upvotes: 1
comments: 0
---

# 3665. 统计镜子反射路径数目

> **[yiduobo的每日leetcode 3665.统计镜子反射路径数目](https://zhuanlan.zhihu.com/p/1950310283898750914) · 知乎 · 2025-09-18 · 赞同 1**
> 力扣：[3665. 统计镜子反射路径数目](https://leetcode.cn/problems/twisted-mirror-path-count/) · Medium · 灵茶山艾府：[在 62 题的基础上加个方向（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3665.统计镜子反射路径数目

[3665. 统计镜子反射路径数目 - 力扣（LeetCode）](https://leetcode.cn/problems/twisted-mirror-path-count/)

题目给出一个m \* n的二进制网格grid，其中值为0的单元格表示这是一个空格子，而值为1的单元格则表示这个单元格内是一面镜子。

一个机器人从左上角(0, 0)出发，想要到达右下角(m - 1, n - 1)。机器人只能向右或者向下移动，若机器人进入了一个有镜子的单元格，那么它在进入该单元格前被反射。若其试图从左侧向右进入镜子，它会被转向下方，同时移动到镜子正下方的单元格中；若其试图从上方向下进入镜子，它会被转向右侧，同时移动到镜子正右方的单元格中。若此次反射会导致机器人移动到网格之外，那么这条路径无效。

问从(0, 0)走到(m - 1, n - 1)的不同路径数量。

如果不考虑镜子的话，本题就是非常经典的动态规划。令f[i][j]表示走到(i, j)的路径数量，那么就有f[i][j] \= f[i - 1][j] + f[i][j - 1]。而对于本题，在加入了镜子之后，则需要将方向额外考虑进去，因此在这里需要使用两个数组f和g分别表示从左侧以及从上方进入单元格(i, j)的路径数量，那么对于f[i][j]和g[i][j]：

1、对于边界上的情况：

1-1）若i和j都为0，那么f[i][j]和g[i][j]都为1

1-2）若仅有i为0，那么只能从左侧进入(i, j)，因此只有f[i][j] \= f[i][j - 1]，g[i][j]则默认为0

1-3）若仅有j为0，那么只能从上方进入(i, j)，因此只有g[i][j] \= g[i - 1][j]，f[i][j]则默认为0

2、对于一般情况：

若(i, j)的左侧单元格(i, j - 1)为空白单元格，那么无论从哪个方向进入到(i, j - 1)，都可以顺利从左往右进入到(i, j)，因此就有f[i][j] \= f[i][j - 1] + g[i][j - 1]；反之，若(i, j - 1)是镜子，那么只有从上方进入(i, j - 1)时，才会被转向并从左侧进入(i, j)，因此就有f[i][j] \= g[i][j - 1]。

同理，若(i, j)的上方单元格(i - 1, j)为空白时，有g[i][j] \= g[i][j - 1] + f[i - 1][j]，否则就有g[i][j] \= f[i - 1][j]

全部计算完成后，最终答案就是f[-1][-1] + g[-1][-1]。

最后附上python代码：

```python
class Solution(object):
    def uniquePaths(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]
        f[0][0] = 1
        g[0][0] = 1
        mod = 10 ** 9 + 7

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        pass
                    else:
                        if grid[i][j - 1] == 0:
                            f[i][j] = f[i][j - 1]
                else:
                    if j == 0:
                        if grid[i - 1][j] == 0:
                            g[i][j] = g[i - 1][j]
                    else:
                        if grid[i][j - 1] == 0:
                            f[i][j] = f[i][j - 1] + g[i][j - 1]
                            if f[i][j] >= mod:
                                f[i][j] -= mod
                        else:
                            f[i][j] = g[i][j - 1]
                        
                        if grid[i - 1][j] == 0:
                            g[i][j] = f[i - 1][j] + g[i - 1][j]
                            if g[i][j] >= mod:
                                g[i][j] -= mod
                        else:
                            g[i][j] = f[i - 1][j]
        
        res = f[-1][-1] + g[-1][-1]
        if res >= mod:
            res -= mod
        return res
```
