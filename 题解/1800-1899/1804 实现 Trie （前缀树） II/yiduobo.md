---
title: "1804. 实现Trie（前缀树）II"
aliases: ["yiduobo的每日leetcode 1804.实现Trie（前缀树）II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/trie", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621783168"
zhihu_id: "621783168"
zhihu_title: "yiduobo的每日leetcode 1804.实现Trie（前缀树）II"
question_id: "1804"
question: "实现 Trie （前缀树） II"
problem_url: "https://leetcode.cn/problems/implement-trie-ii-prefix-tree/"
difficulty: "Medium"
created: "2023-04-13T23:49:55+08:00"
updated: "2023-04-13T23:49:55+08:00"
upvotes: 0
comments: 0
---

# 1804. 实现Trie（前缀树）II

> **[yiduobo的每日leetcode 1804.实现Trie（前缀树）II](https://zhuanlan.zhihu.com/p/621783168) · 知乎 · 2023-04-13 · 赞同 0**
> 力扣：[1804. 实现 Trie （前缀树） II](https://leetcode.cn/problems/implement-trie-ii-prefix-tree/) · Medium · 灵茶山艾府：[Go 写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1804.实现Trie（前缀树）II

[力扣](https://leetcode.cn/problems/implement-trie-ii-prefix-tree/)

题目要求实现trie树，不过除了常规的结构外，还需要维护每个字符串出现的次数以及每种前缀出现的次数，因此对于其中的每个节点，都需要额外维护两个成员变量end_cnt以及prefix_cnt，分别表示当前字符串出现的次数以及当前字符串为前缀的字符串的数量，接下来就只需要在每次插入和删除操作中维护这两个变量即可。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.childs = {}
        self.end_cnt = 0
        self.prefix_cnt = 0

class Trie(object):

    def __init__(self):
        self.root = Node()

    def insert(self, word):
        """
        :type word: str
        :rtype: None
        """

        now = self.root
        for char in word:
            if char not in now.childs:
                node = Node()
                now.childs[char] = node

            now = now.childs[char]
            now.prefix_cnt += 1
        
        now.end_cnt += 1

    def countWordsEqualTo(self, word):
        """
        :type word: str
        :rtype: int
        """

        now = self.root
        for char in word:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.end_cnt

    def countWordsStartingWith(self, prefix):
        """
        :type prefix: str
        :rtype: int
        """

        now = self.root
        for char in prefix:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.prefix_cnt

    def erase(self, word):
        """
        :type word: str
        :rtype: None
        """

        now = self.root
        for char in word:
            now = now.childs[char]
            now.prefix_cnt -= 1
        
        now.end_cnt -= 1

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.countWordsEqualTo(word)
# param_3 = obj.countWordsStartingWith(prefix)
# obj.erase(word)
```
