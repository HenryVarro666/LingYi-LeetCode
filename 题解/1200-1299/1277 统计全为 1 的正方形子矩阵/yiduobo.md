---
title: "1277. 统计全为1的正方形子矩阵"
aliases: ["yiduobo的每日leetcode 1277.统计全为1的正方形子矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/sliding-window", "leetcode/monotonic-stack", "题单/动态规划", "题单/单调栈", "题单/动态规划/七-其他线性-DP", "题单/单调栈/二-矩形"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388277921"
zhihu_id: "388277921"
zhihu_title: "yiduobo的每日leetcode 1277.统计全为1的正方形子矩阵"
question_id: "1277"
question: "统计全为 1 的正方形子矩阵"
problem_url: "https://leetcode.cn/problems/count-square-submatrices-with-all-ones/"
difficulty: "Medium"
created: "2021-07-09T21:45:10+08:00"
updated: "2021-07-09T21:45:10+08:00"
upvotes: 1
comments: 0
---

# 1277. 统计全为1的正方形子矩阵

> **[yiduobo的每日leetcode 1277.统计全为1的正方形子矩阵](https://zhuanlan.zhihu.com/p/388277921) · 知乎 · 2021-07-09 · 赞同 1**
> 力扣：[1277. 统计全为 1 的正方形子矩阵](https://leetcode.cn/problems/count-square-submatrices-with-all-ones/) · Medium · 灵茶山艾府：[三种方法：枚举上下边界 / 动态规划 / 单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1277.统计全为1的正方形子矩阵

[力扣](https://leetcode-cn.com/problems/count-square-submatrices-with-all-ones/)

经典的动态规划问题，令f[i][j]表示以(i, j)为右下角的全为1的正方形子矩阵的最大边长，那么对于f[i][j]：

1、若matrix[i][j]为0，那么f[i][j]必然为0。

2、若matrix[i][j]为1，且i或j等于0，那么f[i][j]就是1。

2、若matrix[i][j]为1，且i和j都大于0，那么我们可以从f[i - 1][j]、f[i][j - 1]以及f[i - 1][j - 1]中推断出f[i][j]。

例如样例中的右下角f[2][3]，该正方形的右侧边可以通过f[1][3]确定出来，而下边则可以通过f[2][2]确定出来。但是这样一来该正方形的左上角还无法确定，因此还需要通过f[i - 1][j - 1]来进行判断。

这样一来，就有f[i][j] \= min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1

遍历每个格子并进行动态规划，在遍历过程求解的过程中将所有的f[i][j]累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def countSquares(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        m = len(matrix)
        n = len(matrix[0])
        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    f[i][j] = matrix[i][j]
                elif j == 0:
                    f[i][j] = matrix[i][j]
                elif matrix[i][j] == 1:
                    f[i][j] = min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1

                res += f[i][j]
        
        return res
```
