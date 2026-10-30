---
title: "2536. 子矩阵元素加1"
aliases: ["yiduobo的每日leetcode 2536.子矩阵元素加1"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637329557"
zhihu_id: "637329557"
zhihu_title: "yiduobo的每日leetcode 2536.子矩阵元素加1"
question_id: "2536"
question: "子矩阵元素加 1"
problem_url: "https://leetcode.cn/problems/increment-submatrices-by-one/"
difficulty: "Medium"
rating: 1583
created: "2023-06-16T20:12:08+08:00"
updated: "2023-06-16T20:12:08+08:00"
upvotes: 0
comments: 0
---

# 2536. 子矩阵元素加1

> **[yiduobo的每日leetcode 2536.子矩阵元素加1](https://zhuanlan.zhihu.com/p/637329557) · 知乎 · 2023-06-16 · 赞同 0**
> 力扣：[2536. 子矩阵元素加 1](https://leetcode.cn/problems/increment-submatrices-by-one/) · Medium · 灵茶山艾府：[【模板题】二维差分+二维前缀和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2536.子矩阵元素加1

[力扣](https://leetcode.cn/problems/increment-submatrices-by-one/)

离线的区间修改单点计算问题，可以使用差分数组来进行求解，不过对于本题，是二维的差分数组。

对于常规的一维差分数组，其基本思路是利用数组f储存后缀的变化量。例如对于区间[l, r]加上1，可以视为对区间[l, n]加上1，再将区间[r + 1, n]减去1，也就是将f[l]加上1，然后将f[r + 1]减去1。

而对于修改二维矩阵[(x1, y1)，(x2, y2)]的情况，则可以认为是将矩阵[(x1, y1), (m, n)]加上1，将区间[(x2 + 1, y1), (m, n)]以及区间[(x1, y2 + 1), (m, n)]减去1，再将矩阵[(x2 + 1, y2 + 1), (m ,n)]减去1。对应到二维差分数组中，就是将f[x1][y1]加上1，将f[x2 + 1][y1]以及f[x1][y2 + 1]减去1，然后将f[x2 + 1][y2 + 1]加上1。

处理完所有的添加操作后，则需要计算出最终的答案数组res，而res[i][j]的值就是f中二维矩阵[(0, 0), (i, j)]中所有元素之和。那么对于res的计算，就可以通过

res[i][j] \= res[i - 1][j] + res[i][j - 1] - res[i - 1][j - 1] + f[i][j]

来进行求解。

最后附上python代码：

```python
class Solution(object):
    def rangeAddQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[List[int]]
        """

        f = [[0] * (n + 1) for _ in range(n + 1)]
        for x1, y1, x2, y2 in queries:
            f[x1][y1] += 1
            f[x2 + 1][y1] -= 1
            f[x1][y2 + 1] -= 1
            f[x2 + 1][y2 + 1] += 1

        res = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        res[i][j] = f[i][j]
                    else:
                        res[i][j] = res[i][j - 1] + f[i][j]
                elif j == 0:
                    res[i][j] = res[i - 1][j] + f[i][j]
                else:
                    res[i][j] = res[i - 1][j] + res[i][j - 1] - res[i - 1][j - 1] + f[i][j]

        
        return res
```
