---
title: "3503. 子字符串连接后的最长回文串I & 3504. 子字符串连接后的最长回文串II"
aliases: ["yiduobo的每日leetcode 3503.子字符串连接后的最长回文串I && 3504.子字符串连接后的最长回文串II", "3503. 子字符串连接后的最长回文串I", "3504. 子字符串连接后的最长回文串II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/dynamic-programming", "leetcode/hard", "leetcode/greedy", "题单/字符串", "题单/字符串/三-Manacher-算法-回文串", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901396682924601612"
zhihu_id: "1901396682924601612"
zhihu_title: "yiduobo的每日leetcode 3503.子字符串连接后的最长回文串I && 3504.子字符串连接后的最长回文串II"
question_id: ["3503", "3504"]
question: ["子字符串连接后的最长回文串 I", "子字符串连接后的最长回文串 II"]
problem_url: ["https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-i/", "https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2398
created: "2025-05-01T23:47:35+08:00"
updated: "2025-05-01T23:47:35+08:00"
upvotes: 0
comments: 0
---

# 3503. 子字符串连接后的最长回文串I & 3504. 子字符串连接后的最长回文串II

> **[yiduobo的每日leetcode 3503.子字符串连接后的最长回文串I && 3504.子字符串连接后的最长回文串II](https://zhuanlan.zhihu.com/p/1901396682924601612) · 知乎 · 2025-05-01 · 赞同 0**
> 力扣：[3503. 子字符串连接后的最长回文串 I](https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-i/) · Medium · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3504. 子字符串连接后的最长回文串 II](https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/) · Hard · 灵茶山艾府：[枚举回文中心 + DP，附后缀数组 + Manacher 线性做法（Python/Java/C++/Go）](../3504%20子字符串连接后的最长回文串%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3503.子字符串连接后的最长回文串I

[3503. 子字符串连接后的最长回文串 I - 力扣（LeetCode）](https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-i/description/)

3504.子字符串连接后的最长回文串II

[3504. 子字符串连接后的最长回文串 II - 力扣（LeetCode）](https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/)

题目给出两个字符串s和t，现在要求从s和t中各选出一个子串(可以为空子串)，拼接在一起之后得到一个新的字符串。问通过这种方法拼接得到的最长的回文串的长度是多少。

两题的题设一样，第二题的数据规模较大，不过也不是特别大，s和t的长度都不超过1000。

方便起见，记选出的两个子串分别为sub_s和sub_t。题目需要保证拼接得到的字符串是回文串，那么最终拼接得到的字符串必然是以下几种形式之一

1、仅有sub_s

这种情况下sub_s本身是回文串，而sub_t为空。对于这种情况，可以使用O(n^2)的动态规划很方便的计算出s中的最长回文子串。令g[left][right]表示s[left: right + 1]是否为回文串，那么对于g[left][right]：

1-1）当left \= right时，有g[left][right]必然为true

1-2）当left \= right - 1时，若s[left]等于s[right]，那么g[left][right]为true，否则为false

1-3）其他情况下，若s[left]等于s[right]，且g[left + 1][right - 1]为ture，那么g[left][right]为ture，否则为false

计算得到g后，只需枚举子串的起点和终点i、j，若g[i][j]为true，就用j - i + 1来更新答案

2、仅有sub_t

这种情况与情况1对称，同样通过动态规划计算出数组g，然后枚举子串起点和终点，通过g判断是否为回文串并更新答案即可

3、sub_s和sub_t都非空

对于这种情况，拼接后的字符串形如

[sub_s的前缀] [空串 或者 sub_s的后缀 或者 sub_t的前缀] [sub_t的后缀]

其中两侧的sub_s的前缀和sub_t的后缀必须是对称的，而中间这个部分可以为空，也可以是sub_s或者sub_t的一部分，但是中间这一部分必须自成回文。

对于判断两个字符串的子串是否对称这个问题，可以反过来思考，将t翻转后，问题就转化为了这两个子串是否相同。而对于这个问题，则可以使用动态规划进行求解。先将字符串t进行翻转，然后令f[i][j]表示以s[i]以及t[j]开头的子串的最长匹配长度，那么对于f[i][j]

3-1）若s[i]不等于t[j]，那么f[i][j]显然为0

3-2）若s[i]等于t[j]，那么f[i][j] \= f[i + 1][j + 1] + 1，也就是在后一位的基础上新增一个字符。在这里需要保证i和j没有越界，同时计算f的时候需要从后往前

得到f后，就可以枚举s和t中子串的起点i和j，此时就可以从s中取出s\[i: i + f\[i\]\[j\]\]作为sub_s的前缀，从的t中取出t\[j: j + f\[i\]\[j\]\]作为sub_t的后缀，最后对于中间这一段，如果从s中选取，那么就应该选取s中以i + f\[i\]\[j\]开头的最长回文子串，如果从t中选取，则应该选取t中以j + f\[i\]\[j\]开头的最长回文子串。

对于这个最长回文子串，则又可以利用情况1和情况2中计算得到的g数组。令best[i]表示当前字符串中以i为起点的最长回文子串长度，那么对于best[i]，可以倒序枚举字符串终点j，若g[i][j]为true，那么就将best[i]置为j - i + 1。得到best后，也可以顺便应用在前两种情况中，就不需要额外再枚举每种子串了。

分别计s和t对应的best为gs和gt，那么拼接得到的字符串长度就是

f\[i\]\[j\] \* 2 + max(gs\[i + f\[i\]\[j\]\], gt\[j + f\[i\]\[j\])

其中f[i][j] \* 2表示sub_s的前缀以及sub_t的后缀这两段的长度之和，最后的max则是sub_s的后缀或者sub_t的前缀中的较长者。

最后附上python代码：

```python
class Solution(object):
    def longestPalindrome(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """
        
        t = t[::-1]
        m = len(s)
        n = len(t)
        f = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if s[i] == t[j]:
                    f[i][j] = 1
                    if i + 1 < m and j + 1 < n:
                        f[i][j] += f[i + 1][j + 1]
        
        def calc(s):
            n = len(s)
            g = [[False] * n for _ in range(n)]
            for length in range(1, n + 1):
                for left in range(n):
                    right = left + length - 1
                    if right >= n:
                        break
                    
                    if left == right:
                        g[left][right] = True
                    elif left == right - 1:
                        g[left][right] = (s[left] == s[right])
                    else:
                        g[left][right] = (s[left] == s[right]) and g[left + 1][right - 1]
            
            best = [0] * (n + 1)
            for i in range(n):
                for j in range(n - 1, -1, -1):
                    if g[i][j]:
                        best[i] = j - i + 1
                        break
            
            return best
                        
        gs = calc(s)
        gt = calc(t)
        res = max(max(gs), max(gt))
        for i in range(m):
            for j in range(n):
                res = max(res, f[i][j] * 2 + max(gs[i + f[i][j]], gt[j + f[i][j]]))
        
        return res
```
