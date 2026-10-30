---
title: "2185. 统计包含给定前缀的字符串"
aliases: ["yiduobo的每日leetcode 2185.统计包含给定前缀的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536559504"
zhihu_id: "536559504"
zhihu_title: "yiduobo的每日leetcode 2185.统计包含给定前缀的字符串"
question_id: "2185"
question: "统计包含给定前缀的字符串"
problem_url: "https://leetcode.cn/problems/counting-words-with-a-given-prefix/"
difficulty: "Easy"
created: "2022-07-02T01:02:39+08:00"
updated: "2022-07-02T01:02:39+08:00"
upvotes: 0
comments: 0
---

# 2185. 统计包含给定前缀的字符串

> **[yiduobo的每日leetcode 2185.统计包含给定前缀的字符串](https://zhuanlan.zhihu.com/p/536559504) · 知乎 · 2022-07-02 · 赞同 0**
> 力扣：[2185. 统计包含给定前缀的字符串](https://leetcode.cn/problems/counting-words-with-a-given-prefix/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2185.统计包含给定前缀的字符串

[力扣](https://leetcode.cn/problems/counting-words-with-a-given-prefix/)

由于题目饿得数据规模很小，因此直接使用暴力法也是可以的。我在这里使用的是trie树，在常规trie树的基础上给每个节点额外设置了一个权重，表示建树时经过这个节点的次数，这个次数实际上就是数组中包含该前缀的字符串数目。建树完成后，在trie数中查找pref，若找不到，那么答案为0，否则答案就是trie树中对应节点的权重。

最后附上python代码：

```python
class Node(object):
    def __init__(self):
        self.w = 1
        self.childs = {}

class Solution(object):
    def prefixCount(self, words, pref):
        """
        :type words: List[str]
        :type pref: str
        :rtype: int
        """

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char in now.childs:
                    now = now.childs[char]
                    now.w += 1
                else:
                    tmp = Node()
                    now.childs[char] = tmp
                    now = tmp

        now = root
        for char in pref:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.w
```
