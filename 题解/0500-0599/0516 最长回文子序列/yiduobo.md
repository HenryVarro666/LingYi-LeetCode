---
title: "516. 最长回文子序列"
aliases: ["yiduobo的每日leetcode 516.最长回文子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260180293"
zhihu_id: "260180293"
zhihu_title: "yiduobo的每日leetcode 516.最长回文子序列"
question_id: "516"
question: "最长回文子序列"
problem_url: "https://leetcode.cn/problems/longest-palindromic-subsequence/"
difficulty: "Medium"
created: "2020-09-28T20:23:55+08:00"
updated: "2020-09-28T20:23:55+08:00"
upvotes: 1
comments: 0
---

# 516. 最长回文子序列

> **[yiduobo的每日leetcode 516.最长回文子序列](https://zhuanlan.zhihu.com/p/260180293) · 知乎 · 2020-09-28 · 赞同 1**
> 力扣：[516. 最长回文子序列](https://leetcode.cn/problems/longest-palindromic-subsequence/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

516.最长回文子序列<https://leetcode-cn.com/problems/longest-palindromic-subsequence/>

经典的区间动态规划问题，使用f[l][r]表示l到r这一段最长的回文子序列长度，那么就有：

1、若l等于r，那么说明此时就只有一个字符，因此f[l][r] \= 1

2、若l等于r - 1，那么说明此时只有两个字符。若它们相等，那么f[l][r] \= 2，否则f[l][r] \= 1

3、若s[l]等于s[r]，那么将这两个字符必然是f[l][r]代表的子序列的一部分，因此就有

f[l][r] \= f[l + 1][r - 1] + 2

4、若s[l]不等于s[r]，那么这两个字符中必然要去掉一个，于是有

f[l][r] \= max(f[l + 1][r], f[l][r - 1])

在具体计算的时候需要注意循环的顺序，方便起见我还是用的记忆化搜索的方法。

最后附上python代码：

```python
class Solution(object):
    def longestPalindromeSubseq(self, s):
        """
        :type s: str
        :rtype: int
        """

        l = len(s)
        f = [[None] * l for _ in range(l)]

        return self.dfs(0, l - 1, s, f)

    def dfs(self, left, right, s, f):
        if f[left][right] is not None:
            return f[left][right]

        if left == right:
            f[left][right] = 1
        elif left == right - 1:
            if s[left] == s[right]:
                f[left][right] = 2
            else:
                f[left][right] = 1
        elif s[left] == s[right]:
            f[left][right] = self.dfs(left + 1, right - 1, s, f) + 2
        else:
            f[left][right] = max(self.dfs(left + 1, right, s, f), self.dfs(left, right - 1, s, f))

        return f[left][right]
```
