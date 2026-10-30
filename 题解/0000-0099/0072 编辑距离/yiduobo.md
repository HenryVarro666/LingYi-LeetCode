---
title: "72. 编辑距离"
aliases: ["yiduobo的每日leetcode 72.编辑距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/四-经典线性-DP", "题单/LeetCode-热题-100/多维动态规划", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/132725208"
zhihu_id: "132725208"
zhihu_title: "yiduobo的每日leetcode 72.编辑距离"
question_id: "72"
question: "编辑距离"
problem_url: "https://leetcode.cn/problems/edit-distance/"
difficulty: "Medium"
created: "2020-04-17T23:30:06+08:00"
updated: "2020-04-17T23:30:06+08:00"
upvotes: 0
comments: 0
---

# 72. 编辑距离

> **[yiduobo的每日leetcode 72.编辑距离](https://zhuanlan.zhihu.com/p/132725208) · 知乎 · 2020-04-17 · 赞同 0**
> 力扣：[72. 编辑距离](https://leetcode.cn/problems/edit-distance/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划，从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

72.编辑距离<https://leetcode-cn.com/problems/edit-distance/>

经典的动态规划问题，首先来明确插入、删除、修改这几种操作。

对于两个字符串word1、word2而言：

1、为了字符能匹配上而修改word1中的某个字符，实际上等价于修改word2中与之匹配后的字符。例如，word1\='abc'，word2\='aac'。我们将word1中的b修改成c，实际上等价于将word2中的第二个a修改成b。

2、为了字符能匹配上而删去word1中的某个字符，实际上等价于在word2对应位置上插入word1中删去的字符。例如，word1\='abc'，word2\='ac'。我们将word1中的b删去，实际上等价于在word2的对应位置，也就是a后面插入一个b。

3、反过来，为了字符匹配而在word1中插入字符，实际上等价于删去word2对应位置上的字符。例如，word1\='ac'，word2\='abc'。我们在word1的a后面插入b，实际上等价于删去word2中a后面的b。

可以发现，所有操作都可以认为是在同一个字符串上进行的，于是就可以问题当成从字符串word1变换到固定的字符串word2需要多少步。

令f[i][j]表示word2的前j位需要经历多少次操作才能变成word1的前i位，那么有：

1、i和j都为0。此时两边都是空串，f[i][j] \= 0。

2、i为0，j不为0。说明word2必须删去所有的前j位，于是有f[i][j] \= j。

3、i不为0，j为0。与上面相反，说明word2必须完全复制word1的前i位，即插入i位，于是有f[i][j] \= i。

4、i和j都不为0，且word1[i - 1] \=\= word2[j - 1]。此时不需要插入、删除或替换中的任意操作，于是有f[i][j] \= f[i - 1][j - 1]。

5、i和j都不为0，且word1[i - 1] !\= word2[j - 1]。那么此时可以：

1）在word2[j - 1]后面插入word1[i - 1]，于是此时的总操作数为f[i - 1][j] + 1。

2）删去word2[j - 1]，于是此时的总操作数为f[i][j - 1] + 1。

3）将word2[j - 1]替换成word1[i - 1]，于是此时的总操作数为f[i - 1][j - 1] + 1。

因此，最终的f[i][j] \= min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1。

一个可能的疑问是，为什么情况4中不进行任何操作，而不是像在情况5中一样也考虑插入与删除的情况？

因为对于f[i - 1][j - 1]而言，其与f[i][j - 1]，f[i - 1][j]的差值至多为1，即使用一次操作即可消除两种状态所代表的串之间的差异。

因此在情况4中，就有f[i - 1][j - 1] \<\= min(f[i][j - 1], f[ii - 1][j]) + 1，所以没有必要再考虑插入或删除的情况。

最终的时间复杂度为O(mn)，m和n分别为两个串的长度。空间方面如果用二维数组来做那就是O(mn)，当然也可以使用滚动数组来做，那么空间复杂度就是O(min(m, n))。

最后附上python代码，方便起见这里没有用滚动数组：

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

        f = [[0 for i in range(n + 1)] for j in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = 0
                    else:
                        f[i][j] = j
                else:
                    if j == 0:
                        f[i][j] = i
                    else:
                        if word1[i - 1] == word2[j - 1]:
                            f[i][j] = f[i - 1][j - 1]
                        else:
                            f[i][j] = min(f[i - 1][j - 1], f[i][j - 1], f[i - 1][j]) + 1
        return f[m][n]
```
