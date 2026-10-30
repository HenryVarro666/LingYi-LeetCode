---
title: "3981. 统计从两个字符串形成目标字符串的不同方案数"
aliases: ["yiduobo的每日leetcode 3981.统计从两个字符串形成目标字符串的不同方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/inclusion-exclusion-principle", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057173411613488835"
zhihu_id: "2057173411613488835"
zhihu_title: "yiduobo的每日leetcode 3981.统计从两个字符串形成目标字符串的不同方案数"
question_id: "3981"
question: "统计从两个字符串形成目标字符串的不同方案数"
problem_url: "https://leetcode.cn/problems/count-distinct-ways-to-form-target-from-two-strings/"
difficulty: "Hard"
rating: 2128
created: "2026-07-07T00:28:59+08:00"
updated: "2026-07-07T00:29:00+08:00"
upvotes: 1
comments: 0
---

# 3981. 统计从两个字符串形成目标字符串的不同方案数

> **[yiduobo的每日leetcode 3981.统计从两个字符串形成目标字符串的不同方案数](https://zhuanlan.zhihu.com/p/2057173411613488835) · 知乎 · 2026-07-07 · 赞同 1**
> 力扣：[3981. 统计从两个字符串形成目标字符串的不同方案数](https://leetcode.cn/problems/count-distinct-ways-to-form-target-from-two-strings/) · Hard · 灵茶山艾府：[动态规划 + 容斥（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3981.统计从两个字符串形成目标字符串的不同方案数

<https://leetcode.cn/problems/count-distinct-ways-to-form-target-from-two-strings/>

题目给出三个由小写字母组成的字符串word1、word2以及target，三者的长度均不超过100。

现在要求计算从word1和word2中选择字符以形成target的方案数，需要满足：

- 对于target中的每个字符，从word1和word2中选择一个匹配的字符
- 从word1中选择的下标必须是严格递增的
- 从word2中选择的下标同样需要时严格递增的
- 必须从word1和word2两者中至少个选取一个字符

问可行的方案数是多少。

基于数据规模以及选取字符的规则，使用动态规划应该是没问题的。最常见的状态表示自然是f[i][j][k]表示通过word1中的前j个字符以及word2中的前k个字符构成target中的前i个字符的方案数。那么对于f[i][j][k]，自然是考虑target的第i个字符、word1的第j个字符以及word2的第k个字符的选用关系。

与常规的转移方程不同的是，这里需要处理重复以及边界情况，就会搞得很复杂。例如word1和word2两边都选择放弃，此时就会出现重复的计算。

我不太想处理这些重复的逻辑，于是选用了更复杂的状态表示：f[i][j][k]表示word1中的前j个字符以及word2中的前k个字符构成target中的前i个字符，且word1的第j个字符以及word2的第k个字符必须被使用的方案数。

这样做的理由是对于常规的状态表示，通常是后面的涵盖了前面的，但是对于本题，如果某个位置上的字符未取用，那么这种涵盖关系实际上是重复的。如果是最初的状态表示，那么在未取用某个字符串时，后续状态会自然继承前置状态，但是对于更后面的计算而言，如果前置状态的所有方案都在后继状态中，会带来各种去重的问题。反过来，如果是后面这种状态表示，word1[j - 1]和word2[k - 1]就必须被使用，也就是不同状态间必然有字符的差异，转移时就不会有重复的问题了。

反过来对于转移，则不是常规的f[i][j][k]通过前置状态转移，而是对于确定下来的target[i - 1]，需要去需要能与之匹配的word1[j - 1]或者word2[k - 1]，然后确定了j或者k之后进行转移。

具体来说，对于确定下来的j，就有f[i][j][k] \= f[i - 1][0][k] + f[i - 1][1][k] + ... f[i - 1][j - 1][k]，直观理解就是word1中，当前的word1[j - 1]匹配上了target的第i个字符target[i - 1]，那么在这里就枚举上一个匹配过的位置，然后问题就转化成了匹配target前i - 1个字符的问题。同样的，对于确定下来的k，就有f[i][j][k] \= f[i - 1][j][0] + f[i - 1][j][1] + ... + f[i - 1][j][k - 1]。

可以发现，这是两个非常典型的前缀和，那么在这里就可以使用s1[i][j][k]记录f[i][0][k]到f[i][j][k]之和，使用s2[i][j][k]记录f[i][j][0]到f[i][j][k]之和，上面的转移方程就可以写成:

- 若word1[j - 1]与target[i - 1]相同，有f[i][j][k] +\= s1[i - 1][j - 1][k]
- 若word2[k - 1]与target[i - 1]相同，有f[i][j][k] +\= s2[i - 1][j][k - 1]

全部计算完成后，答案就是f[-1][j][k]中所有j和k同时非0的项之和。这里非0是因为题目要求从word1和word2中至少取用一个字符。

另外，注意到上面f通过上一轮的s1和s2计算得到，而s1和s2则是通过本轮的f计算得到，因此可以互相迭代，省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def interleaveCharacters(self, word1, word2, target):
        """
        :type word1: str
        :type word2: str
        :type target: str
        :rtype: int
        """
        
        len1 = len(word1)
        len2 = len(word2)
        n = len(target)

        f = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        s1 = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        s2 = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        f[0][0] = 1
        mod = 10 ** 9 + 7
        rnd = 1
        for c in target:
            for j in range(len2 + 1):
                s1[0][j] = f[0][j]
                for i in range(1, len1):
                    s1[i][j] = s1[i - 1][j] + f[i][j]
                    if s1[i][j] >= mod:
                        s1[i][j] -= mod

            for i in range(len1 + 1):
                s2[i][0] = f[i][0]
                for j in range(1, len2):
                    s2[i][j] = s2[i][j - 1] + f[i][j]
                    if s2[i][j] >= mod:
                        s2[i][j] -= mod

            f = [[0] * (len2 + 1) for _ in range(len1 + 1)]
            for i in range(1, len1 + 1):
                if word1[i - 1] == c:
                    for j in range(len2 + 1):
                        f[i][j] += s1[i - 1][j]
                        if f[i][j] >= mod:
                            f[i][j] -= mod
            
            for j in range(1, len2 + 1):
                if word2[j - 1] == c:
                    for i in range(len1 + 1):
                        f[i][j] += s2[i][j - 1]
                        if f[i][j] >= mod:
                            f[i][j] -= mod
    
        res = 0
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                res += f[i][j]
                if res >= mod:
                    res -= mod
        return res
```
