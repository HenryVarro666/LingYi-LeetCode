---
title: "884. 两句话中的不常见单词"
aliases: ["yiduobo的每日leetcode 884.两句话中的不常见单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351541414"
zhihu_id: "351541414"
zhihu_title: "yiduobo的每日leetcode 884.两句话中的不常见单词"
question_id: "884"
question: "两句话中的不常见单词"
problem_url: "https://leetcode.cn/problems/uncommon-words-from-two-sentences/"
created: "2021-02-19T22:09:04+08:00"
updated: "2021-02-19T22:09:04+08:00"
upvotes: 0
comments: 0
---

# 884. 两句话中的不常见单词

> **[yiduobo的每日leetcode 884.两句话中的不常见单词](https://zhuanlan.zhihu.com/p/351541414) · 知乎 · 2021-02-19 · 赞同 0**
> 力扣：[884. 两句话中的不常见单词](https://leetcode.cn/problems/uncommon-words-from-two-sentences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

884.两句话中的不常见单词

[力扣](https://leetcode-cn.com/problems/uncommon-words-from-two-sentences/)

题目中的不常见是在A中出现一次同时在B中没出现，或者在A中没出线同时在B中出现一次，那么综合起来就是，在两个句子中总共只出现了一次。于是可以遍历两个句子中的所有单词并统计每个单词出现的次数，然后找出那些只出现了一次的单词。

最后附上python代码：

```python
class Solution(object):
    def uncommonFromSentences(self, A, B):
        """
        :type A: str
        :type B: str
        :rtype: List[str]
        """

        word_dict = {}
        for word in A.split(' '):
            word_dict[word] = word_dict.get(word, 0) + 1
        for word in B.split(' '):
            word_dict[word] = word_dict.get(word, 0) + 1
        
        res = []
        for word, freq in word_dict.items():
            if freq == 1:
                res.append(word)
                
        return res
```
