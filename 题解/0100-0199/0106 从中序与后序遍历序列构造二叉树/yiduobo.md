---
title: "106. 从中序与后序遍历序列构造二叉树"
aliases: ["yiduobo的每日leetcode 106.从中序与后序遍历序列构造二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/hash-table", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138147539"
zhihu_id: "138147539"
zhihu_title: "yiduobo的每日leetcode 106.从中序与后序遍历序列构造二叉树"
question_id: "106"
question: "从中序与后序遍历序列构造二叉树"
problem_url: "https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/"
difficulty: "Medium"
created: "2020-05-04T21:13:09+08:00"
updated: "2020-05-04T21:13:09+08:00"
upvotes: 0
comments: 0
---

# 106. 从中序与后序遍历序列构造二叉树

> **[yiduobo的每日leetcode 106.从中序与后序遍历序列构造二叉树](https://zhuanlan.zhihu.com/p/138147539) · 知乎 · 2020-05-04 · 赞同 0**
> 力扣：[106. 从中序与后序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) · Medium · 灵茶山艾府：[【图解】从 O(n^2) 到 O(n)（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

106.从中序与后序遍历序列构造二叉树<https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/>

与上一题的做法基本相同（传送门在这里[yiduobo：yiduobo的每日leetcode 105.从前序与中序遍历序列构造二叉树](https://zhuanlan.zhihu.com/p/138001203)）。

前序遍历的顺序为根-左-右，而后序遍历则是左-右-根，因此前序遍历的第一个节点为根节点，而后续遍历的最后一个节点为根节点。

找到根节点后，通过中序遍历得到左右子树节点的数目，然后在前序/后序遍历中划分出左右子树，递归求解即可。

最后附上python代码，这里同样是使用了上一题root_pos的写法来提升效率：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def buildTree(self, inorder, postorder):
        """
        :type inorder: List[int]
        :type postorder: List[int]
        :rtype: TreeNode
        """

        if not inorder:
            return None

        pos_dict = {}
        for index, val in enumerate(inorder):
            pos_dict[val] = index

        return self.build(0, len(inorder), inorder, postorder, len(inorder) - 1, pos_dict)

    def build(self, left, right, inorder, postorder, root_pos, pos_dict):
        if left == right:
            return None

        root_val = postorder[root_pos]
        inorder_pos = pos_dict[root_val]
        root = TreeNode(root_val)

        if inorder_pos < right - 1:
            root.right = self.build(inorder_pos + 1, right, inorder, postorder, root_pos - 1, pos_dict)
        if inorder_pos > left:
            root.left = self.build(left, inorder_pos, inorder, postorder, root_pos - (right - 1 - inorder_pos) - 1, pos_dict)
        return root
```
