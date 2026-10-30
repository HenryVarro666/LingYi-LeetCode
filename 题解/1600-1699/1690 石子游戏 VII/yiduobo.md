---
title: "1690. 石子游戏VII"
aliases: ["yiduobo的每日leetcode 1690.石子游戏VII"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/数学算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446829234"
zhihu_id: "446829234"
zhihu_title: "yiduobo的每日leetcode 1690.石子游戏VII"
question_id: "1690"
question: "石子游戏 VII"
problem_url: "https://leetcode.cn/problems/stone-game-vii/"
difficulty: "Medium"
rating: 1951
created: "2021-12-17T23:22:09+08:00"
updated: "2021-12-17T23:22:09+08:00"
upvotes: 0
comments: 0
---

# 1690. 石子游戏VII

> **[yiduobo的每日leetcode 1690.石子游戏VII](https://zhuanlan.zhihu.com/p/446829234) · 知乎 · 2021-12-17 · 赞同 0**
> 力扣：[1690. 石子游戏 VII](https://leetcode.cn/problems/stone-game-vii/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1690.石子游戏VII

[力扣](https://leetcode-cn.com/problems/stone-game-vii/)

对于这类区间从两侧向中间操作的问题，经典的做法就是动态规划。令f[i][j]表示区间i到j的某种最值，然后状态转移时就分别考虑操作i或者操作j，然后利用这个操作的代价以及f[i - 1][j]或f[i][j - 1]来更新f[i][j]。

对于本题而言，f[i][j]表示的自然就是石子i到石子j，先手比后手得分的差值。那么对于f[i][j]：

1、如果先手取第i颗石子，那么本次操作的收益就是stone[i + 1] + stone[i + 2] + ... + stone[j]。这是一个区间和问题，可以利用前缀和来优化。除此之外，后手在石子i + 1到石子j上的得分将比先手多出f[i + 1][j]。这里的理解是先手拿了第i颗石子后，此时后手变成了先手，面对的是第i + 1颗石子到第j颗石子，因此对应的状态就是f[i + 1][j]。

综合起来，此时的f[i][j] \= min(f[i][j], prefix_s[j] - prefix[i] - f[i + 1][j])

2、如果先手取第j可石子，那么本次的收益就是prefix[j - 1] - prefix[i - 1]，而后手在石子i到石子j - 1上的得分将比先手多出f[i][j - 1]，因此

f[i][j] \= min(f[i][j], prefix_s[j - 1] - prefix_s[i - 1] - f[i][j - 1])

由于这里需要预先处理好长度较短的区间，因此具体实现时需要先从短到长枚举区间长度l，然后枚举区间左边界i，通过i + l - 1计算出区间右边界j然后计算f[i][j]。

最后附上python代码：

```python
class Solution(object):
    def stoneGameVII(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """

        s = [0]
        for stone in stones:
            s.append(s[-1] + stone)

        n = len(stones)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for length in range(1, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                if i == j:
                    f[i][j] = 0
                else:
                    f[i][j] = max(s[j] - s[i] - f[i + 1][j], s[j - 1] - s[i - 1] - f[i][j - 1])
        
        return f[1][n]
```
