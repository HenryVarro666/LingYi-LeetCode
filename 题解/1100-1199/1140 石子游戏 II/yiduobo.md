---
title: "1140. 石子游戏II"
aliases: ["yiduobo的每日leetcode 1140.石子游戏II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/game-theory", "leetcode/monotonic-queue", "题单/动态规划", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377141647"
zhihu_id: "377141647"
zhihu_title: "yiduobo的每日leetcode 1140.石子游戏II"
question_id: "1140"
question: "石子游戏 II"
problem_url: "https://leetcode.cn/problems/stone-game-ii/"
difficulty: "Medium"
rating: 2035
created: "2021-06-01T22:38:06+08:00"
updated: "2021-06-01T22:38:06+08:00"
upvotes: 1
comments: 0
---

# 1140. 石子游戏II

> **[yiduobo的每日leetcode 1140.石子游戏II](https://zhuanlan.zhihu.com/p/377141647) · 知乎 · 2021-06-01 · 赞同 1**
> 力扣：[1140. 石子游戏 II](https://leetcode.cn/problems/stone-game-ii/) · Medium · 灵茶山艾府：[动态规划：从 O(n^3) 到 O(n^2)，单调队列优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1140.石子游戏II

[力扣](https://leetcode-cn.com/problems/stone-game-ii/)

由于题目中的操作是拿走前X堆石子，拿着摆明了就是动态规划的问题。令f[i][j]表示从第i堆石子开始，当前的M等于j时，先手最多可以拿到多少石子。那么对于f[i][j]：

1、若i + j \* 2 >\= n，此时先手可以拿走后面所有的石头，因此有f[i][j] \= sum(piles[i:])

2、若i + j \* 2 \< n，那么我们需要从1到j \* 2之间枚举本次拿走的石子堆数k。拿完之后，后手下一步开始能拿的最多石子数量就是f[i + k][max(j, k)]，因此先手拿到的石子数量就是

f[i][j] \= max(f[i][j], sum(piles[i:] - f[i + k][max(j, k)])

注意到这里的f[i][j]在状态转移时依赖f[i + k]相关的状态，因此我们应该从后向前进行计算，同时这里的piles[i:]只与i有关，因此可以使用一个变量来迭代，而不需要提前预处理区间和。

动态规划完成后，f[0][1]就是最终的答案。

最后附上python代码：

```python
class Solution(object):
    def stoneGameII(self, piles):
        """
        :type piles: List[int]
        :rtype: int
        """

        n = len(piles)
        f = [[0] * (n + 1) for _ in range(n)]
        s = 0
        for i in range(n - 1, -1, -1):
            s += piles[i]
            for j in range(1, n + 1):
                if i + j * 2 >= n:
                    f[i][j] = s
                else:
                    for k in range(1, j * 2 + 1):
                        f[i][j] = max(f[i][j], s - f[i + k][max(j, k)])

        return f[0][1]
```
