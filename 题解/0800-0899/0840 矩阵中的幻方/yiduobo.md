---
title: "840. 矩阵中的幻方"
aliases: ["yiduobo的每日leetcode 840.矩阵中的幻方"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347096191"
zhihu_id: "347096191"
zhihu_title: "yiduobo的每日leetcode 840.矩阵中的幻方"
question_id: "840"
question: "矩阵中的幻方"
problem_url: "https://leetcode.cn/problems/magic-squares-in-grid/"
difficulty: "Medium"
created: "2021-01-27T20:52:36+08:00"
updated: "2021-01-27T20:52:36+08:00"
upvotes: 0
comments: 0
---

# 840. 矩阵中的幻方

> **[yiduobo的每日leetcode 840.矩阵中的幻方](https://zhuanlan.zhihu.com/p/347096191) · 知乎 · 2021-01-27 · 赞同 0**
> 力扣：[840. 矩阵中的幻方](https://leetcode.cn/problems/magic-squares-in-grid/) · Medium · 灵茶山艾府：[无需计算第三行列的和，以及对角线的和，数学证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

840.矩阵中的幻方

[力扣](https://leetcode-cn.com/problems/magic-squares-in-grid/)

由于矩阵的大小很小，因此可以直接枚举每一个可能的中心位置。由于幻方的中心必然为5，因此可以从第1行第1列开始枚举所有值等于5的位置，然后进行下列检测：

1、以该位置为中心的3\*3的小矩阵是否恰好使用了1到9这9个数字

2、以该位置为中心的3\*3的小矩阵的行、列以及对角线之和是否等于15。其中行列的计算相对简单，对角线则可以通过行数加上列数以及行数减去列数来进行判别

最后附上python代码：

```python
class Solution(object):
    def numMagicSquaresInside(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        res = 0

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if grid[i][j] == 5:
                    res += self.check(grid, i, j)
        
        return res

    def check(self, grid, x, y):
        nums = set(range(1, 10))
        row = [0] * 3
        col = [0] * 3
        left = right = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if grid[i][j] not in nums:
                    return 0
                nums.remove(grid[i][j])
                
                row[i - x + 1] += grid[i][j]
                col[j - y + 1] += grid[i][j]
                if i + j == x + y:
                    left += grid[i][j]
                if i - j == x - y:
                    right += grid[i][j]
        
        if left != 15 or right != 15:
            return 0
        if row[0] != 15 or row[1] != 15 or row[2] != 15:
            return 0
        if col[0] != 15 or col[1] != 15 or col[2] != 15:
            return 0

        return 1
```
