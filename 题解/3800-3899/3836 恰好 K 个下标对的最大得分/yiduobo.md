---
title: "3836. 恰好K个下标对的最大得分"
aliases: ["yiduobo的每日leetcode 3836.恰好K个下标对的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2003943605518213150"
zhihu_id: "2003943605518213150"
zhihu_title: "yiduobo的每日leetcode 3836.恰好K个下标对的最大得分"
question_id: "3836"
question: "恰好 K 个下标对的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-using-exactly-k-pairs/"
difficulty: "Hard"
rating: 1988
created: "2026-02-09T21:19:25+08:00"
updated: "2026-02-09T21:19:28+08:00"
upvotes: 0
comments: 0
---

# 3836. 恰好K个下标对的最大得分

> **[yiduobo的每日leetcode 3836.恰好K个下标对的最大得分](https://zhuanlan.zhihu.com/p/2003943605518213150) · 知乎 · 2026-02-09 · 赞同 0**
> 力扣：[3836. 恰好 K 个下标对的最大得分](https://leetcode.cn/problems/maximum-score-using-exactly-k-pairs/) · Hard · 灵茶山艾府：[子序列 DP，从记忆化搜索到递推，循环次数优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3836.恰好K个下标对的最大得分

<https://leetcode.cn/problems/maximum-score-using-exactly-k-pairs/description/>

题目给出两个长度分别为n和m的整数数组nums1和nums2，以及一个整数k。其中n和m都不超过100，k不超过min(n, m)。

现在要求选出恰好k组下标对，(i[1], j[1]), (i[2], j[2]), ..., (i[k], j[k])，满足

0 \<\= i[1] \< i[2] \< ... \< i[k] \< n

0 \<\= j[1] \< j[2] \< ... \< j[k] \< m

对于每组(i, j)，将获得nums1[i] \* num2[j]的得分。

问最大可能获得的得分是多少。

由于题目的数据规模较小，因此可以考虑最直观的动态规划：令f[i][j][t]表示从nums1的前i个数，nums2的前j个数中选出t组可以得到的最大得分，那么对于f[i][j][t]：

1、如果保留nums1[i]以及nums2[j]，那么就有

f[i][j][t] \= f[i - 1][j - 1][t - 1] + nums1[i + 1] \* nums2[j + 1]

需要注意最后的+1是因为定义的是第i个数以及第j个数，从1开始计数，而nums1和num2的下标是从0开始的

2、如果不保留nums1[i]，那么就有

f[i][j][t] \= f[i - 1][j][t]

3、同理，如果不保留nums2[j]，那么就有

f[i][j][t] \= f[i][j - 1][t]

取以上三者的最大值作为最终的f[i][j][t]即可。需要注意，这里有一个前提是前置状态必须是存在的。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums1)
        m = len(nums2)

        f = [[[None] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]
        f[0][0][0] = 0
        for i in range(1, n + 1):
            f[i][0][0] = 0
        for j in range(1, m + 1):
            f[0][j][0] = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                f[i][j][0] = 0
                for t in range(1, min(i, j, k) + 1):
                    f[i][j][t] = f[i - 1][j - 1][t - 1] + nums1[i - 1] * nums2[j - 1]
                    if f[i - 1][j][t] is not None:
                        f[i][j][t] = max(f[i][j][t], f[i - 1][j][t])
                    if f[i][j - 1][t] is not None:
                        f[i][j][t] = max(f[i][j][t], f[i][j - 1][t])
        
        return f[-1][-1][k]
```
