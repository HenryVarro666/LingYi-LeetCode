---
title: "1027. 最长等差数列"
aliases: ["yiduobo的每日leetcode 1027.最长等差数列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/array", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369327816"
zhihu_id: "369327816"
zhihu_title: "yiduobo的每日leetcode 1027.最长等差数列"
question_id: "1027"
question: "最长等差数列"
problem_url: "https://leetcode.cn/problems/longest-arithmetic-subsequence/"
difficulty: "Medium"
rating: 1759
created: "2021-05-01T23:08:54+08:00"
updated: "2021-05-01T23:09:12+08:00"
upvotes: 0
comments: 0
---

# 1027. 最长等差数列

> **[yiduobo的每日leetcode 1027.最长等差数列](https://zhuanlan.zhihu.com/p/369327816) · 知乎 · 2021-05-01 · 赞同 0**
> 力扣：[1027. 最长等差数列](https://leetcode.cn/problems/longest-arithmetic-subsequence/) · Medium · 灵茶山艾府：[两种动态规划的定义方式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1027.最长等差数列

[力扣](https://leetcode-cn.com/problems/longest-arithmetic-subsequence/)

二维的动态规划算法是比较容易想到的。

令f[i][j]表示以A[i]以及A[j]作为末尾两项的等差数列的最长长度，那么对于f[i][j]，该等差数列的公差为A[j] - A[i]，因此A[i]的前一项pre的大小就应该是

A[i] - (A[j] - A[i]) \= A[i] + A[i] - A[j]。

若在0到i - 1之间存在某个A[k]等于pre，那么就可以认为f[i][j]是可以通过f[k][i]再加上A[j]这一项得到的，那么此时就有

f[i][j] \= max(f[i][j]，f[k][i] + 1)

当然，在0到i - 1之间可能存在多个A[k]等于pre，此时很明显应该选择最靠后的那个A[k]，于是我们在这里可以再额外使用一个dict来储存每个数最后一次出现在A中的位置。

最后附上python代码：

```python
class Solution(object):
    def longestArithSeqLength(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        n = len(A)
        f = [[2] * n for _ in range(n - 1)]
        pos_dict = {}
        res = 2
        for i in range(n - 1):
            for j in range(i + 1, n):
                pre = A[i] + A[i] - A[j]
                if pre in pos_dict:
                    f[i][j] = max(f[i][j], f[pos_dict[pre]][i] + 1)
                res = max(res, f[i][j])

            pos_dict[A[i]] = i

        return res
```
