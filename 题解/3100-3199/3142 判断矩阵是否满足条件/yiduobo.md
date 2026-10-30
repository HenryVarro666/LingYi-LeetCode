---
title: "3142. 判断矩阵是否满足条件"
aliases: ["yiduobo的每日leetcode 3142.判断矩阵是否满足条件"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703039444"
zhihu_id: "703039444"
zhihu_title: "yiduobo的每日leetcode 3142.判断矩阵是否满足条件"
question_id: "3142"
question: "判断矩阵是否满足条件"
problem_url: "https://leetcode.cn/problems/check-if-grid-satisfies-conditions/"
difficulty: "Easy"
created: "2024-06-12T23:12:51+08:00"
updated: "2024-06-12T23:12:51+08:00"
upvotes: 0
comments: 0
---

# 3142. 判断矩阵是否满足条件

> **[yiduobo的每日leetcode 3142.判断矩阵是否满足条件](https://zhuanlan.zhihu.com/p/703039444) · 知乎 · 2024-06-12 · 赞同 0**
> 力扣：[3142. 判断矩阵是否满足条件](https://leetcode.cn/problems/check-if-grid-satisfies-conditions/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3142.判断矩阵是否满足条件

[. - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-grid-satisfies-conditions/description/)

题目给出一个二维矩阵grid，要求判断其中每个格子grid[i][j]是否满足

1、如果grid[i + 1][j]存在，那么grid[i][j]需要等于grid[i + 1][j]

2、如果grid[i][j + 1]存在，那么grid[i][j]需要不等于grid[i][j + 1]

只需对grid一趟遍历，按照题目要求判断每个单元格是否符合条件即可。

最后附上python代码：

```python
class Solution(object):
    def satisfiesConditions(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if (i < m - 1 and grid[i][j] != grid[i + 1][j]) or (j < n - 1 and grid[i][j] == grid[i][j + 1]):
                    return False
        
        return True
```
