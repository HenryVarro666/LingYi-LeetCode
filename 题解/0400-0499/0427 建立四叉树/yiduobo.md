---
title: "427. 建立四叉树"
aliases: ["yiduobo的每日leetcode 427.建立四叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/195619387"
zhihu_id: "195619387"
zhihu_title: "yiduobo的每日leetcode 427.建立四叉树"
question_id: "427"
question: "建立四叉树"
problem_url: "https://leetcode.cn/problems/construct-quad-tree/"
created: "2020-08-23T16:53:27+08:00"
updated: "2020-08-23T16:53:27+08:00"
upvotes: 2
comments: 0
---

# 427. 建立四叉树

> **[yiduobo的每日leetcode 427.建立四叉树](https://zhuanlan.zhihu.com/p/195619387) · 知乎 · 2020-08-23 · 赞同 2**
> 力扣：[427. 建立四叉树](https://leetcode.cn/problems/construct-quad-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

427.建立四叉树<https://leetcode-cn.com/problems/construct-quad-tree/>

根据题目的意思，若当前矩阵中每个位置的值都为0或都为1，那么当前矩阵就是一个叶子节点，否则需要将当前矩阵分成四份然后继续递归求解。

对于判断每个位置的值是否都为0或者都为1，可以使用判断和的办法。若都为0，那么和自然是0。若都为1，那么和就是当前矩阵的面积。

于是可以先预处理出矩阵的和然后递归求解。对于矩阵的和，可以使用经典的sum[i][j]表示从左上角(0, 0)到(i, j)这个矩阵的和是多少。不过注意到这里保证了矩阵是正方形，且切分后的小矩阵也同样是正方形，那么边长必然是2的幂次，可以将其加入到状态中加速运算。经典的st算法就是运用了这个思想。简单起见，我这里还是用了老的计算方法。

最后附上python代码：

```python
"""
# Definition for a QuadTree node.
class Node(object):
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
"""

class Solution(object):
    def construct(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: Node
        """

        if not grid:
            return None

        n = len(grid)
        sum_matrix = grid[:]
        for i in range(n):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        sum_matrix[i][j] += sum_matrix[i][j - 1]
                elif j == 0:
                    sum_matrix[i][j] += sum_matrix[i - 1][j]
                else:
                    sum_matrix[i][j] += sum_matrix[i - 1][j] + sum_matrix[i][j - 1] - sum_matrix[i - 1][j - 1]

        return self.build(0, 0, n - 1, n - 1, sum_matrix)

    def build(self, x1, y1, x2, y2, sum_matrix):
        if x1 == 0:
            if y1 == 0:
                s = sum_matrix[x2][y2]
            else:
                s = sum_matrix[x2][y2] - sum_matrix[x2][y1 - 1]
        elif y1 == 0:
            s = sum_matrix[x2][y2] - sum_matrix[x1 - 1][y2]
        else:
            s = sum_matrix[x2][y2] - sum_matrix[x1 - 1][y2] - sum_matrix[x2][y1 - 1] + sum_matrix[x1 - 1][y1 - 1]

        if s == 0 or s == (x2 - x1 + 1) * (y2 - y1 + 1):
            if s == 0:
                val = 0
            else:
                val = 1
            return Node(val, True, None, None, None, None)

        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2
        topLeft = self.build(x1, y1, midx, midy, sum_matrix)
        topRight = self.build(x1, midy + 1, midx, y2, sum_matrix)
        bottomLeft = self.build(midx + 1, y1, x2, midy, sum_matrix)
        bottomRight = self.build(midx + 1, midy + 1, x2, y2, sum_matrix)
        return Node(0, False, topLeft, topRight, bottomLeft, bottomRight)
```
