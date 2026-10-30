---
title: "688. \"马\"在棋盘上的概率"
aliases: ["yiduobo的每日leetcode 688.\"马\"在棋盘上的概率"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/十五-概率-DP-期望-DP", "题单/数学算法/三-概率期望"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/305880428"
zhihu_id: "305880428"
zhihu_title: "yiduobo的每日leetcode 688.\"马\"在棋盘上的概率"
question_id: "688"
question: "骑士在棋盘上的概率"
problem_url: "https://leetcode.cn/problems/knight-probability-in-chessboard/"
difficulty: "Medium"
created: "2020-11-22T14:41:40+08:00"
updated: "2020-11-22T14:41:40+08:00"
upvotes: 0
comments: 0
---

# 688. "马"在棋盘上的概率

> **[yiduobo的每日leetcode 688."马"在棋盘上的概率](https://zhuanlan.zhihu.com/p/305880428) · 知乎 · 2020-11-22 · 赞同 0**
> 力扣：[688. 骑士在棋盘上的概率](https://leetcode.cn/problems/knight-probability-in-chessboard/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

688.马在棋盘上的概率

[力扣](https://leetcode-cn.com/problems/knight-probability-in-chessboard/)

感觉应该有组合数学的做法，但是没有想出来，只能老老实实用动态规划来做。

设f[k][i][j]表示从棋盘上的(i, j)开始起跳，经过k轮之后仍在棋盘上的概率。

对于每个f[k][i][j]，我们枚举下一步可能跳到的位置(next_i, next_j)，若这个位置在棋盘内，那么f[k][i][j] +\= f[k - 1][next_i][next_j]。在枚举完所有的八种跳法之后，将f[k][i][j]除以8。在处理完所有k轮之后，最终答案就是f[k][r][c]。

注意到这里每一轮的结果只跟上一轮的结果有关，因此可以将k这一维变为01的形式。

最后附上python代码：

```python
class Solution(object):
    def knightProbability(self, N, K, r, c):
        """
        :type N: int
        :type K: int
        :type r: int
        :type c: int
        :rtype: float
        """

        f = [[[1] * N for _ in range(N)], [[0] * N for _ in range(N)]]
        dx = [2, 1, -1, -2, -2, -1, 1, 2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]

        for k in range(1, K + 1):
            now = k & 1
            last = now ^ 1
            for i in range(N):
                for j in range(N):
                    f[now][i][j] = 0.0
                    for index in range(8):
                        next_i = i + dx[index]
                        next_j = j + dy[index]
                        if next_i >= 0 and next_i < N and next_j >= 0 and next_j < N:
                            f[now][i][j] += f[last][next_i][next_j]
                    f[now][i][j] /= 8.0
        
        return f[K & 1][r][c]
```
