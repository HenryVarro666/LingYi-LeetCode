---
title: "1977. 划分数字的方案数"
aliases: ["yiduobo的每日leetcode 1977.划分数字的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/十一-优化-DP", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/496909108"
zhihu_id: "496909108"
zhihu_title: "yiduobo的每日leetcode 1977.划分数字的方案数"
question_id: "1977"
question: "划分数字的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-separate-numbers/"
difficulty: "Hard"
rating: 2817
created: "2022-04-12T01:12:56+08:00"
updated: "2022-04-12T01:12:56+08:00"
upvotes: 0
comments: 0
---

# 1977. 划分数字的方案数

> **[yiduobo的每日leetcode 1977.划分数字的方案数](https://zhuanlan.zhihu.com/p/496909108) · 知乎 · 2022-04-12 · 赞同 0**
> 力扣：[1977. 划分数字的方案数](https://leetcode.cn/problems/number-of-ways-to-separate-numbers/) · Hard · 灵茶山艾府：[预处理 + 动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1977.划分数字的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-separate-numbers/)

经典的动态规划问题。令f[i][j]表示字符串中的前i个字符，将最后j个字符划分成一个单独数字时可行的方案数。那么对于f[i][j]，最后一个数字就是nums[i - j : i]：

1、先考虑特殊情况。若此时nums[i - j]是0，由于题目要求不能出现前导0，因此有f[i][j] \= 0

2、接下来考虑另一种特殊情况。若i \= j，那么此时nums[:i]就是一整个数字，因此有f[i][j] \= 1

3、接下来考虑一般情况。对于所有的j \< i，其可能从f[i - j][k]转移而来，即前i - j个字符，取最后k个字符作为划分的情况数，再接上最后这j个字符。此时就需要满足nums[i - j - k : i - j] \<\= nums[i - j : i]。

对于上面这个不等式，若这个字符长度k \< j，那么显然满足nums[i - j - k : i - j] \< nums[i - j : i]，而相对的，若k > j，那么显然有nums[i - j - k : i - j] > nums[i - j : i]。除此之外，当k \= j时，则需要详细比较这两个字符的大小。综合起来就是

若nums[i - j - j : i - j] \< nums[i - j : i]，有

f[i][j] \= f[i - j][1] + f[i - j][2] + ... + f[i - j][j - 1] + f[i - j][j]

否则就有

f[i][j] \= f[i - j][1] + f[i - j][2] + ... + f[i - j][j - 1]

动态规划完成后，最终答案就是sum(f[n])。

以上的做法状态表示是平方级的，状态转移的复杂度为O(n)，因此最终的时间复杂度为O(n^3)。这个做法时间复杂度略高，需要想办法进行优化。

在状态表示方面，没有太好的优化方案，只能从状态转移上想办法。状态转移方程需要考虑两个地方，分别为计算f[i - j][1] + f[i - j][2] + ... + f[i - j][j - 1]这个式子的和，以及判断字符串nums[i - j - j : i - j]与nums[i - j : i]的大小。

前者是个很常见的前缀和式子，那么完全可以在计算完所有的f[i - j]之后，使用一个数组s来储存f[i - j]的前缀和，在后续的计算中只需要使用s来更新f即可。

而对于后者，则可以先计算出nums中任意两个后缀的最长公共前缀的长度，这个过程可以用常规的O(n^2)的做法，从后向前进行动态规划。令g[i][j]表示nums[i:]与nums[j:]的最长前缀的长度，那么只有当nums[i] \= nums[j]时，g[i][j] \= g[i + 1][j + 1] + 1，否则g[i][j] \= 0。

在得到了任意两个后缀的最长公共前缀的长度后，对于nums[i - j - j : i - j]与nums[i - j : i]大小的判断，则可以利用这个最长公共前缀。

位于最长公共前缀内的字符显然是相同的，那么若最长公共前缀的长度大于等于j，就有nums\[i - j - j : i - j\] \= nums\[i - j : i\]，可以将f\[i - j\]\[j\]累加到答案中。另一方面，若最长公共前缀的长度小于j，则可以根据最长公共前缀的下一个字符的大小关系来判断二者的大小，具体来说就是若此时nums\[i - j - j + g\[i - j\]\[i - j - j\]\] \< nums\[i - j + g\[i - j\]\[i - j - j\]\]，那么就可以将f\[i - j\]\[j\]累加到答案中。

根据上面的两步操作，就可以将整个转移过程优化到O(1)了，这样一来就得到了一种O(n^2)的算法，足以适配题目的数据规模了。

最后附上python代码：

```python
class Solution(object):
    def numberOfCombinations(self, num):
        """
        :type num: str
        :rtype: int
        """

        n = len(num)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        s = [[0] * (n + 1) for _ in range(n + 1)]
        g = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if num[i] == num[j]:
                    if i == n - 1 or j == n - 1:
                        g[i][j] = 1
                    else:
                        g[i][j] = g[i + 1][j + 1] + 1

        if num[0] == '0':
            return 0
        
        f[1][1] = 1
        s[1][1] = 1
        mod = 10 ** 9 + 7
        for i in range(2, n + 1):
            f[i][i] = 1
            for j in range(i - 1, 0, -1):
                if num[i - j] == '0':
                    f[i][j] = 0
                    continue
                if j - 1 <= i - j:
                    f[i][j] = s[i - j][j - 1]
                else:
                    f[i][j] = s[i - j][i - j]

                if i - j - j >= 0 and num[i - j - j] != '0' and (g[i - j][i - j - j] >= j or num[i - j + g[i - j][i - j - j]] > num[i - j - j + g[i - j][i - j - j]]):
                        f[i][j] += f[i - j][j]
                        if f[i][j] >= mod:
                            f[i][j] -= mod
        
            for j in range(1, i + 1):
                s[i][j] = s[i][j - 1] + f[i][j]
                if s[i][j] >= mod:
                    s[i][j] -= mod

        res = 0
        for i in range(n + 1):
            res += f[n][i]
            if res >= mod:
                res -= mod
        
        return res
```
