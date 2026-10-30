---
title: "73. 矩阵置零"
aliases: ["yiduobo的每日leetcode 73.矩阵置零"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/LeetCode-热题-100/矩阵", "题单/面试经典-150-题/矩阵"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/132737814"
zhihu_id: "132737814"
zhihu_title: "yiduobo的每日leetcode 73.矩阵置零"
question_id: "73"
question: "矩阵置零"
problem_url: "https://leetcode.cn/problems/set-matrix-zeroes/"
difficulty: "Medium"
created: "2020-04-17T23:41:52+08:00"
updated: "2020-04-17T23:41:52+08:00"
upvotes: 0
comments: 0
---

# 73. 矩阵置零

> **[yiduobo的每日leetcode 73.矩阵置零](https://zhuanlan.zhihu.com/p/132737814) · 知乎 · 2020-04-17 · 赞同 0**
> 力扣：[73. 矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/) · Medium · 灵茶山艾府：[一步步优化，从 O(m+n) 到 O(1) 空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

73.矩阵置零<https://leetcode-cn.com/problems/set-matrix-zeroes/>

比较基础的题目，不过原地算法要求常数空间这里倒是挺有意思的。

我的做法是用第0行与第0列中的数表示当前行是否需要置0。例如在matrix[i][j]位置上有一个0，那么就将matrix[i][0]与matrix[0][j]置为0，表示第i行与第j列都需要置0。

具体流程为：

1、扫描matrix，将0对应的行和列中的第0个元素置0。

2、扫描matrix的第0行与第0列，将其中0所在的列、行全部置为0。

这样做会有一个问题，就是在步骤2时，若matrix[0][0]为0，无法确定是第0行需要置0，还是第0列需要置0。于是我在这里添加了一个标记，表示第0列是否需要置0，然后matrix[0][0]则用来表示第0行是否需要置0。这样一来，所有需要置0的行与列就都能覆盖住了。

最终的时间复杂度为O(mn)，空间复杂度则是常数。

最后附上python代码，其中first_column即为第0列是否需要置0的标记：

```python
class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """

        m = len(matrix)
        n = len(matrix[0])

        first_column = False
        for i in range(m):
            if matrix[i][0] == 0:
                first_column = True
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if matrix[0][0] == 0:
            for i in range(n):
                matrix[0][i] = 0
        if first_column:
            for i in range(m):
                matrix[i][0] = 0

        return matrix
```
