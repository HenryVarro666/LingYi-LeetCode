---
title: "2218. 从栈中取出K个硬币的最大面值和"
aliases: ["yiduobo的每日leetcode 2218.从栈中取出K个硬币的最大面值和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/541674068"
zhihu_id: "541674068"
zhihu_title: "yiduobo的每日leetcode 2218.从栈中取出K个硬币的最大面值和"
question_id: "2218"
question: "从栈中取出 K 个硬币的最大面值和"
problem_url: "https://leetcode.cn/problems/maximum-value-of-k-coins-from-piles/"
difficulty: "Hard"
rating: 2158
created: "2022-07-14T19:12:16+08:00"
updated: "2022-07-14T19:12:16+08:00"
upvotes: 1
comments: 0
---

# 2218. 从栈中取出K个硬币的最大面值和

> **[yiduobo的每日leetcode 2218.从栈中取出K个硬币的最大面值和](https://zhuanlan.zhihu.com/p/541674068) · 知乎 · 2022-07-14 · 赞同 1**
> 力扣：[2218. 从栈中取出 K 个硬币的最大面值和](https://leetcode.cn/problems/maximum-value-of-k-coins-from-piles/) · Hard · 灵茶山艾府：[转化成分组背包：记忆化搜索 / 递推 / 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2218.从栈中取出K个硬币的最大面值和

[力扣](https://leetcode.cn/problems/maximum-value-of-k-coins-from-piles/)

经典的动态规划问题，令f[i][j]表示前i堆硬币，操作j次可以得到的最大面值，那么对于f[i][j]，就可以尝试对第i - 1堆硬币操作0到min(j, len(piles[i - 1]))次，对应的面值和则为

0: f[i - 1][j]

1: f[i - 1][j - 1] + piles[i - 1][0]

2: f[i - 1][j - 2] + piles[i - 1][0] + piles[i - 1][1]

...

依次类推

可以发现，转移方程中关于piles[i - 1]的项可以使用前缀和来进行预处理，记s[i - 1][j] \= s[i - 1][0] + s[i - 1][1] + ... + s[i - 1][j]，那么就有

f[i][j] \= max(f[i - 1][j], f[i - 1][j - c] + s[i - 1][c - 1])，这里的c表示操作次数，取值范围为1 \<\= c \<\= min(j, len(piles[i - 1]))

这样一来，就可以在O(k \* sum(piles[i].length))的复杂度内求出最终答案了。

另外，在这里每一轮的状态只与上一轮有关，因此可以利用反向遍历操作次数来滚动f，从而省略掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def maxValueOfCoins(self, piles, k):
        """
        :type piles: List[List[int]]
        :type k: int
        :rtype: int
        """

        f = [0] * (k + 1)
        for pile in piles:
            s = [pile[0]]
            for coin in pile[1:]:
                s.append(s[-1] + coin)
                
            for j in range(k, -1, -1):
                for c in range(1, min(j, len(s)) + 1):
                    f[j] = max(f[j], f[j - c] + s[c - 1])

        return f[-1]
```
