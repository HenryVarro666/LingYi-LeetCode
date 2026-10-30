---
title: "115. 不同的子序列"
aliases: ["yiduobo的每日leetcode 115.不同的子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139106505"
zhihu_id: "139106505"
zhihu_title: "yiduobo的每日leetcode 115.不同的子序列"
question_id: "115"
question: "不同的子序列"
problem_url: "https://leetcode.cn/problems/distinct-subsequences/"
difficulty: "Hard"
created: "2020-05-08T21:57:05+08:00"
updated: "2020-05-08T21:57:05+08:00"
upvotes: 1
comments: 0
---

# 115. 不同的子序列

> **[yiduobo的每日leetcode 115.不同的子序列](https://zhuanlan.zhihu.com/p/139106505) · 知乎 · 2020-05-08 · 赞同 1**
> 力扣：[115. 不同的子序列](https://leetcode.cn/problems/distinct-subsequences/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

115.不同的子序列<https://leetcode-cn.com/problems/distinct-subsequences/>

动态规划的题目。与之前做过的字符串问题相同，这类问题总还是二维的状态f[i][j]，表示s的前i位与t的前j位能达成的某个最优关系，这里就是s[:i]的子序列中t[:j]出现的次数。

于是对于f[i][j]，有这几种情况：

1、j为0。此时t[:j]为空串，必定是s[:i]的一个子序列，因此有f[i][j] \= 1。

2、j不为0，且i为0。此时s[:i]为空串，而t[:j]非空，因此此时的f[i][j] \= 0。

3、i与j都不为0。首先，s[:i - 1]的所有子序列也一定是s[:i]的子序列，因此f[i][j]至少等于f[i - 1][j]。接下来，若s[i - 1] \=\= t[j - 1]，那么f[i][j]应该再额外加上f[i - 1][j - 1]的值，这里的原理是s[:i]的最后一位s[i - 1]与t[:j]的最后一位t[j - 1]固定匹配住，那么剩下的就是s[:I - 1]的子序列与t[j - 1]的匹配情况，即f[i - 1][j - 1]，因此有f[i][j] +\= f[i - 1][j]。

最后的答案则是f[m][n]，m和n分别为s与t的长度。时间复杂度为O(mn)，空间复杂度这边可以使用滚动数组优化到O(n)，简单起见我这里的实现就没做这个优化。

最后附上python代码：

```python
class Solution(object):
    def numDistinct(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        m = len(s)
        n = len(t)

        f = [[0] * (n + 1) for index in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if j == 0:
                    f[i][j] = 1
                elif i == 0:
                    continue
                else:
                    f[i][j] = f[i - 1][j]
                    if s[i - 1] == t[j - 1]:
                        f[i][j] += f[i - 1][j - 1]
        
        return f[m][n]
```
