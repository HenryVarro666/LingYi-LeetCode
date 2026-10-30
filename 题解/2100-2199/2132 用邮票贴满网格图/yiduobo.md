---
title: "2132. 用邮票贴满网格图"
aliases: ["yiduobo的每日leetcode 2132.用邮票贴满网格图"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527234922"
zhihu_id: "527234922"
zhihu_title: "yiduobo的每日leetcode 2132.用邮票贴满网格图"
question_id: "2132"
question: "用邮票贴满网格图"
problem_url: "https://leetcode.cn/problems/stamping-the-grid/"
difficulty: "Hard"
rating: 2364
created: "2022-06-11T01:16:46+08:00"
updated: "2022-06-11T01:16:46+08:00"
upvotes: 0
comments: 0
---

# 2132. 用邮票贴满网格图

> **[yiduobo的每日leetcode 2132.用邮票贴满网格图](https://zhuanlan.zhihu.com/p/527234922) · 知乎 · 2022-06-11 · 赞同 0**
> 力扣：[2132. 用邮票贴满网格图](https://leetcode.cn/problems/stamping-the-grid/) · Hard · 灵茶山艾府：[【图解】从一维差分到二维差分（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2132.用邮票贴满网格图

[力扣](https://leetcode.cn/problems/stamping-the-grid/)

很有意思的题目，我在这里的做法是反复利用二维前缀和。

首先，对于某个坐标为(i, j)个格子来说，能够以这个格子为右下角贴上邮票的条件为：

1、行坐标i必须大于等于stampHeight - 1

2、列坐标j必须大于等于stampWidth - 1

3、以(i - stampHeight +1, j - stampWidth + 1)为左上角，(i, j)为右下角的矩阵中不存在被占据的格子

前两个条件是很好判断的，第三个条件则可以转化为以(i - stampHeight +1, j - stampWidth + 1)为左上角，(i, j)为右下角的矩阵中所有元素之和都为0。这是一个经典的二维区间和问题，可以利用二维前缀和来解决。

令f[i][j]表示以(0, 0)为左上角，(i, j)为右下角的矩阵中所有元素之和，那么：

1、当i \= 0且j \= 0时，有f[i][j] \= grid[i][j]

2、当i \= 0且j > 0时，有f[i][j] \= f[i][j - 1] + grid[i][j]

3、当i > 0且j \= 0时，有f[i][j] \= f[i - 1][j] + grid[i][j]

4、当i > 0且j > 0时，有f[i][j] \= f[i - 1][j] + f[i][j - 1] - f[i - 1][j - 1] + grid[i][j]

根据上面的结论，就可以在O(mn)的时间内计算出所有的f。得到f之和，要计算以(x, y)为左上角，(i, j)为右下角的矩阵中元素之和，就可以利用f来辅助计算：

1、当x \= 0且y \= 0时，元素之和就等于f[i][j]

2、当x \= 0且y > 0时，元素之和就等于f[i][j] - f[i][y - 1]

3、当x > 0且y \= 0时，元素之和就等于f[i][j] - f[x - 1][j]

4、当x > 0且y > 0时，元素之和就等于f[i][j] - f[x - 1][j] - f[i][y - 1] + f[x - 1][y - 1]

此时就可以在O(mn)的时间内求出grid中能以哪些格子为右下角来贴邮票。使用一个二维数组g，记录是否能以当前格子为右下角贴上邮票，那么对于某个格子(i, j)，若能以该格子贴上邮票，那么就有g[i][j] \= 1，否则就有g[i][j] \= 0。

接下来需要想办法判断每个格子能否被邮票覆盖住。对于某个格子(i, j)，若在以(i, j)为左上角，min((i + stampHeight - 1, m - 1), min(j + stampWidth - 1, n - 1))为右下角的矩阵中有某个格子对应的g等于1，那么以这个格子为右下角贴上邮票，就可以覆盖住格子(i, j)，那么此时问题就转化成了在二维数组g中，以(i, j)为左上角，以min((i + stampHeight - 1, m - 1), min(j + stampWidth - 1, n - 1))为右下角的矩阵中是否存在1，这与最开始能否贴邮票的问题是一个路子，只是现在的二维前缀和变成了二维后缀和而已。于是如法炮制，计算g的二维后缀和，然后计算每个格子能否被邮票覆盖住即可。

最后附上python代码：

```python
class Solution(object):
    def possibleToStamp(self, grid, stampHeight, stampWidth):
        """
        :type grid: List[List[int]]
        :type stampHeight: int
        :type stampWidth: int
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = grid[i][j]
                    else:
                        f[i][j] = f[i][j - 1] + grid[i][j]
                elif j == 0:
                    f[i][j] = f[i - 1][j] + grid[i][j]
                else:
                    f[i][j] = f[i - 1][j] + f[i][j - 1] - f[i - 1][j - 1] + grid[i][j]
        
        g = [[0] * n for _ in range(m)]
        for i in range(stampHeight - 1, m):
            for j in range(stampWidth - 1, n):
                x = i - stampHeight + 1
                y = j - stampWidth + 1
                if x == 0:
                    if y == 0:
                        cnt = f[i][j]
                    else:
                        cnt = f[i][j] - f[i][y - 1]
                elif y == 0:
                    cnt = f[i][j] - f[x - 1][j]
                else:
                    cnt = f[i][j] - f[x - 1][j] - f[i][y - 1] + f[x - 1][y - 1]
                
                if cnt > 0:
                    g[i][j] = 0
                else:
                    g[i][j] = 1

        f = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if i == m - 1:
                    if j == n - 1:
                        f[i][j] = g[i][j]
                    else:
                        f[i][j] = f[i][j + 1] + g[i][j]
                elif j == n - 1:
                    f[i][j] = f[i + 1][j] + g[i][j]
                else:
                    f[i][j] = f[i + 1][j] + f[i][j + 1] - f[i + 1][j + 1] + g[i][j]
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    continue
                
                x = min(m - 1, i + stampHeight - 1)
                y = min(n - 1, j + stampWidth - 1)
                if x == m - 1:
                    if y == n - 1:
                        cnt = f[i][j]
                    else:
                        cnt = f[i][j] - f[i][y + 1]
                elif y == n - 1:
                    cnt = f[i][j] - f[x + 1][j]
                else:
                    cnt = f[i][j] - f[x + 1][j] - f[i][y + 1] + f[x + 1][y + 1]
                
                if cnt == 0:
                    return False

        return True
```
