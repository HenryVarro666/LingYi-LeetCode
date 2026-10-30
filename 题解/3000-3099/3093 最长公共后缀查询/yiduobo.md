---
title: "3093. 最长公共后缀查询"
aliases: ["yiduobo的每日leetcode 3093.最长公共后缀查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/trie", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699302183"
zhihu_id: "699302183"
zhihu_title: "yiduobo的每日leetcode 3093.最长公共后缀查询"
question_id: "3093"
question: "最长公共后缀查询"
problem_url: "https://leetcode.cn/problems/longest-common-suffix-queries/"
difficulty: "Hard"
rating: 2118
created: "2024-05-23T00:26:16+08:00"
updated: "2024-05-23T00:26:16+08:00"
upvotes: 2
comments: 0
---

# 3093. 最长公共后缀查询

> **[yiduobo的每日leetcode 3093.最长公共后缀查询](https://zhuanlan.zhihu.com/p/699302183) · 知乎 · 2024-05-23 · 赞同 2**
> 力扣：[3093. 最长公共后缀查询](https://leetcode.cn/problems/longest-common-suffix-queries/) · Hard · 灵茶山艾府：[字典树+维护最短长度和下标（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3093.最长公共后缀查询

[. - 力扣（LeetCode）](https://leetcode.cn/problems/longest-common-suffix-queries/description/)

对于公共后缀问题，如果将单词和查询都翻转，那么原题中的最长公共后缀实际上就变成了最长公共前缀问题，最直观的思路自然是trie树。

需要注意的，对于每个前缀，需要返回包含该前缀的最短的且下标最靠前的单词下标，于是在trie树中的每个节点都需要额外记录管辖每个前缀的单词下标index，方便起见还可以记录这个单词的长度length。

接下来只需倒序遍历每个单词，然后将其加入到trie树中，过程中根据当前单词的长度以及下标来更新trie树中经过节点对应的index和length。

建立好trie树后，再倒序遍历每个询问，从trie树的根节点尽量向下走，直到走完询问的每个字符或者trie树中当前节点不存在对应的字符为止，此时trie树中当前节点对应的单词下标即为当前询问对应的答案。

最后附上python代码：

```python
class TreeNode(object):
    def __init__(self, index, length):
        self.childs = {}
        self.index = index
        self.length = length

    def update(self, new_index, new_length):
        if new_length < self.length or (new_length == self.length and new_index < self.index):
            self.index = new_index
            self.length = new_length

class Trie(object):
    def __init__(self, root_index, root_length):
        self.root = TreeNode(root_index, root_length)
    
    def add(self, s, s_index):
        now = self.root
        length = len(s)
        for char in s[::-1]:
            now.update(s_index, length)
            if char not in now.childs:
                now.childs[char] = TreeNode(s_index, length)
            now = now.childs[char]

        now.update(s_index, length)
    
    def find(self, s):
        now = self.root
        for char in s[::-1]:
            if char not in now.childs:
                break
            now = now.childs[char]
        
        return now.index

class Solution(object):
    def stringIndices(self, wordsContainer, wordsQuery):
        """
        :type wordsContainer: List[str]
        :type wordsQuery: List[str]
        :rtype: List[int]
        """

        trie = Trie(0, len(wordsContainer[0]))
        for index, s in enumerate(wordsContainer):
            trie.add(s, index)
        
        return [trie.find(s) for s in wordsQuery]
```
