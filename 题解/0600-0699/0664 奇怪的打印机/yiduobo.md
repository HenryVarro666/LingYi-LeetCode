---
title: "664. 奇怪的打印机"
aliases: ["yiduobo的每日leetcode 664.奇怪的打印机"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/289668633"
zhihu_id: "289668633"
zhihu_title: "yiduobo的每日leetcode 664.奇怪的打印机"
question_id: "664"
question: "奇怪的打印机"
problem_url: "https://leetcode.cn/problems/strange-printer/"
created: "2020-11-12T23:09:39+08:00"
updated: "2020-11-12T23:09:39+08:00"
upvotes: 0
comments: 0
---

# 664. 奇怪的打印机

> **[yiduobo的每日leetcode 664.奇怪的打印机](https://zhuanlan.zhihu.com/p/289668633) · 知乎 · 2020-11-12 · 赞同 0**
> 力扣：[664. 奇怪的打印机](https://leetcode.cn/problems/strange-printer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

664.奇怪的打印机

[力扣](https://leetcode-cn.com/problems/strange-printer/)

经典的区间动态规划问题，用f[i][j]表示打印i到j这一段需要的最少次数。对于f[i][j]：

1、首先，我们可以在f[i][j - 1]的基础上直接打印s[j]，因此可以将f[i][j]初始化为f[i][j - 1] + 1

2、除此之外，我们还可以利用起打印机连续打印的性质，对于新加入的s[j]，若其与之前的某个s[k]相等，那么我们可以分别打印s[i]到s[k - 1]以及s[k]到s[j]，其中s[k]到s[j]的部分由于首尾相等，因此可以视为在答应这一部分是首先全部都打印了s[k]，然后再处理额外的s[k + 1]到s[j - 1]的部分。

需要注意的是，这里不能简单的认为状态变成了f[k + 1][j - 1] + 1，因为这个区间里面可能还存在其他与s[j]相等的字符，因此这里只能将f[k][j]视为f[k + 1][j]或f[k][j - 1]。

因此，这种情况下就有f[i][j] \= min(f[i][j]，f[i][k - 1] + f[k + 1][j])

方便起见，我在这里采用的是记忆化搜索的方法。当然使用普通的递推式动态规划也是可以的，不过此时就必须优先计算较短区间的值，具体来说就是枚举区间长度l，然后枚举区间的左边界i，通过i + l获得区间的右边界j。

最后附上python代码：

```python
class Solution(object):
    def strangePrinter(self, s):
        """
        :type s: str
        :rtype: int
        """

        if not s:
            return 0

        n = len(s)
        f = [[None] * n for _ in range(n)]
        
        return self.dfs(0, n - 1, f, s)

    def dfs(self, l, r, f, s):
        if l > r:
            return 0
        if l == r:
            return 1
        if f[l][r] is None:
            f[l][r] = self.dfs(l, r - 1, f, s) + 1
            for cut_pos in range(l, r):
                if s[r] == s[cut_pos]:
                    f[l][r] = min(f[l][r], self.dfs(l, cut_pos - 1, f, s) + self.dfs(cut_pos + 1, r, f, s))
        
        return f[l][r]
```
