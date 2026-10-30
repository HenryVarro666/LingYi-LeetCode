---
title: "3418. 机器人可以获得的最大金币数"
aliases: ["yiduobo的每日leetcode 3418.机器人可以获得的最大金币数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32724571577"
zhihu_id: "32724571577"
zhihu_title: "yiduobo的每日leetcode 3418.机器人可以获得的最大金币数"
question_id: "3418"
question: "机器人可以获得的最大金币数"
problem_url: "https://leetcode.cn/problems/maximum-amount-of-money-robot-can-earn/"
difficulty: "Medium"
rating: 1798
created: "2025-03-25T22:56:20+08:00"
updated: "2025-03-25T22:56:20+08:00"
upvotes: 1
comments: 0
---

# 3418. 机器人可以获得的最大金币数

> **[yiduobo的每日leetcode 3418.机器人可以获得的最大金币数](https://zhuanlan.zhihu.com/p/32724571577) · 知乎 · 2025-03-25 · 赞同 1**
> 力扣：[3418. 机器人可以获得的最大金币数](https://leetcode.cn/problems/maximum-amount-of-money-robot-can-earn/) · Medium · 灵茶山艾府：[三种写法：记忆化搜索 / 递推 / 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3418.机器人可以获得的最大金币数

[3418. 机器人可以获得的最大金币数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-amount-of-money-robot-can-earn/description/)

题目给出一个m \* n的网格coins[i][j]，一个机器人将从网格的左上角(0, 0)出发向右下角(m - 1, n - 1)行走，行走过程中只能向右或者向下移动。

对于网格中的某个单元格coins[i][j]，若coins[i][j] >\= 0，说明机器人可以获得该单元格的金币，若coins[i][j] \< 0，机器人将会遇到一个强盗，强盗将会抢走abs(coins[i][j])的金币。机器人在行走过程中金币的数量可以为负。

机器人有一项特殊能力，可以感化最多两个单元格的强盗，防止金币被抢走。问如何行走才能使得获得的金币数量最大。

如果不考虑机器人的感化能力，那么本题就是经典的动态规划问题。

令f[i][j]表示走到单元格(i, j)可以得到的最大金币数量，然后对于f[i][j]，其可以从上方或者左侧走过来，于是有f[i][j] \= max(f[i - 1][j], f[i][j - 1] + coins[i][j]。另外需要特别注意i或j贴着边的情况。

对于本题，由于感化的次数有限，于是可以考虑将感化的次数也加入到状态表示中。令f[i][j]、g[i][j]、h[i][j]分别表示走到单元格(i, j)，且还有两次、一次、零次感化的机会时可以获得的最大金币数量，那么对于coins[i][j] >\= 0的单元格，f[i][j]、g[i][j]、h[i][j]的更新方式保持不变；对于coins[i][j] \< 0的单元格，f[i][j]的更新方式依然保持不变，而g[i][j]和h[i][j]则可以在之前更新方式的基础上选择感化强盗，也就是说g[i][j]还可以从max(f[i - 1][j], f[i][j - 1])得到，而h[i][j]还可以从max(g[i - 1][j], g[i][j - 1])得到。

计算完成后，最终答案就是h[-1][-1]。

最后附上python代码：

```python
class Solution(object):
    def maximumAmount(self, coins):
        """
        :type coins: List[List[int]]
        :rtype: int
        """
        
        m = len(coins)
        n = len(coins[0])

        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]
        h = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = coins[i][j]
                        if coins[i][j] < 0:
                            g[i][j] = 0
                            h[i][j] = 0
                        else:
                            g[i][j] = coins[i][j]
                            h[i][j] = coins[i][j]
                    
                    else:
                        f[i][j] = f[i][j - 1] + coins[i][j]
                        if coins[i][j] >= 0:
                            g[i][j] = g[i][j - 1] + coins[i][j]
                            h[i][j] = h[i][j - 1] + coins[i][j]
                        else:
                            g[i][j] = max(f[i][j - 1], g[i][j - 1] + coins[i][j])
                            h[i][j] = max(g[i][j - 1], h[i][j - 1] + coins[i][j])

                elif j == 0:
                    f[i][j] = f[i - 1][j] + coins[i][j]
                    if coins[i][j] >= 0:
                        g[i][j] = g[i - 1][j] + coins[i][j]
                        h[i][j] = h[i - 1][j] + coins[i][j]
                    else:
                        g[i][j] = max(f[i - 1][j], g[i - 1][j] + coins[i][j])
                        h[i][j] = max(g[i - 1][j], h[i - 1][j] + coins[i][j])
                
                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1]) + coins[i][j]
                    if coins[i][j] >= 0:
                        g[i][j] = max(g[i - 1][j], g[i][j - 1]) + coins[i][j]
                        h[i][j] = max(h[i - 1][j], h[i][j - 1]) + coins[i][j]
                    else:
                        g[i][j] = max(max(f[i - 1][j], f[i][j - 1]), max(g[i - 1][j], g[i][j - 1]) + coins[i][j])
                        h[i][j] = max(max(g[i - 1][j], g[i][j - 1]), max(h[i - 1][j], h[i][j - 1]) + coins[i][j])
        
        return h[-1][-1]
```
