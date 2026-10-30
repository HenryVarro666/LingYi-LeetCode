---
title: "766. 托普利茨矩阵"
aliases: ["yiduobo的每日leetcode 766.托普利茨矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339102558"
zhihu_id: "339102558"
zhihu_title: "yiduobo的每日leetcode 766.托普利茨矩阵"
question_id: "766"
question: "托普利茨矩阵"
problem_url: "https://leetcode.cn/problems/toeplitz-matrix/"
created: "2020-12-23T22:00:39+08:00"
updated: "2020-12-23T22:00:39+08:00"
upvotes: 0
comments: 0
---

# 766. 托普利茨矩阵

> **[yiduobo的每日leetcode 766.托普利茨矩阵](https://zhuanlan.zhihu.com/p/339102558) · 知乎 · 2020-12-23 · 赞同 0**
> 力扣：[766. 托普利茨矩阵](https://leetcode.cn/problems/toeplitz-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

766.托普利茨矩阵

[力扣](https://leetcode-cn.com/problems/toeplitz-matrix/)

题目要求检测矩阵中左上到右下这条对角线上的数是否一致，那么可以跳出对角线的框框，从第二行开始，每次只检测一行。

对于当前行而言，第0个数是某条对角线的起点，无需检测。接下来从第1个数开始往后，若当前行的第i个数不等于上一行的第i - 1个数，那么就不合法。

最后附上python代码：

```python
class Solution(object):
    def isToeplitzMatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: bool
        """

        m = len(matrix)
        n = len(matrix[0])

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] != matrix[i - 1][j - 1]:
                    return False
        
        return True
```
