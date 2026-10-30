---
title: "524. 通过删除字母匹配到字典里最长单词"
aliases: ["yiduobo的每日leetcode 524.通过删除字母匹配到字典里最长单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261130813"
zhihu_id: "261130813"
zhihu_title: "yiduobo的每日leetcode 524.通过删除字母匹配到字典里最长单词"
question_id: "524"
question: "通过删除字母匹配到字典里最长单词"
problem_url: "https://leetcode.cn/problems/longest-word-in-dictionary-through-deleting/"
created: "2020-10-02T19:27:51+08:00"
updated: "2020-10-02T19:27:51+08:00"
upvotes: 0
comments: 0
---

# 524. 通过删除字母匹配到字典里最长单词

> **[yiduobo的每日leetcode 524.通过删除字母匹配到字典里最长单词](https://zhuanlan.zhihu.com/p/261130813) · 知乎 · 2020-10-02 · 赞同 0**
> 力扣：[524. 通过删除字母匹配到字典里最长单词](https://leetcode.cn/problems/longest-word-in-dictionary-through-deleting/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

524.通过删除字母匹配到字典里最长单词<https://leetcode-cn.com/problems/longest-word-in-dictionary-through-deleting/>

题目要求删除某些字母匹配字典里的单词，实际上就是检测d里的单词是否是s的子序列。对于判断是否是子序列的问题，可以使用之前用过的贪心法，从头到尾一趟扫描尽可能匹配字符。

注意到题目保证d的长度和所有字符串的长度都不超过1000，那么就可以直接枚举d中的所有单词，判断其是否是s的子序列，保留最长且字典序最小的那一个作为答案。

一个小优化是若当前单词的长度大于当前最优解的长度，或者长度等于当前最优解的长度且字典序小于当前最优解的字典序，这个单词才有可能成为新的最优解，否则就没有必要进行后续是否是s子序列的判断了。

最后附上python代码：

```python
class Solution(object):
    def findLongestWord(self, s, d):
        """
        :type s: str
        :type d: List[str]
        :rtype: str
        """

        res = ''
        for now in d:
            if len(now) < len(res) or (len(now) == len(res) and now > res):
                continue
            pos = 0
            for char in s:
                if char == now[pos]:
                    pos += 1
                    if pos == len(now):
                        res = now
                        break

        return res
```
