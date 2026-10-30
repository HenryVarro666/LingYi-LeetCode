---
title: "576. 出界的路劲数"
aliases: ["yiduobo的每日leetcode 576.出界的路劲数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266885456"
zhihu_id: "266885456"
zhihu_title: "yiduobo的每日leetcode 576.出界的路劲数"
question_id: "576"
question: "出界的路劲数"
problem_url: "https://leetcode.cn/problems/out-of-boundary-paths/"
created: "2020-10-19T22:43:52+08:00"
updated: "2020-10-19T22:43:52+08:00"
upvotes: 0
comments: 0
---

# 576. 出界的路劲数

> **[yiduobo的每日leetcode 576.出界的路劲数](https://zhuanlan.zhihu.com/p/266885456) · 知乎 · 2020-10-19 · 赞同 0**
> 力扣：[576. 出界的路劲数](https://leetcode.cn/problems/out-of-boundary-paths/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

576.出界的路径数<https://leetcode-cn.com/problems/out-of-boundary-paths/>

拿到题目感觉可以用组合数学的方法直接算出来，但是推了老半天也没想出来，最后只能老老实实用动态规划来做。

为了避免重复，我在这里采用的是f[k][x][y]表示从x行y列开始，移动k次之后移除界的操作总数。这个状态表示意味着对于f[k][x][y]，其前k - 1步操作都必须保证球在界内，而最后一步操作时才将球移出界外，那么就有

f[k][x][y] \= f[k - 1][x - 1][y] + f[k - 1][x + 1][y] + f[k - 1][x][y - 1] + f[k -1][x][y + 1]

分别表示第一步往上、下、左、右进行移动。当然，这里的目标位置必须是位于界内的。

在循环计算的过程中，应该将所有的f[k][i][j]累加到答案当中去，因为题目并不要求用完全部的步数。

由于每一轮的状态只与上一轮的状态有关，因此可以使用滚动数组，但是更新的方式较为复杂，因此使用的是01形式的滚动数组。

最后附上python代码：

```python
class Solution(object):
    def findPaths(self, m, n, N, i, j):
        """
        :type m: int
        :type n: int
        :type N: int
        :type i: int
        :type j: int
        :rtype: int
        """

        if N == 0:
            return 0

        x = i
        y = j
        f = [[[0] * n for _ in range(m)] for _ in range(2)]

        for i in range(m):
            f[1][i][0] += 1
            f[1][i][n - 1] += 1
        for j in range(n):
            f[1][0][j] += 1
            f[1][m - 1][j] += 1

        res = f[1][x][y]
        mod = 10 ** 9 + 7
        for k in range(2, N + 1):
            now = k % 2
            last = 1 - now
            for i in range(m):
                for j in range(n):
                    f[now][i][j] = 0
                    if i > 0:
                        f[now][i][j] += f[last][i - 1][j]
                    if i < m - 1:
                        f[now][i][j] += f[last][i + 1][j]
                    if j > 0:
                        f[now][i][j] += f[last][i][j - 1]
                    if j < n - 1:
                        f[now][i][j] += f[last][i][j + 1]
                    f[now][i][j] %= mod
            res += f[now][x][y]
            res %= mod
        return res
```
