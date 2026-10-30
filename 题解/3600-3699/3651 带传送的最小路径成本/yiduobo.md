---
title: "3651. 带传送的最小路径成本"
aliases: ["yiduobo的每日leetcode 3651.带传送的最小路径成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948874753063524149"
zhihu_id: "1948874753063524149"
zhihu_title: "yiduobo的每日leetcode 3651.带传送的最小路径成本"
question_id: "3651"
question: "带传送的最小路径成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-teleportations/"
difficulty: "Hard"
rating: 2411
created: "2025-09-11T23:59:20+08:00"
updated: "2025-09-11T23:59:24+08:00"
upvotes: 0
comments: 0
---

# 3651. 带传送的最小路径成本

> **[yiduobo的每日leetcode 3651.带传送的最小路径成本](https://zhuanlan.zhihu.com/p/1948874753063524149) · 知乎 · 2025-09-11 · 赞同 0**
> 力扣：[3651. 带传送的最小路径成本](https://leetcode.cn/problems/minimum-cost-path-with-teleportations/) · Hard · 灵茶山艾府：[网格图 DP + 后缀最小值优化 + 收敛优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3651.带传送的最小路径成本

[3651. 带传送的最小路径成本 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-path-with-teleportations/description/)

题目给出一个m \* n的二维整数数组grid以及一个整数k，要求从左上角单元格(0, 0)出发，目的地是右下角单元格(m - 1, n - 1)。其中m和n不超过80，k不超过10。

有两种移动方式可用：

普通移动：可以从单元格(i, j)向右或者向下移动，即移动到(i, j + 1)或者(i + 1, j)，移动的成本为目标单元格的值

传送：可以从任意单元格(i, j)传送人另一个满足grid[x][y] \<\= grid[i][j]的单元格(x, y)，传送的成本为0，但是最多只能传送k次

问从(0, 0)到达(m - 1, n - 1)的最小成本。

如果不考虑传送，本题就是很常规的动态规划。令f[i][j]表示到达(i, j)所需的最小成本，那么就有f[i][j] \= min(f[i - 1][j], f[i][j - 1]) + grid[i][j]。

对于本题，则可以考虑将k也编码到状态表示中，那么就是f[i][j][t]表示使用了t次传送，到达单元格(i, j)所需的最小成本，那么依然有f[i][j][t] \= min(f[i - 1][j][t], f[i][j - 1][t]) + grid[i][j]，表示当前这次移动不使用传送到达(i, j)的成本。

除此之外，还需要考虑传送到(i, j)的成本。基于题目中传送的规则，就有f[i][j][t] \= min(f[i][j][t], f[x][y][t - 1])，在这里需要满足grid[x][y] >\= grid[i][j]。

如果直接枚举所有可行的(x, y)，复杂度就比较高了，但是如果能按照grid从大到小的顺序来进行状态转移，那么问题就变成了前缀最大值，只需一趟遍历就可以解决了。于是在这里可以将所有单元格按照单元格的值从大到小进行排序，然后一趟遍历，并使用一个变量best记录当前遍历到的最大的f[x][y][t - 1]。对于当前遍历到的(x, y)，由于已经使用遍历过所有值大于grid[x][y]的单元格了，这也就意味着已经用所有值大于grid[x][y]的单元格更新过best了，此时只需使用所有值恰好等于grid[x][y]的单元格对应的f值来更新best，然后使用best更新f[x][y][t]就行了。

全部计算完成后，只需遍历所有的t，使用每种t对应的f[-1][-1][t]来更新答案即可。

需要特别注意的是，在具体实现时需要先处理传送的情况，再处理正常走的情况，因为对于特定的t，可能出现先从t - 1传送过来，再正常行走的情况，但是在t这一层正常行走后再进行传送，到达将是t + 1这一层。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        f = [[[None] * (k + 1) for _ in range(n)] for _ in range(m)]
        f[0][0][0] = 0
        position = []
        for i in range(m):
            for j in range(n):
                position.append((grid[i][j], i, j))
        position.sort(key=lambda d:-d[0])

        res = None
        for t in range(k + 1):
            if t != 0:
                p = 0
                best = None
                for v, x, y in position:
                    while p < len(position) and position[p][0] == v:
                        _, pre_x, pre_y = position[p]
                        if best is None or best > f[pre_x][pre_y][t - 1]:
                            best = f[pre_x][pre_y][t - 1]
                        p += 1
                    f[x][y][t] = best
            
            for x in range(m):
                for y in range(n):
                    best = None
                    if x > 0 and f[x - 1][y][t] is not None:
                        best = f[x - 1][y][t] + grid[x][y]
                    if y > 0 and f[x][y - 1][t] is not None:
                        if best is None or best > f[x][y - 1][t] + grid[x][y]:
                            best = f[x][y - 1][t] + grid[x][y]
                    
                    if best is not None and (f[x][y][t] is None or f[x][y][t] > best):
                        f[x][y][t] = best
            
            if f[-1][-1][t] is not None:
                if res is None or res > f[-1][-1][t]:
                    res = f[-1][-1][t]
        
        return res
```
