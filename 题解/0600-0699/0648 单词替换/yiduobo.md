---
title: "648. 单词替换"
aliases: ["yiduobo的每日leetcode 648.单词替换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/276551001"
zhihu_id: "276551001"
zhihu_title: "yiduobo的每日leetcode 648.单词替换"
question_id: "648"
question: "单词替换"
problem_url: "https://leetcode.cn/problems/replace-words/"
created: "2020-11-06T23:11:28+08:00"
updated: "2020-11-06T23:11:28+08:00"
upvotes: 0
comments: 0
---

# 648. 单词替换

> **[yiduobo的每日leetcode 648.单词替换](https://zhuanlan.zhihu.com/p/276551001) · 知乎 · 2020-11-06 · 赞同 0**
> 力扣：[648. 单词替换](https://leetcode.cn/problems/replace-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

648.单词替换

[力扣](https://leetcode-cn.com/problems/replace-words/)

题目要求对于sentence中的每个单词，检查其是否有前缀在字典里出现过。若有，找到最短的那个前缀。

看到前缀和字典，很自然就想到了使用trie树来解决。我们先通过字典建立起一棵trie树，然后对于sentence中的每个单词，枚举其前缀并在trie树中行走，直到命中某个单词或者无法继续往下走为止。

这里有个小优化是在建立trie树时，先按单词的长度进行排序。接下来在建树时，如果当前字母已经有了结束标记，说明当前单词的前缀恰好就是之前的某个单词，没必要再继续处理当前的单词了。

```python
class Node(object):

    def __init__(self):
        self.end_flag = False
        self.next_dict = {}

class Solution(object):
    def replaceWords(self, dictionary, sentence):
        """
        :type dictionary: List[str]
        :type sentence: str
        :rtype: str
        """

        trie = Node()
        for word in sorted(dictionary, key=lambda d:len(d)):
            now = trie
            for char in word:
                if char not in now.next_dict:
                    tmp = Node()
                    now.next_dict[char] = tmp
                
                now = now.next_dict[char]
                if now.end_flag:
                    break
            
            now.end_flag = True

        res = []
        for word in split(sentence, ' '):
            now = trie
            flag = False
            for index, char in enumerate(word):
                if char not in now.next_dict:
                    break
                now = now.next_dict[char]
                if now.end_flag:
                    res.append(word[:index + 1])
                    flag = True
                    break
            
            if not flag:
                res.append(word)

        return ' '.join(res)
```
