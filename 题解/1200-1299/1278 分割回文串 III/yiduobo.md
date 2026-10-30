---
title: "1278. 分割回文串III"
aliases: ["yiduobo的每日leetcode 1278.分割回文串III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388280511"
zhihu_id: "388280511"
zhihu_title: "yiduobo的每日leetcode 1278.分割回文串III"
question_id: "1278"
question: "分割回文串 III"
problem_url: "https://leetcode.cn/problems/palindrome-partitioning-iii/"
difficulty: "Hard"
rating: 1979
created: "2021-07-09T22:06:05+08:00"
updated: "2021-07-09T22:06:05+08:00"
upvotes: 0
comments: 0
---

# 1278. 分割回文串III

> **[yiduobo的每日leetcode 1278.分割回文串III](https://zhuanlan.zhihu.com/p/388280511) · 知乎 · 2021-07-09 · 赞同 0**
> 力扣：[1278. 分割回文串 III](https://leetcode.cn/problems/palindrome-partitioning-iii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1278.分割回文串III

[力扣](https://leetcode-cn.com/problems/palindrome-partitioning-iii/)

题目中有两种操作，一种是修改某个字符，另一种是将一个大串分割成若干个小串。

首先，我们可以先考虑修改字符的情况，那么就可以得到一种动态规划的做法，令f[i][l]表示将从第i个字符开始，长度为l的字符串修改成为回文串所需的最少操作次数，那么对于f[i][l]，若s[i]等于s[i + l - 1]，那么首末两个字符就无须处理，于是有f[i][l] \= f[i +1][l - 2]，否则我们就需要修改s[i]或者s[i + l - 1]，因此就有f[i][l] \= f[i + 1][l - 2] + 1。

接下来我们考虑切分的情况。同样是使用动态规划，令g[i][j]表示前i个字符，切分成k份之后然后修改字符满足条件之后所需的最小操作数，那么对于g[i][j]：

1、若j等于1，那么g[i][j]不需要进行切分，因此就有g[i][j] \= f[0][i + 1]

2、若j大于1，那么我们可以枚举前j - 1个部分的右边界cut_pos。由于这里需要切分成j份，因此这个cut_pos必须给前面留出至少j - 1个字符，因此cut_pos的取值范围就是j - 2到i - 1，而后面从cut_pos + 1到i这一段只能修改字符，于是就有

g[i][j] \= min(g[i][j], g[cut_pos][j - 1] + f[cut_pos + 1][i - cut_pos])

计算完成后，g[n - 1][k]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def palindromePartition(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)
        f = [[0] * (n + 1) for _ in range(n)]
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                if s[i] == s[i + l - 1]:
                    f[i][l] = f[i + 1][l - 2]
                else:
                    f[i][l] = f[i + 1][l - 2] + 1
        
        g = [[None] * (k + 1) for _ in range(n)]
        for j in range(1, k + 1):
            for i in range(j - 1, n):
                if j == 1:
                    g[i][j] = f[0][i + 1]
                else:
                    for cut_pos in range(j - 2, i):
                        if g[i][j] is None or g[i][j] > g[cut_pos][j - 1] + f[cut_pos + 1][i - cut_pos]:
                            g[i][j] = g[cut_pos][j - 1] + f[cut_pos + 1][i - cut_pos]

        return g[n - 1][k]
```
