---
title: "583. 两个字符串的删除操作"
aliases: ["yiduobo的每日leetcode 583.两个字符串的删除操作"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267142849"
zhihu_id: "267142849"
zhihu_title: "yiduobo的每日leetcode 583.两个字符串的删除操作"
question_id: "583"
question: "两个字符串的删除操作"
problem_url: "https://leetcode.cn/problems/delete-operation-for-two-strings/"
created: "2020-10-20T21:21:09+08:00"
updated: "2020-10-20T21:21:09+08:00"
upvotes: 0
comments: 0
---

# 583. 两个字符串的删除操作

> **[yiduobo的每日leetcode 583.两个字符串的删除操作](https://zhuanlan.zhihu.com/p/267142849) · 知乎 · 2020-10-20 · 赞同 0**
> 力扣：[583. 两个字符串的删除操作](https://leetcode.cn/problems/delete-operation-for-two-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

583.两个字符串的删除操作<https://leetcode-cn.com/problems/delete-operation-for-two-strings/>

之前好像有这个题的升级版，就是除了删除还可以替换或者插入。这题也是使用动态规划，状态f[i][j]表示第一个串的前i位和第二个串的前j位如果要匹配需要多少次操作，那么对于f[i][j]：

1、若i为0，且j为0：若word1[i]等于word2[j]，那么f[i][j] \= 0，否则f[i][j] \= 2，表示分别删去了第0位。

2、若i为0，且j不为0：若word1[i]等于word2[j]，那么f[i][j] \= j，表示删去word2中0到j - 1这一共j位字符，否则f[i][j] \= f[i][j - 1] + 1，表示删去word2中的第j位字符。

3、若i不为0，且j为0：此时与情况2类似，若word1[i]等于word2[j]，则f[i][j] \= i，否则就是f[i][j] \= f[i - 1][j] + 1。

4、若i和j都不为0：若word1[i]等于word2[j]，那么就有f[i][j] \= f[i - 1][j - 1]，否则尝试删去word1的第i位字符或者删去word2的第j为字符，即f[i][j] \= min(f[i - 1][j], f[i][j - 1]) + 1。

最后附上python代码：

```python
class Solution(object):
    def minDistance(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """

        m = len(word1)
        n = len(word2)
        if m == 0:
            return n
        if n == 0:
            return m
        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        if word1[i] == word2[j]:
                            f[i][j] = 0
                        else:
                            f[i][j] = 2
                    else:
                        if word1[i] == word2[j]:
                            f[i][j] = j
                        else:
                            f[i][j] = f[i][j - 1] + 1
                elif j == 0:
                    if word1[i] == word2[j]:
                        f[i][j] = i
                    else:
                        f[i][j] = f[i - 1][j] + 1
                else:
                    if word1[i] == word2[j]:
                        f[i][j] = f[i - 1][j - 1]
                    else:
                        f[i][j] = min(f[i - 1][j], f[i][j - 1]) + 1
        
        return f[m - 1][n - 1]
```
