---
title: "132. 分割回文串II"
aliases: ["yiduobo的每日leetcode 132.分割回文串II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141252015"
zhihu_id: "141252015"
zhihu_title: "yiduobo的每日leetcode 132.分割回文串II"
question_id: "132"
question: "分割回文串 II"
problem_url: "https://leetcode.cn/problems/palindrome-partitioning-ii/"
difficulty: "Hard"
created: "2020-05-15T22:01:49+08:00"
updated: "2020-05-15T22:01:49+08:00"
upvotes: 0
comments: 0
---

# 132. 分割回文串II

> **[yiduobo的每日leetcode 132.分割回文串II](https://zhuanlan.zhihu.com/p/141252015) · 知乎 · 2020-05-15 · 赞同 0**
> 力扣：[132. 分割回文串 II](https://leetcode.cn/problems/palindrome-partitioning-ii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

132.分割回文串II <https://leetcode-cn.com/problems/palindrome-partitioning-ii/submissions/>

上一题的升级版本，不过这里是要求最少的切分次数，使用的是动态规划。

f[i]表示前i个字符切分的最少次数，那么：

1、首先当i为0时，表示空串，那么有f[i] \= 0。

2、若s[:i]本身就是回文串，那么不需要进行切分，于是有f[i] \= 0。

3、若s[:i]不是回文串，则需要从1到i之间枚举分割点cut_pos，若s[cut_pos : index]是回文串，那么有f[i] \= min(f[i], f[cut_pos - 1] + 1)。

判断回文依然可以先预处理，或者使用记忆化搜索来做。我这里还是用的记忆化搜索，具体细节与上一题一样（传送门在这里：[yiduobo：yiduobo的每日leetcode 131.分割回文串](https://zhuanlan.zhihu.com/p/141249547)）。

最后附上python代码：

```python
class Solution(object):
    def minCut(self, s):
        """
        :type s: str
        :rtype: int
        """

        f = [0]
        g = [[None] * len(s) for _ in range(len(s))]
        for index in range(1, len(s)):
            if self.check(s, 0, index, g):
                f.append(0)
            else:
                min_step = None
                for cut_pos in range(1, index + 1):
                    if self.check(s, cut_pos, index, g):
                        if min_step is None or min_step > f[cut_pos - 1] + 1:
                            min_step = f[cut_pos - 1] + 1
                f.append(min_step)
        
        return f[len(s) - 1]

    def check(self, s, left, right, g):
        if g[left][right] is None:
            if left >= right:
                g[left][right] = True
            else:
                if s[left] == s[right]:
                    g[left][right] = self.check(s, left + 1, right - 1, g)
                else:
                    g[left][right] = False

        return g[left][right]
```
