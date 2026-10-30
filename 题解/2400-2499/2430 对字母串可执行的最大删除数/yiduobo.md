---
title: "2430. 对字母串可执行的最大删除数"
aliases: ["yiduobo的每日leetcode 2430.对字母串可执行的最大删除数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/五-划分型-DP", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582822902"
zhihu_id: "582822902"
zhihu_title: "yiduobo的每日leetcode 2430.对字母串可执行的最大删除数"
question_id: "2430"
question: "对字母串可执行的最大删除数"
problem_url: "https://leetcode.cn/problems/maximum-deletions-on-a-string/"
difficulty: "Hard"
rating: 2102
created: "2022-11-12T17:20:51+08:00"
updated: "2022-11-12T17:20:51+08:00"
upvotes: 0
comments: 0
---

# 2430. 对字母串可执行的最大删除数

> **[yiduobo的每日leetcode 2430.对字母串可执行的最大删除数](https://zhuanlan.zhihu.com/p/582822902) · 知乎 · 2022-11-12 · 赞同 0**
> 力扣：[2430. 对字母串可执行的最大删除数](https://leetcode.cn/problems/maximum-deletions-on-a-string/) · Hard · 灵茶山艾府：[动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2430.对字母串可执行的最大删除数

[力扣](https://leetcode.cn/problems/maximum-deletions-on-a-string/)

题目对于一个字符串，可能将这个字符串全部删除，或者删除其某个前缀，那么在这里就很容易想到令g[i]表示字符串中从i开始的后缀最多可以删除的次数。

对于g[i]，首先可以初始化g[i] \= 1，表示一次全删了。接下来，可以从i + 1开始往后枚举j，尝试将i到j - 1之间的字符删除。不过在这里有一个前提条件是i到j - 1之间字符串必须与以j开头的长度为j - i的字符串完全一致，也就是以i开头的后缀字符串与以j开头的后缀字符串的最长公共前缀必须大于等于j - i。

对于公共前缀这个问题，在这里就可以先预处理出字符串中所有后缀字符串之间的最长公共前缀，并将其保存在f[i][j]中。由于题目的数据规模不大，在这里使用O(n^2)的动态规划算法来求解是可行的。

得到f[i][j]后，若f[i][j] >\= j - i，那么就有g[i] \= max(g[i], g[j] + 1)，表示删去了i到j - 1这一段。

全部计算完毕后，g[0]就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def deleteString(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        s += '#'

        f = [[0] * (n + 1) for _ in range(n + 1)]
        f[n - 1][n] = 0
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    f[i][j] = f[i + 1][j + 1] + 1
        
        g = [1] * n
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                if f[i][j] >= j - i:
                    g[i] = max(g[i], g[j] + 1)
        
        return g[0]
```
