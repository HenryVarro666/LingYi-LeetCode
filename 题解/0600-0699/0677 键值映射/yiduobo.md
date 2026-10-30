---
title: "677. 键值映射"
aliases: ["yiduobo的每日leetcode 677.键值映射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/300085629"
zhihu_id: "300085629"
zhihu_title: "yiduobo的每日leetcode 677.键值映射"
question_id: "677"
question: "键值映射"
problem_url: "https://leetcode.cn/problems/map-sum-pairs/"
created: "2020-11-18T22:59:03+08:00"
updated: "2020-11-18T22:59:03+08:00"
upvotes: 0
comments: 0
---

# 677. 键值映射

> **[yiduobo的每日leetcode 677.键值映射](https://zhuanlan.zhihu.com/p/300085629) · 知乎 · 2020-11-18 · 赞同 0**
> 力扣：[677. 键值映射](https://leetcode.cn/problems/map-sum-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

677.键值映射

[力扣](https://leetcode-cn.com/problems/map-sum-pairs/)

题目需要我们维护某种数据结构，可以很快得到词表中以某个前缀开头的所有词语的权重之和，看到词表和前缀很自然就想到了使用trie树来做。除了普通的树结构之外，对于每个节点我们额外维护从根节点到当前节点这一前缀的所有词的前缀之和。

对于插入操作，若要插入的词没有在词表中，我们从根节点开始往下走，对于途经的所有节点都加上该词的权重；若其已经出现在词表中，那么我们计算这个词要新插入的权重与之前插入的权重的差值，然后从根节点往下走，对于途经的所有节点都加上该差值。

对于查询操作，则从根节点往下走到对应节点，返回该节点的权重即可。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self):
        self.next_char = {}
        self.sum = 0

class MapSum(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.trie = TreeNode()
        self.key_dict = {}

    def insert(self, key, val):
        """
        :type key: str
        :type val: int
        :rtype: None
        """
        now = self.trie
        if key in self.key_dict:
            delta = val - self.key_dict[key]
        else:
            delta = val
        self.key_dict[key] = val

        for char in key:
            if char not in now.next_char:
                tmp = TreeNode()
                now.next_char[char] = tmp
            
            now = now.next_char[char]
            now.sum += delta

    def sum(self, prefix):
        """
        :type prefix: str
        :rtype: int
        """
        now = self.trie
        for char in prefix:
            if char not in now.next_char:
                return 0
            now = now.next_char[char]
        
        return now.sum

# Your MapSum object will be instantiated and called as such:
# obj = MapSum()
# obj.insert(key,val)
# param_2 = obj.sum(prefix)
```
