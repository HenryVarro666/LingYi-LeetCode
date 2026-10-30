---
title: "2911. 得到K个半回文串的最少修改次数"
aliases: ["yiduobo的每日leetcode 2911.得到K个半回文串的最少修改次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664414149"
zhihu_id: "664414149"
zhihu_title: "yiduobo的每日leetcode 2911.得到K个半回文串的最少修改次数"
question_id: "2911"
question: "得到 K 个半回文串的最少修改次数"
problem_url: "https://leetcode.cn/problems/minimum-changes-to-make-k-semi-palindromes/"
difficulty: "Hard"
rating: 2608
created: "2023-11-01T01:48:15+08:00"
updated: "2023-11-01T01:48:15+08:00"
upvotes: 0
comments: 0
---

# 2911. 得到K个半回文串的最少修改次数

> **[yiduobo的每日leetcode 2911.得到K个半回文串的最少修改次数](https://zhuanlan.zhihu.com/p/664414149) · 知乎 · 2023-11-01 · 赞同 0**
> 力扣：[2911. 得到 K 个半回文串的最少修改次数](https://leetcode.cn/problems/minimum-changes-to-make-k-semi-palindromes/) · Hard · 灵茶山艾府：[预处理+记忆化搜索/递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2911.得到K个半回文串的最少修改次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-changes-to-make-k-semi-palindromes/)

题目的数据规模比较小，可以直接上O(n^3)的算法，那么如果先抛开半回文串判定相关的部分不看的话，很容易得到一个O(n^2 \* k)的动态规划算法。

令g[i][j]表示前i个字符，切分成j个半回文子串所需的最小代价，那么对于g[i][j]，可以枚举前j - 1个回文子串的终点p，那么就有g[i][j] \= min(g[i][j], g[p][j - 1] + cost(p + 1, i))，其中cost(p + 1, i)表示将p + 1到i这个子串转化成半回文串的最小代价。由于题目给出的字符串是常量，因此在这里可以先预处理出所有的cost，这样一来就可以在O(n)的时间内完成状态转移，因此最终的时间复杂度就是O(n^2 \* k)。

接下来的问题是进行预处理。首先同样是需要二重循环枚举所有子串，对于当前枚举到的s[i : j + 1]，首先计算其长度length \= j - i + 1，接下来则可以从1到length - 1枚举题设中的d，计算每种d需要的修改次数，然后取其中的最小值作为cost[i][j]。

在这里需要先满足length是d的倍数，接下来则需要分别计算将对d取模为0到d - 1之间的所有字符组转化为回文串所需的最少操作数。具体来说，在这里可以使用offset从0枚举到d - 1，然后使用两个指针left和right，分别从i + offset和j - d + offset + 1向中间以d为步长进行遍历，直到二者相遇，在此过程中若s[left]与s[right]不同，那么就需要将当前d对应的cost加上1。

这个预处理的过程看上去像是O(n^4)的，但是实际上后面两重循环最终只会遍历s中每个字符一次，因此总体的时间复杂度还是O(n^3)。

最后附上python代码：

```python
class Solution(object):
    def minimumChanges(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)
        f = [[None] * n for _ in range(n)]
        for i in range(n - 1):
            for j in range(i + 1, n):
                length = j - i + 1
                for d in range(1, length):
                    if length % d == 0:
                        cnt = 0
                        for offset in range(d):
                            left = i + offset
                            right = j - d + offset + 1
                            while left < right:
                                if s[left] != s[right]:
                                    cnt += 1
                                left += d
                                right -= d
                            
                        if f[i][j] is None or f[i][j] > cnt:
                            f[i][j] = cnt
        
        g = [[None] * (k + 1) for _ in range(n + 1)]
        g[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for p in range(i):
                    if g[p][j - 1] is None:
                        continue
                    if f[p][i - 1] is None:
                        continue
                    if g[i][j] is None or g[i][j] > g[p][j - 1] + f[p][i - 1]:
                        g[i][j] = g[p][j - 1] + f[p][i - 1]
        
        return g[-1][-1]
```
