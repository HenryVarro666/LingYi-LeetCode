---
title: "87. 扰乱字符串"
aliases: ["yiduobo的每日leetcode 87.扰乱字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134182065"
zhihu_id: "134182065"
zhihu_title: "yiduobo的每日leetcode 87.扰乱字符串"
question_id: "87"
question: "扰乱字符串"
problem_url: "https://leetcode.cn/problems/scramble-string/"
created: "2020-04-24T23:10:42+08:00"
updated: "2020-04-24T23:10:42+08:00"
upvotes: 0
comments: 0
---

# 87. 扰乱字符串

> **[yiduobo的每日leetcode 87.扰乱字符串](https://zhuanlan.zhihu.com/p/134182065) · 知乎 · 2020-04-24 · 赞同 0**
> 力扣：[87. 扰乱字符串](https://leetcode.cn/problems/scramble-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

87.扰乱字符串<https://leetcode-cn.com/problems/scramble-string/>

动态规划的题目。

设f[i][j][l]表示s1从i开始，s2从j开始，长度为l的字串是否能经过反转然后匹配上。

1、那么首先边界情况l \= 1，那么此时若s1[i] \=\= s2[j]，那么f[i][j][l]为True，否则为False。

2、然后考虑l > 1的情况。我们可以枚举分隔点，将l划分为left，right两个部分，然后：

1)不进行扰乱操作：

此时需要s1[i : i + left]与s2[j : j + left]进行匹配，s1[i + left : i + l]与s2[j + left : j + l]进行匹配，那么就是当f[i][j][left]、f[i + left][j + left][right]均为True时，f[i][j][l]为True。

2)进行扰乱操作：

此时则是考察s1[i : i + left]与s2[j + right : j + l]以及s1[i + left : i + l]与s2[j : j + right]的匹配情况，那么就是当f[i][j + right][left]与f[i + left][j][right]均为True时，f[i][j][l]为True。

若所有的left与right都无法令f[i][j][l]为True，说明找不到可行的分割方案，f[i][j][l]为False。

最终答案就是f[0][0][len(s1)]。

方便起见，在实现的时候采用记忆化搜索的写法会更加简洁一些。

三维的状态空间，转移时需要一维的扫描，因此最终时间复杂度为O(n^4)。

最后附上python代码：

```python
class Solution(object):
    def isScramble(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        n = len(s1)
        if len(s2) != n:
            return False

        f = [[[None] * (n + 1) for index in range(n)] for index in range(n)]
        return self.dfs(0, 0, n, s1, s2, f)

    def dfs(self, i, j, l, s1, s2, f):
        if f[i][j][l] is not None:
            return f[i][j][l]

        if l == 1:
            if s1[i] == s2[j]:
                f[i][j][l] = True
            else:
                f[i][j][l] = False
            return f[i][j][l]

        for left in range(1, l):
            right = l - left
            if self.dfs(i, j, left, s1, s2, f) and self.dfs(i + left, j + left, right, s1, s2, f):
                f[i][j][l] = True
                return True
            if self.dfs(i, j + right, left, s1, s2, f) and self.dfs(i + left, j, right, s1, s2, f):
                f[i][j][l] = True
                return True

        f[i][j][l] = False
        return False
```
