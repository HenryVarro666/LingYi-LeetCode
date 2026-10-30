---
title: "211. 添加与搜索单词"
aliases: ["yiduobo的每日leetcode 211.添加与搜索单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147664118"
zhihu_id: "147664118"
zhihu_title: "yiduobo的每日leetcode 211.添加与搜索单词"
question_id: "211"
question: "添加与搜索单词"
problem_url: "https://leetcode.cn/problems/add-and-search-word-data-structure-design/"
created: "2020-06-11T21:40:50+08:00"
updated: "2020-06-11T21:40:50+08:00"
upvotes: 0
comments: 0
---

# 211. 添加与搜索单词

> **[yiduobo的每日leetcode 211.添加与搜索单词](https://zhuanlan.zhihu.com/p/147664118) · 知乎 · 2020-06-11 · 赞同 0**
> 力扣：[211. 添加与搜索单词](https://leetcode.cn/problems/add-and-search-word-data-structure-design/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

211.添加与搜索单词<https://leetcode-cn.com/problems/add-and-search-word-data-structure-design/>

依然是trie树的运用。按常规的方法建好树之后，在trie树中进行dfs。若当前字符为'.'，则需要尝试当前节点的所有孩子节点，否则找到当前字符对应的孩子节点进行下一步搜索即可。

我在这里依然是使用嵌套的dict实现，每个节点的值由一个dict与一个标记值组成，dict中存放的是该节点的孩子，标记则是表面该节点是否是某个单词的结尾。

最后附上python代码：

```python
class WordDictionary(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.trie = [{}, False]

    def addWord(self, word):
        """
        Adds a word into the data structure.
        :type word: str
        :rtype: None
        """
        now = self.trie
        for char in word:
            if char not in now[0]:
                now[0][char] = [{}, False]
            now = now[0][char]

        now[1] = True

    def dfs(self, now, word):
        if not word:
            return now[1]

        if word[0] == '.':
            for next_char in now[0].keys():
                if self.dfs(now[0][next_char], word[1:]):
                    return True
            return False
        else:
            if word[0] not in now[0]:
                return False
            return self.dfs(now[0][word[0]], word[1:])

    def search(self, word):
        """
        Returns if the word is in the data structure. A word could contain the dot character '.' to represent any one letter.
        :type word: str
        :rtype: bool
        """
        return self.dfs(self.trie, word)

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)
```
