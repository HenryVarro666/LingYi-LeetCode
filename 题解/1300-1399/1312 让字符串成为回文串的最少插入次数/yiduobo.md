---
title: "1312. 让字符串成为回文串的最少插入次数"
aliases: ["yiduobo的每日leetcode 1312.让字符串成为回文串的最少插入次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392610752"
zhihu_id: "392610752"
zhihu_title: "yiduobo的每日leetcode 1312.让字符串成为回文串的最少插入次数"
question_id: "1312"
question: "让字符串成为回文串的最少插入次数"
problem_url: "https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/"
created: "2021-07-23T22:18:17+08:00"
updated: "2021-07-23T22:18:17+08:00"
upvotes: 0
comments: 1
---

# 1312. 让字符串成为回文串的最少插入次数

> **[yiduobo的每日leetcode 1312.让字符串成为回文串的最少插入次数](https://zhuanlan.zhihu.com/p/392610752) · 知乎 · 2021-07-23 · 赞同 0**
> 力扣：[1312. 让字符串成为回文串的最少插入次数](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1312.让字符串成为回文串的最少插入次数

[力扣](https://leetcode-cn.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)

经典的动态规划问题，令f[l][r]表示将l到r这一段子串变为回文串所需的最少插入次数，那么对于f[l][r]：

1、若l \= r，说明此时字符串的长度为1，必然为回文串，因此有f[l][r] \= 0

2、若s[l] \= s[r]，且l \= r - 1，说明此时字符串的由两个相同的字符组成，必然为回文串，因此有f[l][r] \= 0

3、若s[l] \= s[r]，且l \< r - 1，此时无论我们如何在l + 1到r - 1之间插入字符，最后得到的字符中s[l]依然是与s[r]进行匹配的，因此此时就有

f[l][r] \= f[l +1][r - 1]

4、若s[l] !\= s[r]，那么我们必须想办法在s[l]左侧插入一个字符，与s[r]进行匹配，或者在s[r]右侧插入一个字符，与s[l]进行匹配，因此有

f[l][r] \= min(f[l + 1][r], f[l][r - 1]) + 1

具体实现上，可以使用递推，先从小到大枚举区间长度，再枚举区间起点，并通过区间长度和起点计算出区间终点，然后进行动态规划。

我在这里采用的记忆化搜索的实现方式，相对简洁一点。

最后附上python代码：

```python
class Solution(object):
    def minInsertions(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        f = [[None] * n for _ in range(n)]
        return self.dfs(0, n - 1, s, f)
    
    def dfs(self, l, r, s, f):
        if f[l][r] is None:
            if l == r:
                f[l][r] = 0
            elif s[l] == s[r]:
                if l == r - 1:
                    f[l][r] = 0
                else:
                    f[l][r] = self.dfs(l + 1, r - 1, s, f)
            else:
                f[l][r] = min(self.dfs(l + 1, r, s, f), self.dfs(l, r - 1, s, f)) + 1
        
        return f[l][r]
```
