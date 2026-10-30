---
title: "94. 二叉树的中序遍历"
aliases: ["yiduobo的每日leetcode 94.二叉树的中序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/graph", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137080593"
zhihu_id: "137080593"
zhihu_title: "yiduobo的每日leetcode 94.二叉树的中序遍历"
question_id: "94"
question: "二叉树的中序遍历"
problem_url: "https://leetcode.cn/problems/binary-tree-inorder-traversal/"
difficulty: "Easy"
created: "2020-04-28T22:59:31+08:00"
updated: "2020-04-28T22:59:31+08:00"
upvotes: 1
comments: 0
---

# 94. 二叉树的中序遍历

> **[yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593) · 知乎 · 2020-04-28 · 赞同 1**
> 力扣：[94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/) · Easy · 灵茶山艾府：[【图解】Morris 遍历（线索二叉树），一图秒懂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

94.二叉树的中序遍历<https://leetcode-cn.com/problems/binary-tree-inorder-traversal/>

经典的树操作的题目。递归的做法很简单，非递归的做法倒是挺有意思的。

首先明确一点，中序遍历的顺序是左-根-右。

在递归的做法中，首先需要遍历当前节点的左子树，然后回溯到当前节点，接下来在遍历当前节点的右子树。于是，问题就变成了如何在不回溯的情况下遍历完当前节点左子树之后返回到当前节点。

一个可行的想法是先找到**当前节点now的左子树中最右侧的节点rightest**，这个节点一定是左子树中最后被遍历到的，且该节点一定没有右孩子。于是我们可以将rightest的右孩子指向当前节点now，这样一来我们在遍历完now的左子树之后，自然就会从rightest返回到now了。需要注意的一点是，为了避免死循环，在完成rightest右孩子指向now之后，需要记得断开now与左子树的联系。

于是现在的做法是：

1、对于当前节点now，如果其左孩子不为空，那么找到其左子树中的最右节点rightest，将rightest的右孩子指向now，然后开始遍历now的左子树，同时断开now与左子树的连接。

2、如果其左孩子为空，那么记录下now的值之后遍历now的右子树即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def inorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        res = []
        now = root
        while now:
            if now.left is None:
                res.append(now.val)
                now = now.right
            else:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                now = now.left
                rightest.right.left = None

        return res
```
