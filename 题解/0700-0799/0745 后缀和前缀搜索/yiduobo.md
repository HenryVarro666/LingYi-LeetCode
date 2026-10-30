---
title: "745. 后缀和前缀搜索"
aliases: ["yiduobo的每日leetcode 745.后缀和前缀搜索"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337471573"
zhihu_id: "337471573"
zhihu_title: "yiduobo的每日leetcode 745.后缀和前缀搜索"
question_id: "745"
question: "后缀和前缀搜索"
problem_url: "https://leetcode.cn/problems/prefix-and-suffix-search/"
created: "2020-12-16T22:53:49+08:00"
updated: "2020-12-16T22:53:49+08:00"
upvotes: 0
comments: 0
---

# 745. 后缀和前缀搜索

> **[yiduobo的每日leetcode 745.后缀和前缀搜索](https://zhuanlan.zhihu.com/p/337471573) · 知乎 · 2020-12-16 · 赞同 0**
> 力扣：[745. 后缀和前缀搜索](https://leetcode.cn/problems/prefix-and-suffix-search/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

745.后缀和前缀搜索

[力扣](https://leetcode-cn.com/problems/prefix-and-suffix-search/)

对于后缀与前缀相关的问题，经典的做法是使用trie树。不过注意到这里每个单词的长度不超过10，因此直接将所有的后缀与前缀进行组合，然后存入哈希表也是可行的做法。由于题目要找的是权重最大的单词，而后来的单词比前面的单词权重要大，因此可以直接从头往后扫描words，对于每个单词，枚举其所有的后缀与前缀并存入哈希表即可。

最后附上python代码：

```python
class WordFilter(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.word_dict = {}
        for index, word in enumerate(words):
            l = len(word)
            for i in range(l + 1):
                for j in range(l + 1):
                    self.word_dict[word[:i] + ' ' + word[j:]] = index

    def f(self, prefix, suffix):
        """
        :type prefix: str
        :type suffix: str
        :rtype: int
        """
        return self.word_dict.get(prefix + ' ' + suffix, -1)

# Your WordFilter object will be instantiated and called as such:
# obj = WordFilter(words)
# param_1 = obj.f(prefix,suffix)
```
