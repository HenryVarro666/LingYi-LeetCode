---
title: "3485. 删除元素后K个字符串的最长公共前缀"
aliases: ["yiduobo的每日leetcode 3485.删除元素后K个字符串的最长公共前缀"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/sorting", "题单/字符串", "题单/字符串/十-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897409543203451265"
zhihu_id: "1897409543203451265"
zhihu_title: "yiduobo的每日leetcode 3485.删除元素后K个字符串的最长公共前缀"
question_id: "3485"
question: "删除元素后 K 个字符串的最长公共前缀"
problem_url: "https://leetcode.cn/problems/longest-common-prefix-of-k-strings-after-removal/"
difficulty: "Hard"
rating: 2290
created: "2025-04-23T22:08:34+08:00"
updated: "2025-04-23T22:08:34+08:00"
upvotes: 1
comments: 0
---

# 3485. 删除元素后K个字符串的最长公共前缀

> **[yiduobo的每日leetcode 3485.删除元素后K个字符串的最长公共前缀](https://zhuanlan.zhihu.com/p/1897409543203451265) · 知乎 · 2025-04-23 · 赞同 1**
> 力扣：[3485. 删除元素后 K 个字符串的最长公共前缀](https://leetcode.cn/problems/longest-common-prefix-of-k-strings-after-removal/) · Hard · 灵茶山艾府：[排序 + LCP 性质 + 简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3485.删除元素后K个字符串的最长公共前缀

[3485. 删除元素后 K 个字符串的最长公共前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-common-prefix-of-k-strings-after-removal/description/)

题目给出一个字符串数组words以及一个整数k，现在要求对于0到len(words) - 1之间的所有下标index，都计算在移除words[index]后剩余的数组中，由k个不同字符串形成的最长公共前缀的最长长度。

对于至少k个不同字符串的最长公共前缀问题，一种常见的处理方法是将这些字符串都加入到trie树中，trie树中的节点除了记录孩子之外，还额外记录命中当前前缀的字符串的数量weight。

对于从trie树根节点向下的某条路径，若路径上所有节点的weight都大于等于k，说明至少有k个不同字符串都有这个公共前缀，因此符合条件的最长路径长度就是题目要求的由k个不同字符串形成的最长公共前缀的长度。

对于本题，由于还有删除操作存在，因此在使用words构造出最初的trie树后，还需要遍历words，对于当前遍历到的单词w，先使用w修正trie树中节点的weight，然后自顶向上计算满足weight大于等于k的最长路径长度，然后再消除掉这次修正对trie树中节点weight的影响。

在具体实现上，可以在构造trie树时为每个节点now设置weight以及length。其中weight的含义如上面所述，而length则表示以now向下的满足路径上所有节点weight都大于等于k的最长路径的长度。除此之外，还可以对每个节点now都记录两个孩子节点first以及second，表示now所有孩子中length最大的两个孩子分别为first和second，在初次构建trie树时就可以利用first.length + 1来更新now.length。

接下来在枚举w修正trie树的阶段，无论w对trie树进行了何种修正，其中每个节点now的length都可以按照w中节点自底向上的顺序，通过max(now.first.length, now.second.length) + 1计算得到，无需考虑到底修正的是now的哪个孩子。

最后附上python代码：

```python
class Node(object):
    def __init__(self):
        self.childs = {}
        self.fa = None
        self.weight = 0
        self.length = 0
        self.first = None
        self.second = None

class Trie(object):
    def __init__(self, words, k):
        self.root = Node()
        self.root.weight = k
        self.k = k
        for w in words:
            self.update(w, 1)
        self.calc_length(self.root)
    
    def update(self, w, delta):
        now = self.root
        for char in w:
            if char not in now.childs:
                now.childs[char] = Node()
                now.childs[char].fa = now
            now = now.childs[char]
            now.weight += delta
        return now

    def get_length(self, node):
        if node is None:
            return 0
        return node.length

    def calc_length(self, now):
        if now.weight < self.k:
            now.length = 0
            return
        
        for char in now.childs:
            self.calc_length(now.childs[char])
            if self.get_length(now.childs[char]) > self.get_length(now.first):
                now.first, now.second = now.childs[char], now.first
            elif self.get_length(now.childs[char]) > self.get_length(now.second):
                now.second = now.childs[char]
        
        now.length = self.get_length(now.first) + 1
    
    def modify_word(self, w):
        now = self.update(w, -1)
        while now:
            if now.weight < self.k:
                now.length = 0
            else:
                now.length = max(self.get_length(now.first), self.get_length(now.second)) + 1
            now = now.fa
        
        res = self.root.length

        now = self.update(w, 1)
        while now:
            if now.weight < self.k:
                now.length = 0
            else:
                now.length = max(self.get_length(now.first), self.get_length(now.second)) + 1
            now = now.fa

        return res - 1

class Solution(object):
    def longestCommonPrefix(self, words, k):
        """
        :type words: List[str]
        :type k: int
        :rtype: List[int]
        """
        
        trie = Trie(words, k)
        res = []
        for w in words:
            res.append(trie.modify_word(w))
        return res
```
