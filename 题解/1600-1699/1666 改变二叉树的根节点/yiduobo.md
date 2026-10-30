---
title: "1666. 改变二叉树的根节点"
aliases: ["yiduobo的每日leetcode 1666.改变二叉树的根节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619471114"
zhihu_id: "619471114"
zhihu_title: "yiduobo的每日leetcode 1666.改变二叉树的根节点"
question_id: "1666"
question: "改变二叉树的根节点"
problem_url: "https://leetcode.cn/problems/change-the-root-of-a-binary-tree/"
created: "2023-04-04T19:30:31+08:00"
updated: "2023-04-04T19:30:31+08:00"
upvotes: 0
comments: 0
---

# 1666. 改变二叉树的根节点

> **[yiduobo的每日leetcode 1666.改变二叉树的根节点](https://zhuanlan.zhihu.com/p/619471114) · 知乎 · 2023-04-04 · 赞同 0**
> 力扣：[1666. 改变二叉树的根节点](https://leetcode.cn/problems/change-the-root-of-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1666.改变二叉树的根节点

[力扣](https://leetcode.cn/problems/change-the-root-of-a-binary-tree/)

题目已经给出了详细的变换规则，同时给出的节点数据结构中也包含了parent字段，因此可以从leaf开始，不断执行移动操作，然后向上迭代直到来到根节点为止。

在迭代过程中需要特别注意的是，题目中的移动同样也需要修改节点的parent指针，因此需要使用一个额外的变量储存待处理节点now的原始父亲节点，然后才能修改now的父亲节点。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
"""

class Solution(object):
    def flipBinaryTree(self, root, leaf):
        """
        :type node: Node
        :rtype: Node
        """

        now = leaf
        prev_fa = now.parent
        while prev_fa:
            if now.left:
                now.right = now.left
                now.left = None
            
            fa = prev_fa

            if fa.left == now:
                fa.left = None
            else:
                fa.right = None
            
            now.left = fa
            prev_fa = fa.parent
            fa.parent = now
            now = fa
        
        leaf.parent = None
        return leaf
```
