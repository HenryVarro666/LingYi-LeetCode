---
title: "919. 完全二叉树插入器"
aliases: ["yiduobo的每日leetcode 919.完全二叉树插入器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355596604"
zhihu_id: "355596604"
zhihu_title: "yiduobo的每日leetcode 919.完全二叉树插入器"
question_id: "919"
question: "完全二叉树插入器"
problem_url: "https://leetcode.cn/problems/complete-binary-tree-inserter/"
created: "2021-03-08T23:23:04+08:00"
updated: "2021-03-08T23:23:04+08:00"
upvotes: 0
comments: 0
---

# 919. 完全二叉树插入器

> **[yiduobo的每日leetcode 919.完全二叉树插入器](https://zhuanlan.zhihu.com/p/355596604) · 知乎 · 2021-03-08 · 赞同 0**
> 力扣：[919. 完全二叉树插入器](https://leetcode.cn/problems/complete-binary-tree-inserter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

919.完全二叉树插入器

[力扣](https://leetcode-cn.com/problems/complete-binary-tree-inserter/)

由于最后一层的所有节点只与倒数第二层有关，同时插入的顺序是严格从左至右的，因此我们可以使用类似层次遍历的做法，使用一个队列储存bfs倒数第二轮以及最后一轮的节点。bfs完成后，倒数第二层最左侧且不同时拥有左右孩子的节点就是下一个插入节点的父亲节点，而下一个插入节点则应该插入到最后一轮的节点队列当中。

对于初始化操作，我们可以从根节点开始进行bfs，将节点逐层加入到队列中，同时保留住倒数第二层以及最后一层的队列作为备用。bfs过程中注意记录倒数第二层使用到了哪个节点。

对于插入操作，设插入的节点为node：

1、若倒数第二层中的节点还未用完，那么选择当前层最左侧未被使用的节点now：

1-1)若now没有左孩子，则将node置为now的左孩子

1-2)若now有左孩子，则将node置为now的右孩子，同时将now指向倒数第二层的下一个节点

1-3)除此之外还需要将node加入到最后一层的队列末尾

2、若倒数第二层中的节点已经用完，那么就将最后一层作为新的倒数第二层，并将now指向第一个节点，然后回到步骤1进行插入操作

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class CBTInserter(object):

    def __init__(self, root):
        """
        :type root: TreeNode
        """
        self.now_q = [root]
        self.child_q = []
        self.root = root
        self.l = 0
        self.r = 1
        while True:
            for now in self.now_q[self.l : self.r]:
                if now.left:
                    self.child_q.append(now.left)
                    if now.right:
                        self.child_q.append(now.right)
                        self.l += 1
            if self.l == self.r:
                self.now_q = self.child_q[:]
                self.child_q = []
                self.l = 0
                self.r = len(self.now_q)
            else:
                break

    def insert(self, v):
        """
        :type v: int
        :rtype: int
        """
        node = TreeNode(v)
        self.child_q.append(node)
        now = self.now_q[self.l]
        if now.left:
            now.right = node
            self.l += 1
            if self.l == self.r:
                self.now_q = self.child_q[:]
                self.child_q = []
                self.l = 0
                self.r = len(self.now_q)
        else:
            now.left = node
        
        return now.val

    def get_root(self):
        """
        :rtype: TreeNode
        """
        return self.root

# Your CBTInserter object will be instantiated and called as such:
# obj = CBTInserter(root)
# param_1 = obj.insert(v)
# param_2 = obj.get_root()
```
