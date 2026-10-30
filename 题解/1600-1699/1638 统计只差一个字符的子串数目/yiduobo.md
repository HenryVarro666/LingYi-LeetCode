---
title: "1638. 统计只差一个字符的子串数目"
aliases: ["yiduobo的每日leetcode 1638.统计只差一个字符的子串数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/tu-jie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438388678"
zhihu_id: "438388678"
zhihu_title: "yiduobo的每日leetcode 1638.统计只差一个字符的子串数目"
question_id: "1638"
question: "统计只差一个字符的子串数目"
problem_url: "https://leetcode.cn/problems/count-substrings-that-differ-by-one-character/"
difficulty: "Medium"
created: "2021-11-27T12:58:48+08:00"
updated: "2021-11-27T12:58:48+08:00"
upvotes: 0
comments: 0
---

# 1638. 统计只差一个字符的子串数目

> **[yiduobo的每日leetcode 1638.统计只差一个字符的子串数目](https://zhuanlan.zhihu.com/p/438388678) · 知乎 · 2021-11-27 · 赞同 0**
> 力扣：[1638. 统计只差一个字符的子串数目](https://leetcode.cn/problems/count-substrings-that-differ-by-one-character/) · Medium · 灵茶山艾府：[【图解】非暴力 O(nm) 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1638.统计只差一个字符的子串数目

[力扣](https://leetcode-cn.com/problems/count-substrings-that-differ-by-one-character/)

动态规划的题目。如果想知道之差一个字符的子串数目，那么在此之前知道完全一致的子串数目就很有必要了。那么令f[i][j]表示以s[i]和t[j]结尾的相同子串的数目，令g[i][j]表示以s[i]和t[j]结尾的只差一个字符的子串数目，那么对于f[i][j]和g[i][j]：

1、当i \= 0且j \= 0时：

此时若s[0] \= t[0]，那么就有f[i][j] \= 1，g[i][j] \= 0，否则就是反过来f[i][j] \= 0，g[i][j] \= 1

2、当i \= 0且j !\= 0时：

此时需要对比s[0]与t[j]，若s[0] \= t[j]，那么就有f[i][j] \= 1，g[i][j] \= 0，否则就是反过来f[i][j] \= 0，g[i][j] \= 1

3、当i !\= 0且j \= 0时：

与情况2类似，此时需要对比s[i]与t[0]，若s[j] \= t[0]，那么就有f[i][j] \= 1，g[i][j] \= 0，否则就是反过来f[i][j] \= 0，g[i][j] \= 1

4、当i和j都不为0时：

首先考察f[i][j]。

当s[i] !\= t[j]时，以s[i]和t[j]结尾的子串是不可能相同的，因此就有f[i][j] \= 0。

当s[i] \= t[j]时，可以认为在f[i - 1][j - 1]代表的所有相同子串后面分别添加上了s[i]与t[j]，这样一来会得到f[i - 1][j - 1]组以s[i]和t[j]结尾的相同子串。除此之外，单独将s[i]和t[j]拎出来也是一组相同子串，因此就有

f[i][j] \= f[i - 1][j - 1] + 1

接下来考察g[i][j]。

当s[i] !\= t[j]时，由于这里已经出现了1个不相同的字符，因此需要子串之前的字符全部相同，那么就可以认为是在f[i - 1][j - 1]代表的所有相同子串后面分别添加上了s[i]与t[j]，这样一来会得到f[i - 1][j - 1]组以s[i]和t[j]结尾的只有一个字符不同的子串。除此之外，单独将s[i]和t[j]拎出来也是一组只有一个字符不同的子串，因此就有

g[i][j] \= f[i - 1][j - 1] + 1

当s[i] \= t[j]时，由于最后一个字符相同，那么这个不同的字符需要出现在i和j前面，那么就可以认为是在g[i - 1][j - 1]代表的所有只有一个字符不同的子串后面分别添加上了s[i]和t[j]，这样一来会得到g[i - 1][j - 1]组以s[i]和t[j]结尾的只有一个字符不同的子串。此时需要注意，单独将s[i]和t[j]拎出来并不能形成只有一个字符不同的子串，因此就有

g[i][j] \= g[i - 1][j - 1]

动态规划结束后，所有g[i][j]之和就是最终答案了。

当然，根据这里转移方程的形式完全可以使用滚动数组，不过为了f和g表达的意义更加清晰，我在这里就没有进行这个优化了。

最后附上python代码：

```python
class Solution(object):
    def countSubstrings(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        m = len(s)
        n = len(t)
        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]

        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    if s[i] == t[j]:
                        f[i][j] = 1
                    else:
                        g[i][j] = 1
                elif s[i] == t[j]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    g[i][j] = g[i - 1][j - 1]
                else:
                    g[i][j] = f[i - 1][j - 1] + 1
                
                res += g[i][j]
        
        return res
```
