---
title: "1035. 不相交的线"
aliases: ["yiduobo的每日leetcode 1035.不相交的线"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369946015"
zhihu_id: "369946015"
zhihu_title: "yiduobo的每日leetcode 1035.不相交的线"
question_id: "1035"
question: "不相交的线"
problem_url: "https://leetcode.cn/problems/uncrossed-lines/"
difficulty: "Medium"
rating: 1806
created: "2021-05-05T21:41:05+08:00"
updated: "2021-05-05T21:41:05+08:00"
upvotes: 0
comments: 0
---

# 1035. 不相交的线

> **[yiduobo的每日leetcode 1035.不相交的线](https://zhuanlan.zhihu.com/p/369946015) · 知乎 · 2021-05-05 · 赞同 0**
> 力扣：[1035. 不相交的线](https://leetcode.cn/problems/uncrossed-lines/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1035.不相交的线

[力扣](https://leetcode-cn.com/problems/uncrossed-lines/)

虽然题目描述花里胡哨的，但是仔细分析可以发现这就是个最长公共子序列问题，那么使用经典的二维动态规划，令f[i][j]表示A的前i个数字与B的前j个数字最多能匹配上多少然后执行二维的动态规划即可。

最后附上python代码：

```python
class Solution(object):
    def maxUncrossedLines(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: int
        """

        m = len(A)
        n = len(B)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if A[i] == B[j]:
                    f[i + 1][j + 1] = f[i][j] + 1
                else:
                    f[i + 1][j + 1] = max(f[i + 1][j], f[i][j + 1])
        
        return f[m][n]
```
