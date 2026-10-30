---
title: "472. 连接词"
aliases: ["yiduobo的每日leetcode 472.连接词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/235600868"
zhihu_id: "235600868"
zhihu_title: "yiduobo的每日leetcode 472.连接词"
question_id: "472"
question: "连接词"
problem_url: "https://leetcode.cn/problems/concatenated-words/"
created: "2020-09-11T23:24:37+08:00"
updated: "2020-09-11T23:24:37+08:00"
upvotes: 0
comments: 0
---

# 472. 连接词

> **[yiduobo的每日leetcode 472.连接词](https://zhuanlan.zhihu.com/p/235600868) · 知乎 · 2020-09-11 · 赞同 0**
> 力扣：[472. 连接词](https://leetcode.cn/problems/concatenated-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

472.连接词<https://leetcode-cn.com/problems/concatenated-words/>

这一题暂时没有什么好的思路，总体来说就是从短到长逐个通过dfs进行检测。检测过程中可以使用trie树或者set，配合上记忆化搜索的方式来进行优化，但是整体的复杂度依然很高。

我在这里采用的是set加记忆化搜索的做法，首先对所有单词按长度从短到长进行排序，这一步的理由是只可能是较长的单词由较短的单词组成，因此优先判断短的单词。然后逐个判断当前的单词是否能由之前的单词组成，具体的判断方法为使用f[i]表示当前单词的前i个字符是否能由之前的单词组成，然后进行记忆化搜索。

最后附上python代码：

```python
class Solution(object):
    def findAllConcatenatedWordsInADict(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """

        if not words:
            return []

        words = sorted(words, key=lambda d:len(d))
        word_set = set()
        res = []
        for word in words:
            if not word:
                continue
            f = [None] * len(word)
            if self.check(word, 0, word_set, f):
                res.append(word)
            else:
                word_set.add(word)

        return res

    def check(self, word, start_pos, word_set, f):
        if f[start_pos] is not None:
            return f[start_pos]
        if word[start_pos:] in word_set:
            f[start_pos] = True
            return True

        for pos in range(start_pos, len(word)):
            if word[start_pos:pos] in word_set:
                if self.check(word, pos, word_set, f):
                    f[start_pos] = True
                    return True
            
        f[start_pos] = False
        return False
```
