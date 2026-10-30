---
title: "208. 实现Trie（前缀树）"
aliases: ["yiduobo的每日leetcode 208.实现Trie（前缀树）"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/trie", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/六-字典树-trie", "题单/LeetCode-热题-100/图论", "题单/面试经典-150-题/字典树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147051263"
zhihu_id: "147051263"
zhihu_title: "yiduobo的每日leetcode 208.实现Trie（前缀树）"
question_id: "208"
question: "实现 Trie (前缀树)"
problem_url: "https://leetcode.cn/problems/implement-trie-prefix-tree/"
difficulty: "Medium"
created: "2020-06-09T22:00:10+08:00"
updated: "2020-06-09T22:00:10+08:00"
upvotes: 0
comments: 0
---

# 208. 实现Trie（前缀树）

> **[yiduobo的每日leetcode 208.实现Trie（前缀树）](https://zhuanlan.zhihu.com/p/147051263) · 知乎 · 2020-06-09 · 赞同 0**
> 力扣：[208. 实现 Trie (前缀树)](https://leetcode.cn/problems/implement-trie-prefix-tree/) · Medium · 灵茶山艾府：[从二叉树到二十六叉树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

208.实现Trie（前缀树）<https://leetcode-cn.com/problems/implement-trie-prefix-tree/>

经典的数据结构问题，不过感觉用python写起来怪怪的。

我的做法是对于每个节点都维护一个dict，若当前字符在dict中，那么迭代到dict中的对应节点，否则在dict中加入对应的节点并迭代过去。若当前字符是单词的最后一个字符，则在当前节点中置一个标记表示从根到当前节点的路径是某个词。

最后附上python代码：

```python
class Trie(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: None
        """
        now = self.root
        for char in word:
            if char not in now:
                now[char] = {}
            now = now[char]
        now['end'] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        now = self.root
        for char in word:
            if char not in now:
                return False
            now = now[char]
            
        return now.get('end', False)

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        now = self.root
        for char in prefix:
            if char not in now:
                return False
            now = now[char]
        
        return True

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```
