---
title: "2319. 判断矩阵是否是一个X矩阵"
aliases: ["yiduobo的每日leetcode 2319.判断矩阵是否是一个X矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557090394"
zhihu_id: "557090394"
zhihu_title: "yiduobo的每日leetcode 2319.判断矩阵是否是一个X矩阵"
question_id: "2319"
question: "判断矩阵是否是一个 X 矩阵"
problem_url: "https://leetcode.cn/problems/check-if-matrix-is-x-matrix/"
difficulty: "Easy"
created: "2022-08-23T23:03:45+08:00"
updated: "2022-08-23T23:03:45+08:00"
upvotes: 0
comments: 0
---

# 2319. 判断矩阵是否是一个X矩阵

> **[yiduobo的每日leetcode 2319.判断矩阵是否是一个X矩阵](https://zhuanlan.zhihu.com/p/557090394) · 知乎 · 2022-08-23 · 赞同 0**
> 力扣：[2319. 判断矩阵是否是一个 X 矩阵](https://leetcode.cn/problems/check-if-matrix-is-x-matrix/) · Easy · 灵茶山艾府：[简洁写法（Python 一行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2319.判断矩阵是否是一个X矩阵

[力扣](https://leetcode.cn/problems/check-if-matrix-is-x-matrix/)

题目对于X矩阵的定义是对角线上的数不为0，其他位置上的数全为0，那么需要先想办法判断哪些格子是对角线上的格子。观察题目给出的样例，可以发现左对角线上的格子都满足横纵坐标相等，而右对角线上的格子则满足横纵坐标之和刚好等于n - 1，接下来只需遍历矩阵中的每个格子进行判断就行了。

最后附上python代码：

```python
class Solution(object):
    def checkXMatrix(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        n = len(grid)
        for i in range(n):
            for j in range(n):
                if i == j or i + j == n - 1:
                    if grid[i][j] == 0:
                        return False
                elif grid[i][j] != 0:
                    return False
        
        return True
```
