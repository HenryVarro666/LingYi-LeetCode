---
title: "304. 二维区域和检索"
aliases: ["yiduobo的每日leetcode 304.二维区域和检索"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/matrix", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158216830"
zhihu_id: "158216830"
zhihu_title: "yiduobo的每日leetcode 304.二维区域和检索"
question_id: "304"
question: "二维区域和检索 - 矩阵不可变"
problem_url: "https://leetcode.cn/problems/range-sum-query-2d-immutable/"
difficulty: "Medium"
created: "2020-07-09T22:50:29+08:00"
updated: "2020-07-09T22:50:29+08:00"
upvotes: 0
comments: 0
---

# 304. 二维区域和检索

> **[yiduobo的每日leetcode 304.二维区域和检索](https://zhuanlan.zhihu.com/p/158216830) · 知乎 · 2020-07-09 · 赞同 0**
> 力扣：[304. 二维区域和检索 - 矩阵不可变](https://leetcode.cn/problems/range-sum-query-2d-immutable/) · Medium · 灵茶山艾府：[【图解】一张图秒懂二维前缀和！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

304.二维区域和检索<https://leetcode-cn.com/problems/range-sum-query-2d-immutable/>

上一题的二维版本，做法也类似，不过前缀和对应的是一维数组，在二维的情况下，需要维护的是从矩阵左上角(0, 0)到当前位置(x, y)这个矩阵中所有数的和。

那么对于求解sumRegion(x1, y1, x2, y2)，我们就可以通过

sum[x2][y2] - sum[x2][y1 - 1] - sum[x1 - 1][y2] + sum[x1 - 1][y1 - 1]

来得到答案，具体原理也跟上一题类似：

sum[x2][y2] \= matrix[0][0] + matrix[0][1] + ... + matrix[0][y2] +

matrix[1][0] + matrix[1][1] + ... + matrix[1][y2] +

... +

matrix[x2][0] + matrix[x2][1] + ... + matrix[x2][y2]

那么需要得到sumRegion(x1, y1, x2, y2)，就需要从sum[x2][y2]中去除掉

S1 \= matrix[0][0] + matrix[0][1] + ... + matrix[0][y2] +

matrix[1][0] + matrix[1][1] + ... + matrix[1][y2] +

... +

matrix[x1 - 1][0] + matrix[x1 - 1][1] + ... + matrix[x1 - 1][y2]

S2 \= matrix[x1][0] + matrix[x1][1] + ... + matrix[x1][y1 - 1] +

... +

matrix[x2][0] + matrix[x2][1] + ... + matrix[x2][y1 - 1]

这两个部分。可以发现，S1正好就是sum[x1 - 1][y2]，于是还剩下后面的S2需要处理。

这里可以把matrix[0][0]到matrix[x1 - 1][y1 - 1]再补上来，即

S3 \= matrix[0][0] + matrix[0][1] + ... + matrix[0][y1 - 1] +

... +

matrix[x1 - 1][0] + matrix[x1 - 1][1] + ... + matrix[x1 - 1][y1 - 1]

S2 \= matrix[x1][0] + matrix[x1][1] + ... + matrix[x1][y1 - 1] +

... +

matrix[x2][0] + matrix[x2][1] + ... + matrix[x2][y1 - 1]

那么S2 + S3就正好是sum[x2][y1 - 1]，而S3则是sum[x1 - 1][y1 - 1]

于是最后答案

sumRegion(x1, y1, x2, y2) \= sum[x2][y2] - S1 - S2

\= sum[x2][y2] - sum[x1 - 1][y2] - (S2 + S3) + S3

\= sum[x2][y2] - sum[x1 - 1][y2] - sum[x2][y1 - 1] + sum[x1 - 1][y1 - 1]

那么现在的问题就是如何高效的生成sum[x][y]。具体做法其实与求解sumRegion也类似，即

sum[x][y] \= sum[x][y - 1] + sum[x - 1][y] - sum[x - 1][y - 1]

另外，在预处理以及求解的过程中都需要注意x或y等于0的情况。

最后附上python代码：

```python
class NumMatrix(object):

    def __init__(self, matrix):
        """
        :type matrix: List[List[int]]
        """
        self.sum_matrix = matrix[:]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        self.sum_matrix[i][j] += self.sum_matrix[i][j - 1]
                elif j == 0:
                    self.sum_matrix[i][j] += self.sum_matrix[i - 1][j]
                else:
                    self.sum_matrix[i][j] += self.sum_matrix[i - 1][j] + self.sum_matrix[i][j - 1] - self.sum_matrix[i - 1][j - 1]        

    def sumRegion(self, row1, col1, row2, col2):
        """
        :type row1: int
        :type col1: int
        :type row2: int
        :type col2: int
        :rtype: int
        """
        if row1 == 0:
            if col1 == 0:
                return self.sum_matrix[row2][col2]
            else:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row2][col1 - 1]
        else:
            if col1 == 0:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row1 - 1][col2]
            else:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row2][col1 - 1] - self.sum_matrix[row1 - 1][col2] + self.sum_matrix[row1 - 1][col1 - 1]

# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)
```
