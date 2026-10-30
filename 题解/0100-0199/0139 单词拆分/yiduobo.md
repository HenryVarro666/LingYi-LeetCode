---
title: "139. 单词拆分 & 140. 单词拆分II"
aliases: ["yiduobo的每日leetcode 139.单词拆分 && 140.单词拆分II", "139. 单词拆分", "140. 单词拆分II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/六-字典树-trie", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP", "题单/LeetCode-热题-100/动态规划", "题单/面试经典-150-题/一维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142165551"
zhihu_id: "142165551"
zhihu_title: "yiduobo的每日leetcode 139.单词拆分 && 140.单词拆分II"
question_id: ["139", "140"]
question: ["单词拆分", "单词拆分II"]
problem_url: ["https://leetcode.cn/problems/word-break/", "https://leetcode.cn/problems/word-break-ii/"]
difficulty: "Medium"
created: "2020-05-19T23:08:27+08:00"
updated: "2020-05-19T23:08:27+08:00"
upvotes: 0
comments: 0
---

# 139. 单词拆分 & 140. 单词拆分II

> **[yiduobo的每日leetcode 139.单词拆分 && 140.单词拆分II](https://zhuanlan.zhihu.com/p/142165551) · 知乎 · 2020-05-19 · 赞同 0**
> 力扣：[139. 单词拆分](https://leetcode.cn/problems/word-break/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[140. 单词拆分II](https://leetcode.cn/problems/word-break-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

139.单词拆分<https://leetcode-cn.com/problems/word-break/>

140.单词拆分II <https://leetcode-cn.com/problems/word-break-ii/>

又是经典的字符串动态规划问题，还是老样子，设f[i]表示s的前i位怎么怎么样。

对于139题，设f[i]表示s的前i位能否被拆分，然后对于f[i]，我们从0到i - 1枚举分割点j。如果存在j满足f[j]为True，且s[j : i]这一段在wordDict中，那么当前的f[i]为True，否则为False。

对于140题，做法差不多，不过这里f[i]表示s的前i位如果能被拆分，那么当前这一位可能拆成哪些单词。同样是枚举分割点，如果存在j满足f[j]非空，且s[j : i]这一段在wordDict中，那么将s[j : i]加入到f[i]中。

在求出最后的f[len(s)]后，使用记忆化搜索，res[i]表示前i位的拆分方案，然后每次枚举的f[i]中的单词word，先递归求解出res[i - len(word)]后将其拼上word后加入到res[i]的一种方案即可。

最后附上140题的python代码，139题可以参考第一个二重循环中的状态转移方程：

```python
class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """

        word_set = set(wordDict)
        f = [[] for _ in range(len(s) + 1)]

        for i in range(1, len(s) + 1):
            for j in range(i):
                if (j == 0 or len(f[j]) > 0) and s[j : i] in word_set:
                    f[i].append(s[j : i])

        if not f[len(s)]:
            return []

        res = [None] * (len(s) + 1)
        self.dfs(f, len(s), res)
        return [' '.join(x) for x in res[len(s)]]

    def dfs(self, f, now, res):
        if now == 0:
            return [[]]
        if not res[now]:
            res[now] = []
            for word in f[now]:
                tmp = self.dfs(f, now - len(word), res)
                res[now].extend(x + [word] for x in tmp)

        return res[now]
```
