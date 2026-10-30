---
title: "1682. 最长回文子序列II"
aliases: ["yiduobo的每日leetcode 1682.最长回文子序列II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619660071"
zhihu_id: "619660071"
zhihu_title: "yiduobo的每日leetcode 1682.最长回文子序列II"
question_id: "1682"
question: "最长回文子序列II"
problem_url: "https://leetcode.cn/problems/longest-palindromic-subsequence-ii/"
created: "2023-04-05T19:30:17+08:00"
updated: "2023-04-05T19:30:17+08:00"
upvotes: 2
comments: 0
---

# 1682. 最长回文子序列II

> **[yiduobo的每日leetcode 1682.最长回文子序列II](https://zhuanlan.zhihu.com/p/619660071) · 知乎 · 2023-04-05 · 赞同 2**
> 力扣：[1682. 最长回文子序列II](https://leetcode.cn/problems/longest-palindromic-subsequence-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1682.最长回文子序列II

[力扣](https://leetcode.cn/problems/longest-palindromic-subsequence-ii/)

本题在常规最长回文子序列问题的基础上多出了不能有相同的连续字符这个条件，那么最直观的想法就是在原始冬天规划状态表示的基础上加上最外层字符的信息。

令f[i][j][k]表示字符串中第i到第j个字符中，以字符k为最外侧字符的回文子序列的最长长度，那么对于f[i][j][k]：

1、可以选择放弃第i个字符或者第j个字符，那么就有

f[i][j][k] \= max(f[i + 1][j][k]，f[i][j - 1][k])

2、若s[i]与s[j]相同，那么可以认为这两个字符形成配对，此时就需要内层的字符不同，于是可以枚举内层的字符t，那么当t与s[i]不同时，就有

f[i][j][k] \= max(f[i][j][k], f[i + 1][j - 1][t] + 2)

计算完成后，最终答案即为max(f[0][-1])

最后附上pyhton代码：

```python
class Solution(object):
    def longestPalindromeSubseq(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        f = [[[0] * 26 for j in range(n)] for i in range(n)]

        for length in range(2, n + 1):
            for i in range(n):
                j = i + length - 1
                if j >= n:
                    break

                for k in range(26):
                    f[i][j][k] = max(f[i + 1][j][k], f[i][j - 1][k])
                
                if s[i] == s[j]:
                    k = ord(s[i]) - 97
                    for t in range(26):
                        if k == t:
                            continue
                        f[i][j][k] = max(f[i][j][k], f[i + 1][j - 1][t] + 2)
        
        return max(f[0][-1])
```
