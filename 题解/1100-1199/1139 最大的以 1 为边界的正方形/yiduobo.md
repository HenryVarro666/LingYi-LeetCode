---
title: "1139. 最大的以1为边界的正方形"
aliases: ["yiduobo的每日leetcode 1139.最大的以1为边界的正方形"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/matrix", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377139689"
zhihu_id: "377139689"
zhihu_title: "yiduobo的每日leetcode 1139.最大的以1为边界的正方形"
question_id: "1139"
question: "最大的以 1 为边界的正方形"
problem_url: "https://leetcode.cn/problems/largest-1-bordered-square/"
difficulty: "Medium"
created: "2021-06-01T22:31:58+08:00"
updated: "2021-06-01T22:31:58+08:00"
upvotes: 0
comments: 0
---

# 1139. 最大的以1为边界的正方形

> **[yiduobo的每日leetcode 1139.最大的以1为边界的正方形](https://zhuanlan.zhihu.com/p/377139689) · 知乎 · 2021-06-01 · 赞同 0**
> 力扣：[1139. 最大的以 1 为边界的正方形](https://leetcode.cn/problems/largest-1-bordered-square/) · Medium · 灵茶山艾府：[【图解】前缀和轻松 AC！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1139.最大的以1为边界的正方形

[力扣](https://leetcode-cn.com/problems/largest-1-bordered-square/)

首先，我们可以在O(n^2)的时间复杂度预处理出从每个点开始向上、下、左、右这四个方向上延伸的连续1的长度。

由于题目要找的是最大的正方形，答案正方形的左上角和右下角节点必然是位于同一条对角线上的，因此我们可以枚举所有的对角线，然后问题就变成了给出一个数组a，求出a中的点对(a[i], a[j])，其需要满足min(a[i], a[j]) >\= j - i，同时j - i最大。理论上这个问题应该是可以利用单调栈在O(n)的时间复杂度内处理掉，那么一共最多2n条对角线，因此整体的时间复杂度就是O(n^2)。

不过这里的n最大只有100，因此我选择了比较偷懒的做法，直接枚举答案正方形的边长，然后枚举答案正方形的左上角，并通过左上角和边长计算出右下角，然后分别检测左上角向下和向右可以延伸的长度是否大于等于枚举的边长，以及右下角向上和向左可以延伸的长度是否大于等于枚举的边长。由于需要枚举边长和点，因此最终的时间复杂度为O(n^3)。

最后附上python代码：

```python
class Solution(object):
    def largest1BorderedSquare(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        left = [[0] * n for _ in range(m)]
        right = [[0] * n for _ in range(m)]
        up = [[0] * n for _ in range(m)]
        down = [[0] * n for _ in range(m)]

        for i in range(m):
            left[i][0] = grid[i][0]
            for j in range(1, n):
                if grid[i][j] == 1:
                    left[i][j] = left[i][j - 1] + 1
                else:
                    left[i][j] = 0
            
            right[i][n - 1] = grid[i][n - 1]
            for j in range(n - 2, -1, -1):
                if grid[i][j] == 1:
                    right[i][j] = right[i][j + 1] + 1
                else:
                    right[i][j] = 0
        
        for j in range(n):
            up[0][j] = grid[0][j]
            for i in range(1, m):
                if grid[i][j] == 1:
                    up[i][j] = up[i - 1][j] + 1
                else:
                    up[i][j] = 0
            
            down[m - 1][j] = grid[m - 1][j]
            for i in range(m - 2, -1, -1):
                if grid[i][j] == 1:
                    down[i][j] = down[i + 1][j] + 1
                else:
                    down[i][j] = 0

        for res in range(min(m, n), 0, -1):
            for i in range(m - res + 1):
                for j in range(n - res + 1):
                    if right[i][j] >= res and down[i][j] >= res and left[i + res - 1][j + res - 1] >= res and up[i + res - 1][j + res - 1] >= res:
                        return res * res
        
        return 0
```
