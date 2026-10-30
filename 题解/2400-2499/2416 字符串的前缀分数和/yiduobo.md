---
title: "2416. 字符串的前缀分数和"
aliases: ["yiduobo的每日leetcode 2416.字符串的前缀分数和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/trie", "leetcode/hash-table", "leetcode/string", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569537316"
zhihu_id: "569537316"
zhihu_title: "yiduobo的每日leetcode 2416.字符串的前缀分数和"
question_id: "2416"
question: "字符串的前缀分数和"
problem_url: "https://leetcode.cn/problems/sum-of-prefix-scores-of-strings/"
difficulty: "Hard"
rating: 1725
created: "2022-09-30T01:16:24+08:00"
updated: "2022-09-30T01:16:24+08:00"
upvotes: 0
comments: 0
---

# 2416. 字符串的前缀分数和

> **[yiduobo的每日leetcode 2416.字符串的前缀分数和](https://zhuanlan.zhihu.com/p/569537316) · 知乎 · 2022-09-30 · 赞同 0**
> 力扣：[2416. 字符串的前缀分数和](https://leetcode.cn/problems/sum-of-prefix-scores-of-strings/) · Hard · 灵茶山艾府：[字典树：两次遍历 / DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2416.字符串的前缀分数和

[力扣](https://leetcode.cn/problems/sum-of-prefix-scores-of-strings/)

题目要求计算每个字符串的每种前缀在所有字符串中出现的次数，既然涉及到了所有前缀，那么很自然想到使用trie树来解决。

首先遍历每个字符串，将这些字符串加入到到trie树中。在常规trie树的基础上，还需要记录下每个前缀出现的次数。接下来再遍历一次字符串，通过trie树计算当前字符串的所有前缀出现了多少次，累加后更新答案即可。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.weight = 0
        self.childs = {}

class Solution(object):
    def sumPrefixScores(self, words):
        """
        :type words: List[str]
        :rtype: List[int]
        """

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char not in now.childs:
                    now.childs[char] = Node()
                now = now.childs[char]
                now.weight += 1
        
        res = []
        for word in words:
            now = root
            res.append(0)
            for char in word:
                now = now.childs[char]
                res[-1] += now.weight
        
        return res
```
