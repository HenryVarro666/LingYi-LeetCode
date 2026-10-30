---
title: "311. 稀疏矩阵的乘法"
aliases: ["yiduobo的每日leetcode 311.稀疏矩阵的乘法"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595939499"
zhihu_id: "595939499"
zhihu_title: "yiduobo的每日leetcode 311.稀疏矩阵的乘法"
question_id: "311"
question: "稀疏矩阵的乘法"
problem_url: "https://leetcode.cn/problems/sparse-matrix-multiplication/"
created: "2023-01-02T03:26:17+08:00"
updated: "2023-01-02T03:26:17+08:00"
upvotes: 3
comments: 0
---

# 311. 稀疏矩阵的乘法

> **[yiduobo的每日leetcode 311.稀疏矩阵的乘法](https://zhuanlan.zhihu.com/p/595939499) · 知乎 · 2023-01-02 · 赞同 3**
> 力扣：[311. 稀疏矩阵的乘法](https://leetcode.cn/problems/sparse-matrix-multiplication/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

311.稀疏矩阵的乘法

[力扣](https://leetcode.cn/problems/sparse-matrix-multiplication/)

题目要求两个稀疏矩阵相乘的结果，由于数据规模比较小，因此直接使用常规的矩阵乘法也是可行的，不过在这里还有更好的做法。由于是稀疏矩阵，也就意味着两个矩阵中大部分元素都为0，而0本身是不会影响矩阵乘法的结果的，因此只需要对矩阵中不为0的值进行乘法操作。

对于mat1中的(i, j)这个位置上的数，其只会与mat2中第j行上的数进行乘法，而mat1[i][j]与mat2[j][p]的乘积将被累加到答案数组的(i, p)这个位置上，于是可以先使用哈希表将mat1的列上，以及mat2的行上的非零值分别收集起来，然后两两枚举，相乘之后累加到答案数组指定的位置上即可。

最后附上python代码：

```python
class Solution(object):
    def multiply(self, mat1, mat2):
        """
        :type mat1: List[List[int]]
        :type mat2: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(mat1)
        k = len(mat1[0])
        n = len(mat2[0])

        h1 = {}
        for i in range(m):
            for j in range(k):
                if mat1[i][j] != 0:
                    if j not in h1:
                        h1[j] = []
                    h1[j].append([i, mat1[i][j]])
        
        h2 = {}
        for j in range(k):
            for p in range(n):
                if mat2[j][p] != 0:
                    if j not in h2:
                        h2[j] = []
                    h2[j].append([p, mat2[j][p]])

        res = [[0] * n for _ in range(m)]
        for j in h1:
            for i, v1 in h1[j]:
                for p, v2 in h2.get(j, []):
                    res[i][p] += v1 * v2
        
        return res
```
