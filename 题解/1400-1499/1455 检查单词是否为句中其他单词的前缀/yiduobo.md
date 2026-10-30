---
title: "1455. 检查单词是否为句中其他单词的前缀"
aliases: ["yiduobo的每日leetcode 1455.检查单词是否为句中其他单词的前缀"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412115254"
zhihu_id: "412115254"
zhihu_title: "yiduobo的每日leetcode 1455.检查单词是否为句中其他单词的前缀"
question_id: "1455"
question: "检查单词是否为句中其他单词的前缀"
problem_url: "https://leetcode.cn/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/"
created: "2021-09-19T22:04:40+08:00"
updated: "2021-09-19T22:04:40+08:00"
upvotes: 0
comments: 0
---

# 1455. 检查单词是否为句中其他单词的前缀

> **[yiduobo的每日leetcode 1455.检查单词是否为句中其他单词的前缀](https://zhuanlan.zhihu.com/p/412115254) · 知乎 · 2021-09-19 · 赞同 0**
> 力扣：[1455. 检查单词是否为句中其他单词的前缀](https://leetcode.cn/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1455.检查单词是否为句中其他单词的前缀

[力扣](https://leetcode-cn.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/)

由于这里句子的数目以及长度都比较小，同时只需要判断是否为前缀，因此可以直接枚举每个句子，逐个判断单词是否为该句子的前缀。

最后附上python代码：

```python
class Solution(object):
    def isPrefixOfWord(self, sentence, searchWord):
        """
        :type sentence: str
        :type searchWord: str
        :rtype: int
        """

        l = len(searchWord)

        for index, word in enumerate(sentence.split(' ')):
            if len(word) < l:
                continue

            flag = True
            for p in range(l):
                if word[p] != searchWord[p]:
                    flag = False
                    break
                
            if flag:
                return index + 1

        return -1
```
