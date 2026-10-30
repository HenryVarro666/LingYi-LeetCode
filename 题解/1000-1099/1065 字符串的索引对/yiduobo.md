---
title: "1065. 字符串的索引对"
aliases: ["yiduobo的每日leetcode 1065.字符串的索引对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608328865"
zhihu_id: "608328865"
zhihu_title: "yiduobo的每日leetcode 1065.字符串的索引对"
question_id: "1065"
question: "字符串的索引对"
problem_url: "https://leetcode.cn/problems/index-pairs-of-a-string/"
created: "2023-02-21T22:45:59+08:00"
updated: "2023-02-21T22:45:59+08:00"
upvotes: 0
comments: 0
---

# 1065. 字符串的索引对

> **[yiduobo的每日leetcode 1065.字符串的索引对](https://zhuanlan.zhihu.com/p/608328865) · 知乎 · 2023-02-21 · 赞同 0**
> 力扣：[1065. 字符串的索引对](https://leetcode.cn/problems/index-pairs-of-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1065.字符串的索引对

[力扣](https://leetcode.cn/problems/index-pairs-of-a-string/)

没有什么特别好的思路，不过好在本题的数据规模较小，使用暴力法完全是可行的。

我在这里先通过words建立起trie树，然后枚举text中的所有位置作为单词的起点start_pos，接下来通过trie树判断以start_pos为起点的所有子串是否出现在words中。为了能够高效进行判断，trie树中的节点除了常规的孩子数组外，还需要额外设置一个标记，用来表示当前节点是否为某个单词的结尾。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.childs = {}
        self.final = False

class Solution(object):
    def indexPairs(self, text, words):
        """
        :type text: str
        :type words: List[str]
        :rtype: List[List[int]]
        """

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char not in now.childs:
                    node = Node()
                    now.childs[char] = node
                now = now.childs[char]
            
            now.final = True

        res = []
        for start_pos in range(len(text)):
            now = root
            for index, char in enumerate(text[start_pos:]):
                if char not in now.childs:
                    break
                now = now.childs[char]
                if now.final:
                    res.append([start_pos, start_pos + index])
        
        return res
```
