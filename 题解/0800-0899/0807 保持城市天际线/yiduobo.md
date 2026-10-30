---
title: "807. 保持城市天际线"
aliases: ["yiduobo的每日leetcode 807.保持城市天际线"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343236414"
zhihu_id: "343236414"
zhihu_title: "yiduobo的每日leetcode 807.保持城市天际线"
question_id: "807"
question: "保持城市天际线"
problem_url: "https://leetcode.cn/problems/max-increase-to-keep-city-skyline/"
difficulty: "Medium"
created: "2021-01-10T16:16:58+08:00"
updated: "2021-01-10T16:16:58+08:00"
upvotes: 0
comments: 0
---

# 807. 保持城市天际线

> **[yiduobo的每日leetcode 807.保持城市天际线](https://zhuanlan.zhihu.com/p/343236414) · 知乎 · 2021-01-10 · 赞同 0**
> 力扣：[807. 保持城市天际线](https://leetcode.cn/problems/max-increase-to-keep-city-skyline/) · Medium · 灵茶山艾府：[增加到行列最大值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

807.保持城市天际线

[力扣](https://leetcode-cn.com/problems/max-increase-to-keep-city-skyline/)

观察样例可以发现，所谓的天际线对于横向来说，就是每一行中的最大值，而对于竖向则是每一列中的最大值。那么对于位于一栋建筑，只要其加高之后的高度不超过其所在行和列中的最大值都是合法的。

于是可以首先对于矩阵的行列求出每一行的最大值max_row和每一列的最大值max_col，然后遍历整个矩阵，对于处于(x, y)上的建筑，其可以增加的高度就是

min(max_row[x], max_col[y]) - grid[x][y]

将这个值累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxIncreaseKeepingSkyline(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        max_row = [0] * m
        max_col = [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] > max_row[i]:
                    max_row[i] = grid[i][j]
                if grid[i][j] > max_col[j]:
                    max_col[j] = grid[i][j]
        

        res = 0
        for i in range(m):
            for j in range(n):
                res += min(max_row[i], max_col[j]) - grid[i][j]
        
        return res
```
