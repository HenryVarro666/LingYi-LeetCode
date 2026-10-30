---
title: "1582. 二进制矩阵中的特殊位置"
aliases: ["yiduobo的每日leetcode 1582.二进制矩阵中的特殊位置"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430279925"
zhihu_id: "430279925"
zhihu_title: "yiduobo的每日leetcode 1582.二进制矩阵中的特殊位置"
question_id: "1582"
question: "二进制矩阵中的特殊位置"
problem_url: "https://leetcode.cn/problems/special-positions-in-a-binary-matrix/"
difficulty: "Easy"
created: "2021-11-06T21:05:40+08:00"
updated: "2021-11-06T21:05:40+08:00"
upvotes: 0
comments: 0
---

# 1582. 二进制矩阵中的特殊位置

> **[yiduobo的每日leetcode 1582.二进制矩阵中的特殊位置](https://zhuanlan.zhihu.com/p/430279925) · 知乎 · 2021-11-06 · 赞同 0**
> 力扣：[1582. 二进制矩阵中的特殊位置](https://leetcode.cn/problems/special-positions-in-a-binary-matrix/) · Easy · 灵茶山艾府：[简单题，简单做，O(N^2) 时间 O(1) 空间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1582.二进制矩阵中的特殊位置

[力扣](https://leetcode-cn.com/problems/special-positions-in-a-binary-matrix/)

对于特殊位置而言，其所在的行和列上的数字之和必然都是1，因此可以先一趟遍历，计算矩阵中各行各列之和，然后再一趟遍历，若当前位置上的值为1，且其所在行和列的和都是1，那么该位置就是特殊位置了。

最后附上python代码：

```python
class Solution(object):
    def numSpecial(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])

        s_row = [0] * m
        s_col = [0] * n
        for i in range(m):
            for j in range(n):
                s_row[i] += mat[i][j]
                s_col[j] += mat[i][j]
        
        res = 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1 and s_row[i] == 1 and s_col[j] == 1:
                    res += 1
        
        return res
```
