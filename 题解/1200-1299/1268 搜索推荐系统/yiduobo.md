---
title: "1268. 搜索推荐系统"
aliases: ["yiduobo的每日leetcode 1268.搜索推荐系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387605959"
zhihu_id: "387605959"
zhihu_title: "yiduobo的每日leetcode 1268.搜索推荐系统"
question_id: "1268"
question: "搜索推荐系统"
problem_url: "https://leetcode.cn/problems/search-suggestions-system/"
created: "2021-07-07T22:06:44+08:00"
updated: "2021-07-07T22:06:44+08:00"
upvotes: 0
comments: 0
---

# 1268. 搜索推荐系统

> **[yiduobo的每日leetcode 1268.搜索推荐系统](https://zhuanlan.zhihu.com/p/387605959) · 知乎 · 2021-07-07 · 赞同 0**
> 力扣：[1268. 搜索推荐系统](https://leetcode.cn/problems/search-suggestions-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1268.搜索推荐系统

[力扣](https://leetcode-cn.com/problems/search-suggestions-system/)

题目要求给出与searchWord每一个前缀最接近且字典序最小的三个单词，那么对于字符串前缀相关的问题，很自然想到使用trie树来解决。

按正常做法构造trie树，不过在构造时需要对每个节点额外储存一个信息，即到当前节点的所有单词中字典序最小的三个。

接下来遍历searchWord中的字母并在trie树中行走，每走到一个节点，该节点所储存的三个单词就是当前前缀对应的答案。若无法继续行走，那么就直接使用空list填充答案然后返回答案即可。

最后附上python代码：

```python
class Trie(object):
    def __init__(self):
        self.end_flag = False
        self.next_dict = {}
        self.candidate = [None] * 3

class Solution(object):
    def suggestedProducts(self, products, searchWord):
        """
        :type products: List[str]
        :type searchWord: str
        :rtype: List[List[str]]
        """

        root = Trie()
        for index, word in enumerate(products):
            now = root
            for char in word:
                if char not in now.next_dict:
                    tmp = Trie()
                    now.next_dict[char] = tmp
                
                now = now.next_dict[char]
                if now.candidate[0] is None or word < products[now.candidate[0]]:
                    now.candidate[2] = now.candidate[1]
                    now.candidate[1] = now.candidate[0]
                    now.candidate[0] = index
                elif now.candidate[1] is None or word < products[now.candidate[1]]:
                    now.candidate[2] = now.candidate[1]
                    now.candidate[1] = index
                elif now.candidate[2] is None or word < products[now.candidate[2]]:
                    now.candidate[2] = index
            
            now.end_flag = True
        
        res = []
        now = root
        for char in searchWord:
            if char not in now.next_dict:
                while len(res) < len(searchWord):
                    res.append([])
                return res
            now = now.next_dict[char]
            res.append([])
            for index in range(3):
                if now.candidate[index] is not None:
                    res[-1].append(products[now.candidate[index]])
        
        return res
```
