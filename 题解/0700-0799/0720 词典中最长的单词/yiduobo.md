---
title: "720. 词典中最长的单词"
aliases: ["yiduobo的每日leetcode 720.词典中最长的单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/332515363"
zhihu_id: "332515363"
zhihu_title: "yiduobo的每日leetcode 720.词典中最长的单词"
question_id: "720"
question: "词典中最长的单词"
problem_url: "https://leetcode.cn/problems/longest-word-in-dictionary/"
created: "2020-12-06T17:58:31+08:00"
updated: "2020-12-06T17:58:31+08:00"
upvotes: 0
comments: 0
---

# 720. 词典中最长的单词

> **[yiduobo的每日leetcode 720.词典中最长的单词](https://zhuanlan.zhihu.com/p/332515363) · 知乎 · 2020-12-06 · 赞同 0**
> 力扣：[720. 词典中最长的单词](https://leetcode.cn/problems/longest-word-in-dictionary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。、

720.词典中最长的单词

[力扣](https://leetcode-cn.com/problems/longest-word-in-dictionary/)

题目要求从词典中找出最长的单词，满足这个单词的所有前缀也都在词典中。我的做法是用一个set来储存所有可以通过添加字符形成的单词，然后将词典中的词按长度进行排序之后遍历词典。若某个单词的长度为1，或者其去除最后一个字符后在set中，那么就将该词加入到set中，同时更新答案。

最后附上python代码：

```python
class Solution(object):
    def longestWord(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        word_set = set()
        res = ''
        for word in sorted(words, key=lambda d:len(d)):
            if len(word) == 1 or word[:-1] in word_set:
                word_set.add(word)
                if (len(word) > len(res)) or (len(word) == len(res) and word < res):
                    res = word
        
        return res
```
