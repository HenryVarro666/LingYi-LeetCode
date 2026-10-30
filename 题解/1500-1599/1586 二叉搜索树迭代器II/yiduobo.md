---
title: "1586. 二叉搜索树迭代器II"
aliases: ["yiduobo的每日leetcode 1586.二叉搜索树迭代器II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618371279"
zhihu_id: "618371279"
zhihu_title: "yiduobo的每日leetcode 1586.二叉搜索树迭代器II"
question_id: "1586"
question: "二叉搜索树迭代器II"
problem_url: "https://leetcode.cn/problems/binary-search-tree-iterator-ii/"
created: "2023-03-31T02:11:37+08:00"
updated: "2023-03-31T02:11:37+08:00"
upvotes: 0
comments: 0
---

# 1586. 二叉搜索树迭代器II

> **[yiduobo的每日leetcode 1586.二叉搜索树迭代器II](https://zhuanlan.zhihu.com/p/618371279) · 知乎 · 2023-03-31 · 赞同 0**
> 力扣：[1586. 二叉搜索树迭代器II](https://leetcode.cn/problems/binary-search-tree-iterator-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1586.二叉搜索树迭代器II

[力扣](https://leetcode.cn/problems/binary-search-tree-iterator-ii/)

对于题目中的几种操作，由于prev操作总是发生在next操作之后，那么如果在执行next操作时顺便将遍历到的节点记录下来，对于prev操作就可以直接通过这个记录下来的数组得到了，于是问题就变成了如果不进行预先遍历，要如何找出树中每个节点的后继节点。

对于某个节点，其如果存在后继节点，需要满足下面三个条件之一：

1、该节点已经被记录过，且该节点不是记录数组的最后一个节点：

这种情况主要出现在prev操作之后的next操作，此时只需要找到记录数组中的下一个节点返回即可。

2、该节点存在右孩子：

此时该节点的后继节点就是其右孩子所在子树中的最左侧节点，因此需要从右孩子开始不断向左侧迭代直到到达叶子节点为止。

3、该节点不存在右孩子，但是其存在位于右侧的祖先节点：

此时该节点的后继节点就是位于其右侧的最深的祖先节点。对于这种情况，直接向上遍历的复杂度是比较高的，那么一个自然的想法就是在处理情况2时，将路径上经过的所有节点都储存在栈中。那么到了情况3，栈顶的节点就是要找的右侧且最深的祖先节点。

需要特别注意的是，这个祖先节点也可能存在右子树，那么接下来的后继节点就应该是这颗右子树中最左侧的节点，而不是更上层的祖先节点中，因此在这里需要还应该对这个祖先节点的右孩子执行情况2中对应的操作。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class BSTIterator(object):

    def __init__(self, root):
        """
        :type root: TreeNode
        """
        self.inorder = []
        self.stack = []
        self.p = 0
        self.add_left(root)

    def add_left(self, now):
        while now:
            self.stack.append(now)
            now = now.left

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.p < len(self.inorder) or len(self.stack) > 0

    def next(self):
        """
        :rtype: int
        """
        if self.p == len(self.inorder):
            self.inorder.append(self.stack[-1].val)
            node = self.stack.pop()
            self.add_left(node.right)

        res = self.inorder[self.p]
        self.p += 1
        
        return res

    def hasPrev(self):
        """
        :rtype: bool
        """
        return self.p > 1

    def prev(self):
        """
        :rtype: int
        """
        self.p -= 1
        return self.inorder[self.p - 1]

# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.hasNext()
# param_2 = obj.next()
# param_3 = obj.hasPrev()
# param_4 = obj.prev()
```
