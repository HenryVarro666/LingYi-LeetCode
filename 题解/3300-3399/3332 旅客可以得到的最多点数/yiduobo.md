---
title: "3332. 旅客可以得到的最多点数"
aliases: ["yiduobo的每日leetcode 3332.旅客可以得到的最多点数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24661356821"
zhihu_id: "24661356821"
zhihu_title: "yiduobo的每日leetcode 3332.旅客可以得到的最多点数"
question_id: "3332"
question: "旅客可以得到的最多点数"
problem_url: "https://leetcode.cn/problems/maximum-points-tourist-can-earn/"
difficulty: "Medium"
rating: 1828
created: "2025-02-18T23:56:24+08:00"
updated: "2025-02-18T23:56:37+08:00"
upvotes: 0
comments: 0
---

# 3332. 旅客可以得到的最多点数

> **[yiduobo的每日leetcode 3332.旅客可以得到的最多点数](https://zhuanlan.zhihu.com/p/24661356821) · 知乎 · 2025-02-18 · 赞同 0**
> 力扣：[3332. 旅客可以得到的最多点数](https://leetcode.cn/problems/maximum-points-tourist-can-earn/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3332.旅客可以得到的最多点数

[3332. 旅客可以得到的最多点数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-points-tourist-can-earn/description/)

题目给出两个整数n和k，以及两个二维整数数组stayScore和travelScore。一位旅客在一个有n座城市的国家旅游，所有城市都直接与其他城市相连。这位乘客会旅游恰好k天，且可以选择任意城市作为起点。

每一天这位旅客都可以选择留在当前城市，或者前往另一座城市。若在第i天留在当前城市curr，那么可以得到的点数为stayScore[i][curr]；若这位旅客从curr前往城市dest，那么可以得到的点数为travelScore[curr][dest]。

问这位旅客可以得到的最多点数。

动态规划是比较容易想到的。令f[t][now]表示第t天旅客位于城市now时可以得到的最大点数，那么对于f[t][now]：

1、旅客可能是在时刻t - 1已经在now，然后选择留在now，于是有

f[t][now] \= max(f[t][now], f[t - 1][now] + stayScore[t][now])

2、旅客也可能是在时刻t才从其他城市过来的，于是可以枚举所有不等于now的城市prev，于是有

f[t][now] \= max(f[t][now], f[t - 1][prev] + travelScore[prev][now])

最终答案即为max(f[k - 1])

另外注意到f每一轮的状态之和上一轮有关，在这里可以也使用滚动数组省去t这一维。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, n, k, stayScore, travelScore):
        """
        :type n: int
        :type k: int
        :type stayScore: List[List[int]]
        :type travelScore: List[List[int]]
        :rtype: int
        """
        
        f = [0] * n
        for t in range(k):
            g = f[:]
            f = [0] * n
            for now in range(n):
                f[now] = g[now] + stayScore[t][now]
                for prev in range(n):
                    if prev != now:
                        f[now] = max(f[now], g[prev] + travelScore[prev][now])
        
        return max(f)
```
