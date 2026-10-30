---
title: "1506. 找到N叉树的根节点"
aliases: ["yiduobo的每日leetcode 1506.找到N叉树的根节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617041964"
zhihu_id: "617041964"
zhihu_title: "yiduobo的每日leetcode 1506.找到N叉树的根节点"
question_id: "1506"
question: "找到N叉树的根节点"
problem_url: "https://leetcode.cn/problems/find-root-of-n-ary-tree/"
created: "2023-03-26T00:06:35+08:00"
updated: "2023-03-26T00:06:35+08:00"
upvotes: 0
comments: 0
---

# 1506. 找到N叉树的根节点

> **[yiduobo的每日leetcode 1506.找到N叉树的根节点](https://zhuanlan.zhihu.com/p/617041964) · 知乎 · 2023-03-26 · 赞同 0**
> 力扣：[1506. 找到N叉树的根节点](https://leetcode.cn/problems/find-root-of-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1506.找到N叉树的根节点

[力扣](https://leetcode.cn/problems/find-root-of-n-ary-tree/)

除了根节点之外，树中其他节点都是某个节点的孩子节点，换言之，如果将树中所有节点以及其所有孩子节点全部收集起来，问题就转化成了给出一个数组，其中有一种数字只出现了一次，其他所有数都出现了两次，问这种数字是什么。

对于这个问题，只需将所有数都异或起来，得到的就是这种数字。通过数字反差树中的节点就可以找出根节点了。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
"""

class Solution(object):
    def findRoot(self, tree):
        """
        :type tree: List['Node']
        :rtype: 'Node'
        """

        fa_xor = child_xor = 0

        for node in tree:
            fa_xor ^= node.val
            for child in node.children:
                child_xor ^= child.val
        
        fa_val = fa_xor ^ child_xor
        for node in tree:
            if node.val == fa_val:
                return node
```
