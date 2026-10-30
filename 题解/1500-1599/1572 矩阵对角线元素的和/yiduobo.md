---
title: "1572. 矩阵对角线元素的和"
aliases: ["yiduobo的每日leetcode 1572.矩阵对角线元素的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/428544079"
zhihu_id: "428544079"
zhihu_title: "yiduobo的每日leetcode 1572.矩阵对角线元素的和"
question_id: "1572"
question: "矩阵对角线元素的和"
problem_url: "https://leetcode.cn/problems/matrix-diagonal-sum/"
created: "2021-11-02T15:32:07+08:00"
updated: "2021-11-02T15:32:07+08:00"
upvotes: 0
comments: 0
---

# 1572. 矩阵对角线元素的和

> **[yiduobo的每日leetcode 1572.矩阵对角线元素的和](https://zhuanlan.zhihu.com/p/428544079) · 知乎 · 2021-11-02 · 赞同 0**
> 力扣：[1572. 矩阵对角线元素的和](https://leetcode.cn/problems/matrix-diagonal-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1572.矩阵对角线元素的和

[力扣](https://leetcode-cn.com/problems/matrix-diagonal-sum/)

比较基础的题目，直接遍历每一行并求和。对于第i行，其左对角线上的元素位于第i列，而右对角线上的元素则位于第n - i - 1列，其中n为矩阵的总行数。

除此之外，当n为奇数中，还需要注意矩阵的中心元素不能计算两次。

最后附上python代码：

```python
class Solution(object):
    def diagonalSum(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        n = len(mat)
        res = 0
        for i in range(n):
            res += mat[i][i]
            res += mat[i][n - i - 1]

        if n & 1:
            res -= mat[n / 2][n / 2]
        
        return res
```
