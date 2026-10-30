---
title: "1967. 作为子字符串出现在单词中的字符串数目"
aliases: ["yiduobo的每日leetcode 1967.作为子字符串出现在单词中的字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string-matching", "leetcode/aho-corasick-algorithm", "题单/字符串", "题单/字符串/七-AC-自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/494726441"
zhihu_id: "494726441"
zhihu_title: "yiduobo的每日leetcode 1967.作为子字符串出现在单词中的字符串数目"
question_id: "1967"
question: "作为子字符串出现在单词中的字符串数目"
problem_url: "https://leetcode.cn/problems/number-of-strings-that-appear-as-substrings-in-word/"
difficulty: "Easy"
created: "2022-04-07T21:01:49+08:00"
updated: "2022-04-07T21:01:49+08:00"
upvotes: 0
comments: 0
---

# 1967. 作为子字符串出现在单词中的字符串数目

> **[yiduobo的每日leetcode 1967.作为子字符串出现在单词中的字符串数目](https://zhuanlan.zhihu.com/p/494726441) · 知乎 · 2022-04-07 · 赞同 0**
> 力扣：[1967. 作为子字符串出现在单词中的字符串数目](https://leetcode.cn/problems/number-of-strings-that-appear-as-substrings-in-word/) · Easy · 灵茶山艾府：[两种方法：暴力 / AC 自动机（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1967.作为子字符串出现在单词中的字符串数目

[力扣](https://leetcode-cn.com/problems/number-of-strings-that-appear-as-substrings-in-word/)

由于题目的数据规模较小，因此可以直接枚举每个pattern，然后暴力检测其是否是word的子串。我在这里采用了kmp做匹配，可以稍微起到点优化的作用。

最后附上python代码：

```python
class Solution(object):
    def numOfStrings(self, patterns, word):
        """
        :type patterns: List[str]
        :type word: str
        :rtype: int
        """

        res = 0
        for pattern in patterns:
            f = [0]
            pos = 0
            for index in range(1, len(pattern)):
                while pos > 0 and pattern[pos] != pattern[index]:
                    pos = f[pos - 1]
                if pattern[pos] == pattern[index]:
                    pos += 1
                f.append(pos)
        
            pos = 0
            for char in word:
                while pos > 0 and pattern[pos] != char:
                    pos = f[pos - 1]
                if pattern[pos] == char:
                    pos += 1
                if pos == len(pattern):
                    res += 1
                    break
                    
        return res
```
