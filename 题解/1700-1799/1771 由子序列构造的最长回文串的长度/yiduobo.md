---
title: "1771. 由子序列构造的最长回文串"
aliases: ["yiduobo的每日leetcode 1771.由子序列构造的最长回文串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/461513638"
zhihu_id: "461513638"
zhihu_title: "yiduobo的每日leetcode 1771.由子序列构造的最长回文串"
question_id: "1771"
question: "由子序列构造的最长回文串的长度"
problem_url: "https://leetcode.cn/problems/maximize-palindrome-length-from-subsequences/"
difficulty: "Hard"
rating: 2182
created: "2022-01-25T00:26:24+08:00"
updated: "2022-01-25T00:26:24+08:00"
upvotes: 0
comments: 0
---

# 1771. 由子序列构造的最长回文串

> **[yiduobo的每日leetcode 1771.由子序列构造的最长回文串](https://zhuanlan.zhihu.com/p/461513638) · 知乎 · 2022-01-25 · 赞同 0**
> 力扣：[1771. 由子序列构造的最长回文串的长度](https://leetcode.cn/problems/maximize-palindrome-length-from-subsequences/) · Hard · 灵茶山艾府：[巧妙转换！516 变形题！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1771.由子序列构造的最长回文串

[力扣](https://leetcode-cn.com/problems/maximize-palindrome-length-from-subsequences/)

题目实际上就相当于要求从subsequence1和subsequence2组合后的字符串后找出最长回文子序列，同时要求这个回文子序列是跨越中心连接点的。

找最长回文子序列的问题可以使用经典的区间动态规划来做，即令f[i][j]表示区间i到j这一段的最长回文子序列的长度，那么对于f[i][j]：

1、若i \= j，此时只有一个字符，必然是回文的，因此有f[i][j] \= 1

2、若i \< j，且s[i] \= s[j]，那么可以让这两个字符配对，那么就有f[i][j] \= f[i + 1][j - 1] + 2

3、其他情况下，需要牺牲掉s[i]或者s[j]，于是就有f[i][j] \= max(f[i + 1][j], f[i][j - 1])

接下来需要考虑如何保证这个回文串跨越了中心点。一个可行的想法是确保回文串最两边的字符是分属两个字符串，由于这里全都是小写字符，那么可以先计算每个字符首次和最后一次出现的位置。由于最长回文子序列的两端必然是其中某一组字符，因此可以枚举每种字符，不妨设这个字符第一次出现和最后一次出现的位置分别是first和last，那么此时对应的最长回文子序列的长度就是f[first + 1][last - 1] + 2，取其中最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestPalindrome(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """

        m = len(word1)
        s = word1 + word2
        n = len(s)
        f = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1
                if length == 1:
                    f[l][r] = 1
                elif s[l] == s[r]:
                    f[l][r] = f[l + 1][r - 1] + 2
                else:
                    f[l][r] = max(f[l + 1][r], f[l][r - 1])

        first_pos = {}
        last_pos = {}
        for index, char in enumerate(s):
            if char not in first_pos:
                first_pos[char] = index
            last_pos[char] = index
        
        res = 0
        for index in range(26):
            char = chr(index + 97)
            if char in first_pos:
                if first_pos[char] < m and last_pos[char] >= m:
                    res = max(res, f[first_pos[char] + 1][last_pos[char] - 1] + 2)
        
        return res
```
