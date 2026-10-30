---
title: "1092. 最短公共超序列"
aliases: ["yiduobo的每日leetcode 1092.最短公共超序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/die-dai", "leetcode/shi-pin", "leetcode/dp", "leetcode/di-tui", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373678979"
zhihu_id: "373678979"
zhihu_title: "yiduobo的每日leetcode 1092.最短公共超序列"
question_id: "1092"
question: "最短公共超序列"
problem_url: "https://leetcode.cn/problems/shortest-common-supersequence/"
difficulty: "Hard"
rating: 1977
created: "2021-05-19T22:24:39+08:00"
updated: "2021-05-19T22:24:39+08:00"
upvotes: 0
comments: 0
---

# 1092. 最短公共超序列

> **[yiduobo的每日leetcode 1092.最短公共超序列](https://zhuanlan.zhihu.com/p/373678979) · 知乎 · 2021-05-19 · 赞同 0**
> 力扣：[1092. 最短公共超序列](https://leetcode.cn/problems/shortest-common-supersequence/) · Hard · 灵茶山艾府：[从递归到递推，教你一步步思考动态规划！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1092.最短公共超序列

[力扣](https://leetcode-cn.com/problems/shortest-common-supersequence/)

为了使答案最短，我们就需要尽可能地利用str1和str2中重复的部分，也就是说应当在str1和str2的最长公共子序列的基础上，在合适的位置插入str1和str2中剩余的字符从而得到最终答案。那么我们在这里也可以使用先使用动态规划求解str1和str2的最长公共子序列，在求解过程中，对于f[i][j]：

1、若str1[i - 1]等于str2[j - 1]，那么有f[i][j] \= f[i - 1][j - 1] + 1，那么此时答案应该加上str1[i - 1]

2、若不满足条件1，且f[i - 1][j] \< f[i][j - 1]，那么就有f[i][j] \= f[i][j - 1]，同时我们需要一个字符来覆盖住str2[j - 1]，因此此时答案应该加上str2[j - 1]

3、若不满足条件1和2，那么就有f[i][j] \= f[i - 1][j]，同时我们需要一个字符来覆盖住str1[i - 1]，因此此时答案应该加上str1[i - 1]

具体实现时，我们可以随着动态规划的进行同步更新答案，但这样的空间复杂度较高。注意到每次f[i][j]的更新都只与f[i - 1][j - 1]、f[i][j - 1]以及f[i - 1][j]这三种状态之一有关，同时答案取决于从哪个状态转移而来，因此我们可以维护一个数组last[i][j]，表示状态f[i][j]是从f[i - 1][j - 1]、f[i][j - 1]以及f[i - 1][j]这三种状态中的哪一种转移而来。那么在动态规划结束后，我们就可以从last[m][n]开始倒推，从而还原出最终的答案。

最后附上python代码：

```python
class Solution(object):
    def shortestCommonSupersequence(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """

        m = len(str1)
        n = len(str2)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        last = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        f[i][j] = f[i][j - 1]
                        last[i][j] = 0
                elif j == 0:
                    f[i][j] = f[i - 1][j]
                    last[i][j] = 1
                elif str1[i - 1] == str2[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    last[i][j] = 2
                elif f[i][j - 1] > f[i - 1][j]:
                    f[i][j] = f[i][j - 1]
                    last[i][j] = 0
                else:
                    f[i][j] = f[i - 1][j]
                    last[i][j] = 1
                
        
        res = ''
        i = m
        j = n
        while i != 0 or j != 0:
            if last[i][j] == 0:
                res = str2[j - 1] + res
                j -= 1
            else:
                res = str1[i - 1] + res
                if last[i][j] == 2:
                    i -= 1
                    j -= 1
                else:
                    i -= 1
        
        return res
```
