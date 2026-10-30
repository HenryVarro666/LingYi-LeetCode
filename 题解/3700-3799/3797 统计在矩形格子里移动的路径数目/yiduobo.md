---
title: "3797. 统计在矩阵格子里移动的路径数目"
aliases: ["yiduobo的每日leetcode 3797.统计在矩阵格子里移动的路径数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992079762907230975"
zhihu_id: "1992079762907230975"
zhihu_title: "yiduobo的每日leetcode 3797.统计在矩阵格子里移动的路径数目"
question_id: "3797"
question: "统计在矩形格子里移动的路径数目"
problem_url: "https://leetcode.cn/problems/count-routes-to-climb-a-rectangular-grid/"
difficulty: "Hard"
rating: 2376
created: "2026-01-08T01:22:16+08:00"
updated: "2026-01-08T01:22:16+08:00"
upvotes: 1
comments: 0
---

# 3797. 统计在矩阵格子里移动的路径数目

> **[yiduobo的每日leetcode 3797.统计在矩阵格子里移动的路径数目](https://zhuanlan.zhihu.com/p/1992079762907230975) · 知乎 · 2026-01-08 · 赞同 1**
> 力扣：[3797. 统计在矩形格子里移动的路径数目](https://leetcode.cn/problems/count-routes-to-climb-a-rectangular-grid/) · Hard · 灵茶山艾府：[前缀和优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3797.统计在矩阵格子里移动的路径数目

[3797. 统计在矩形格子里移动的路径数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-routes-to-climb-a-rectangular-grid/)

题目给出一个大小为n \* m的字符矩阵grid。grid中有两种字符'.'以及'\#'，分别表示可用的单元格以及被阻塞的单元格。

现在要求计算攀爬grid的不同路径数目。每条路径必须从第n - 1行的任意格子开始，在第0行结束。路径需要满足以下条件：

- 只能经过可用单元格
- 每次移动的欧式距离最多为d，其中d为给定的整数
- 每次移动要么留在同一行，要么移动到正上方的一行
- 不能连续两次移动都留在同一行

问合法路径的数目。

由于题目规定只能从下往上或者同层移动，且不能连续两次同层移动，因此按层作为阶段的划分是很容易想到的，对应的就是f[i][j]表示通过跨层移动来到第i层第j列的路径数量，g[i][j]则表示通过同层移动来到第i层第j列的路径数量，那么：

1、对于f[i][j]：

若grid[i][j]为'\#'，那么f[i][j]必然为0。

反之，若当前处于第n - 1层，那么就有f[i][j] \= 1，因为可以选择任意为'.'的单元格作为路径的起点。若不处于n - 1层，则需要考虑从第i + 1层的哪些单元格出发可以走到(i, j)。

对于可以走到f[i][j]的f[i + 1][p]或者g[i + 1][p]，这里的p需要满足(p - j)^2 + 1 \<\= d^2，即abs(p - j) \<\= sqrt(d^2 - 1)。

注意到后面这一项是固定的，且下标必须为整数，因此可以令dd为sqrt(d^2 - 1)向下取整，那么就有j - dd \<\= p \<\= j + dd。

另外，p必须在0到m - 1之间，因此可以令left \= max(0, j - dd)，right \= min(m - 1, j + dd)，带入上面的转移方程，就有

f[i][j] \= (f[i + 1][left] + ... + f[i + 1][right]) + (g[i + 1][left] + ... + g[i + 1][right])

可以发现，这是两段区间和，可以使用前缀和进行优化。令

sf[i][j] \= f[i][0] + f[i][1] + ... + f[i][j]

sg[i][j] \= g[i][0] + g[i][1] + ... + g[i][j]

那么上面的转移方程就可以写成

f[i][j] \= (sf[i + 1][right] - sf[i +1][left - 1]) + (sg[i + 1][right] - sg[i + 1][left - 1])

得到完整的f[i]之后，只需一趟遍历，就可以计算得到sf[i]

2、对于g[i][j]：

同样的，若grid[i][j]为'\#'，那么g[i][j]必然为0，反之，由于g的定义是同层移动，因此需要考虑从第i层的哪些单元格出发可以走到(i, j)。

对于可以走到g[i][j]的f[i][p]，这里的p需要满足abs(j - p) \<\= d，即j - d \<\= p \<\= j + d。同样的，这里取left \= max(0, j - d)，right \= min(0, j + d)，那么就有

g[i][j] \= f[i][left] + ... + f[i][right] - f[i][j] \= sf[right] - sf[left - 1] - f[i][j]

这里减去f[i][j]的理由是每次移动必须走到另一个单元格，因此在进行同层移动时，不能待在(i, j)不动，因此不能从f[i][j]转移到g[i][j]

得到完整的g[i]之后，同样只需一趟遍历，就可以计算得到sg[i]

全部计算完成后，sf[0][m - 1] + sg[0][m - 1]即为最终答案。

另外注意到转移时是f、g、sf、sg相互迭代，因此可以通过调整更新的顺序，省去i这一维。具体来说，可以先分析它们之间的依赖关系，即

上一行的sf、sg -> 本行的f

本行的f -> 本行的sf

本行的sf -> 本行的g

本行的g -> 本行的sg

因此只需先使用sf和sg更新f，然后使用f更新sf，再使用sf更新g，最后使用g更新sg，就可以完全省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def numberOfRoutes(self, grid, d):
        """
        :type grid: List[str]
        :type d: int
        :rtype: int
        """
        
        n = len(grid)
        m = len(grid[0])
        mod = 10 ** 9 + 7

        f = []
        sf = []
        for j in range(m):
            if grid[-1][j] == '#':
                f.append(0)
            else:
                f.append(1)
            
            if j == 0:
                sf.append(f[0])
            else:
                sf.append(sf[-1] + f[-1])
        
        g = []
        sg = []
        for j in range(m):
            if grid[-1][j] == '#':
                g.append(0)
            else:
                left = max(0, j - d)
                right = min(m - 1, j + d)
                g.append(sf[right] - f[j])
                if left > 0:
                    g[-1] -= sf[left - 1]
            
            if j == 0:
                sg.append(g[0])
            else:
                sg.append(sg[-1] + g[-1])

        dd = int((d * d - 1) ** 0.5)

        for i in range(n - 2, -1, -1):
            for j in range(m):
                if grid[i][j] == '#':
                    f[j] = 0
                else:
                    left = max(0, j - dd)
                    right = min(m - 1, j + dd)
                    f[j] = (sf[right] + sg[right]) % mod
                    if left > 0:
                        f[j] = (f[j] - (sf[left - 1] + sg[left - 1]) % mod + mod) % mod

            sf[0] = f[0]
            for j in range(1, m):
                sf[j] = (sf[j - 1] + f[j]) % mod
            
            for j in range(m):
                if grid[i][j] == '#':
                    g[j] = 0
                else:
                    left = max(0, j - d)
                    right = min(m - 1, j + d)
                    g[j] = (sf[right] - f[j] + mod) % mod
                    if left > 0:
                        g[j] = (g[j] - sf[left - 1] + mod) % mod
            
            sg[0] = g[0]
            for j in range(1, m):
                sg[j] = (sg[j - 1] + g[j]) % mod
        
        return (sf[-1] + sg[-1]) % mod
```
