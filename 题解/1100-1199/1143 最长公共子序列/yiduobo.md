---
title: "1143. 最长公共子序列"
aliases: ["yiduobo的每日leetcode 1143.最长公共子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/LeetCode-热题-100", "题单/动态规划/四-经典线性-DP", "题单/LeetCode-热题-100/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377445187"
zhihu_id: "377445187"
zhihu_title: "yiduobo的每日leetcode 1143.最长公共子序列"
question_id: "1143"
question: "最长公共子序列"
problem_url: "https://leetcode.cn/problems/longest-common-subsequence/"
difficulty: "Medium"
created: "2021-06-02T23:09:15+08:00"
updated: "2021-06-02T23:09:15+08:00"
upvotes: 0
comments: 0
---

# 1143. 最长公共子序列

> **[yiduobo的每日leetcode 1143.最长公共子序列](https://zhuanlan.zhihu.com/p/377445187) · 知乎 · 2021-06-02 · 赞同 0**
> 力扣：[1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1143.最长公共子序列

[力扣](https://leetcode-cn.com/problems/longest-common-subsequence/)

经典的动态规划问题，令f[i][j]表示text1的前i个字符与text2的前j个字符能形成的最长公共子序列的长度，那么对于f[i][j]：

1、当i或者j为0时，显然有f[i][j] \= 0

2、当i和j都不为0，且text1[i - 1] \= text2[j - 1]，那么我们应该让这两个字符进行匹配，于是此时有f[i][j] \= f[i - 1][j - 1] + 1

3、其他情况下，则需要浪费掉text1[i - 1]或者text2[j - 1]，具体浪费哪一个则取决于f[i - 1][j]和f[i][j - 1]的大小，即f[i][j] \= max(f[i - 1][j], f[i][j - 1])

最后附上python代码：

```python
class Solution(object):
    def longestCommonSubsequence(self, text1, text2):
        """
        :type text1: str
        :type text2: str
        :rtype: int
        """

        m = len(text1)
        n = len(text2)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                else:
                    f[i][j] = max(f[i - 1][j], f[i][j - 1])
        
        return f[-1][-1]
```
