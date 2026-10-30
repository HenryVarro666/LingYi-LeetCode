---
title: "308. 二维区域和检索"
aliases: ["yiduobo的每日leetcode 308.二维区域和检索"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595784783"
zhihu_id: "595784783"
zhihu_title: "yiduobo的每日leetcode 308.二维区域和检索"
question_id: "308"
question: "二维区域和检索"
problem_url: "https://leetcode.cn/problems/range-sum-query-2d-mutable/"
created: "2023-01-01T02:55:10+08:00"
updated: "2023-01-01T02:55:10+08:00"
upvotes: 0
comments: 0
---

# 308. 二维区域和检索

> **[yiduobo的每日leetcode 308.二维区域和检索](https://zhuanlan.zhihu.com/p/595784783) · 知乎 · 2023-01-01 · 赞同 0**
> 力扣：[308. 二维区域和检索](https://leetcode.cn/problems/range-sum-query-2d-mutable/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

308.二维区域和检索

[力扣](https://leetcode.cn/problems/range-sum-query-2d-mutable/)

经典的可变二维区间和问题，对于这类问题，常见的做法有两种，分别是二维st算法以及二维树状数组。我在这里采用的是后者。

与一维树状数组的思路类似，在这里也是将区间和转全为前缀和来进行处理，即左上角为(row1, col1)，右下角为(row2, col2)的二维区间可以认为是右下角为(row2, col2)、(row2，col1 - 1)、(row1 - 1，col2)、(row1 - 1，col1 - 1)，左上角都是(1, 1)的前缀区间通过加减得到，而对于二维前缀和问题，则可以使用二维树状数组来进行求解了。

具体实现上，则只需仿照一维树状数组，使用两重循环分别迭代两个坐标就行了。

最后附上python代码：

```python
class NumMatrix(object):

    def add(self, x, y, v):
        tmp = y
        while x <= self.m:
            y = tmp
            while y <= self.n:
                self.f[x][y] += v
                y += y & -y

            x += x & -x

    def __init__(self, matrix):
        """
        :type matrix: List[List[int]]
        """
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.f = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        self.matrix = [[0] * self.n for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.add(i + 1, j + 1, matrix[i][j])
                self.matrix[i][j] = matrix[i][j]

    def update(self, row, col, val):
        """
        :type row: int
        :type col: int
        :type val: int
        :rtype: None
        """
        delta = val - self.matrix[row][col]
        self.matrix[row][col] = val
        self.add(row + 1, col + 1, delta)

    def get(self, x, y):
        res = 0
        tmp = y
        while x > 0:
            y = tmp
            while y > 0:
                res += self.f[x][y]
                y -= y & -y
            
            x -= x & -x

        return res

    def sumRegion(self, row1, col1, row2, col2):
        """
        :type row1: int
        :type col1: int
        :type row2: int
        :type col2: int
        :rtype: int
        """
        return self.get(row2 + 1, col2 + 1) - self.get(row2 + 1, col1) - self.get(row1, col2 + 1) + self.get(row1, col1)

# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# obj.update(row,col,val)
# param_2 = obj.sumRegion(row1,col1,row2,col2)
```
