---
title: "1048. 最长字符串链"
aliases: ["yiduobo的每日leetcode 1048.最长字符串链"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371552783"
zhihu_id: "371552783"
zhihu_title: "yiduobo的每日leetcode 1048.最长字符串链"
question_id: "1048"
question: "最长字符串链"
problem_url: "https://leetcode.cn/problems/longest-string-chain/"
difficulty: "Medium"
rating: 1599
created: "2021-05-11T23:26:18+08:00"
updated: "2021-05-11T23:26:18+08:00"
upvotes: 0
comments: 0
---

# 1048. 最长字符串链

> **[yiduobo的每日leetcode 1048.最长字符串链](https://zhuanlan.zhihu.com/p/371552783) · 知乎 · 2021-05-11 · 赞同 0**
> 力扣：[1048. 最长字符串链](https://leetcode.cn/problems/longest-string-chain/) · Medium · 灵茶山艾府：[教你一步步思考动态规划！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1048.最长字符串链

[力扣](https://leetcode-cn.com/problems/longest-string-chain/)

看上去与最长上升子序列问题有些类似，但是这里的上升是word1在某个位置添加一个字母得到word2，那么我们可以将words按单词长度从小到大排序后使用动态规划求解。

相比与经典的f[i]表示以第i个单词结尾时的最优解，在这里我才用的是f[word]表示以单词word结尾的最优解，那么对于当前处理的word，我们可以枚举其中的每个字符，然后尝试删去这个字符之后得到前置字符串tmp，那么就有f[word] \= max(f[word], f[tmp] + 1)。这样做的好处是传统f[i]表示下，状态转移需要枚举words[j]并判断words[i]能否由words[j]形成，而是用f[word]表示则只需要检测特定的几个f[tmp]，效率上会更好一点。

最后附上python代码：

```python
class Solution(object):
    def longestStrChain(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        f = {}
        res = 1
        for word in sorted(words, key=lambda d:len(d)):
            l = 1
            for pos in range(len(word)):
                tmp = word[:pos] + word[pos + 1:]
                l = max(l, f.get(tmp, 0) + 1)
            
            f[word] = l
            res = max(res, l)
        
        return res
```
