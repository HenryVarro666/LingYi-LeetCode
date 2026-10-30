---
title: "3546. 等和矩阵分割I"
aliases: ["yiduobo的每日leetcode 3546.等和矩阵分割I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907607381422081349"
zhihu_id: "1907607381422081349"
zhihu_title: "yiduobo的每日leetcode 3546.等和矩阵分割I"
question_id: "3546"
question: "等和矩阵分割 I"
problem_url: "https://leetcode.cn/problems/equal-sum-grid-partition-i/"
difficulty: "Medium"
created: "2025-05-21T22:06:23+08:00"
updated: "2025-05-21T22:06:23+08:00"
upvotes: 0
comments: 0
---

# 3546. 等和矩阵分割I

> **[yiduobo的每日leetcode 3546.等和矩阵分割I](https://zhuanlan.zhihu.com/p/1907607381422081349) · 知乎 · 2025-05-21 · 赞同 0**
> 力扣：[3546. 等和矩阵分割 I](https://leetcode.cn/problems/equal-sum-grid-partition-i/) · Medium · 灵茶山艾府：[枚举分割线的位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3546.等和矩阵分割I

[3546. 等和矩阵分割 I - 力扣（LeetCode）](https://leetcode.cn/problems/equal-sum-grid-partition-i/description/)

题目给出一个由正整数组成的大小为m \* n的矩阵grid，现在要求找出一条水平或者垂直的分割线，将其分为两个非空的矩阵，且这两个矩阵中元素之和相同。问能否找出这样的分割。

首先遍历grid中的每个元素，计算所有元素之和s。接下来分别考虑水平划分或者竖直划分。

对于水平划分，使用f[index]表示grid中第0到第index行中的元素之和，那么对于f[index]，就可以在f[index - 1]的基础上，再累加grid中第index行的所有元素。若某个f[index] \* 2恰好等于s，说明可以水平划分。

对于竖直划分，使用f[index]表示grid中第0到第index列中的元素之和，那么对于g[index]，就可以在g[index - 1]的基础上，再累加grid中第index列的所有元素。若某个g[index] \* 2恰好等于s，说明可以竖直划分。

若两种划分都不行，则返回false。

在具体实现上，由于f和g中每个元素之和上一个元素有关，同时也只是用了一次，因此可以使用变量迭代优化掉数组的空间。

最后附上python代码：

```python
class Solution(object):
    def canPartitionGrid(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """
        
        m = len(grid)
        n = len(grid[0])
        s = 0

        for i in range(m):
            for j in range(n):
                s += grid[i][j]
        
        now = 0
        for i in range(m - 1):
            for j in range(n):
                now += grid[i][j]
            
            if now + now == s:
                return True
            elif now + now > s:
                break
        
        now = 0
        for j in range(n - 1):
            for i in range(m):
                now += grid[i][j]
            
            if now + now == s:
                return True
            elif now + now > s:
                break
        
        return False
```
