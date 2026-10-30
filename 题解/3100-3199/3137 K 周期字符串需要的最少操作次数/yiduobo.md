---
title: "3137. K周期字符串需要的最少操作次数"
aliases: ["yiduobo的每日leetcode 3137.K周期字符串需要的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702629912"
zhihu_id: "702629912"
zhihu_title: "yiduobo的每日leetcode 3137.K周期字符串需要的最少操作次数"
question_id: "3137"
question: "K 周期字符串需要的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-word-k-periodic/"
difficulty: "Medium"
created: "2024-06-11T00:15:07+08:00"
updated: "2024-06-11T00:15:07+08:00"
upvotes: 0
comments: 0
---

# 3137. K周期字符串需要的最少操作次数

> **[yiduobo的每日leetcode 3137.K周期字符串需要的最少操作次数](https://zhuanlan.zhihu.com/p/702629912) · 知乎 · 2024-06-11 · 赞同 0**
> 力扣：[3137. K 周期字符串需要的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-word-k-periodic/) · Medium · 灵茶山艾府：[统计子串个数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3137.K周期字符串需要的最少操作数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-make-word-k-periodic/description/)

题目给出一个长度为n的字符串以及一个整数k，其中n是k的倍数。可以从字符串中选出两个下标i、j，要求i和j都是k的倍数，然后用从j开始的，长度为k的子串覆盖从i开始的，长度为k的子串。问至少需要执行几次覆盖操作才能使得字符串变为k周期字符串，这里的k周期字符串指的是字符串可以由同一段长度为k的子串重复若干次得到。

由于每次覆盖操作的子串的起点必须是k的倍数，且长度为k，换言之本题实际上就是将原字符串按k的长度划分为若干个子串，问其中出现次数最多的子串的出现次数是多少。于是只需遍历所有子串的起点，提取出对应的子串，然后利用哈希表计算每种子串出现的次数，而最终答案就是子串的总数减去哈希表中的最多次数即可。

最后附上python代码：

```python
class Solution(object):
    def minimumOperationsToMakeKPeriodic(self, word, k):
        """
        :type word: str
        :type k: int
        :rtype: int
        """

        freq = Counter()
        for index in range(0, len(word), k):
            substr = word[index : index + k]
            freq[substr] += 1
        
        return len(word) // k - max(freq.values())
```
