---
title: "105. 从前序与中序遍历序列构造二叉树"
aliases: ["yiduobo的每日leetcode 105.从前序与中序遍历序列构造二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/hash-table", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138001203"
zhihu_id: "138001203"
zhihu_title: "yiduobo的每日leetcode 105.从前序与中序遍历序列构造二叉树"
question_id: "105"
question: "从前序与中序遍历序列构造二叉树"
problem_url: "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/"
difficulty: "Medium"
created: "2020-05-03T23:23:15+08:00"
updated: "2020-05-03T23:23:15+08:00"
upvotes: 0
comments: 0
---

# 105. 从前序与中序遍历序列构造二叉树

> **[yiduobo的每日leetcode 105.从前序与中序遍历序列构造二叉树](https://zhuanlan.zhihu.com/p/138001203) · 知乎 · 2020-05-03 · 赞同 0**
> 力扣：[105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · Medium · 灵茶山艾府：[【图解】从 O(n^2) 到 O(n)（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

105.从前序与中序遍历序列构造二叉树<https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/>

经典的树操作的题目。

首先，前序遍历的第一个节点就是整棵树的根节点。

接下来，我们可以在中序遍历中找到根节点的位置，这个位置将中序遍历序列分成了两个部分，即左子树的中序遍历序列以及右子树的中序遍历序列。

接下来，通过计算左子树中序遍历序列的长度，可以得知左子树中节点的数量，而前序遍历中从第一个节点往后数即为左子树的前序遍历序列，而剩下的部分则是右子树的前序遍历序列。

至此，我们已经确定了整棵树的根节点，左子树的前序与中序遍历序列，还有右子树的前序与中序遍历序列，接下来按同样的方式递归求解左子树与右子树即可。

例如样例中的前序遍历[3,9,20,15,7]， 中序遍历[9,3,15,20,7]：

1、首先确定根节点为3，找到3在中序遍历中的位置，那么左子树的中序遍历为[9]，右子树的中序遍历为[15, 20, 7]。

2、左子树的中序遍历长度为1，那么左子树的前序遍历则是3往后推一位，即为[9]。剩下的[20, 15, 7]即为右子树的前序遍历。

3、接下来递归求解左子树与右子树即可。

需要注意的是，由于这里保证了树中没有相同的元素，因此可以将前序遍历与中序遍历明确地进行一一对应，才能保证上面这种方法的正确性。

我在这里的实现是按根，左子树，右子树这个顺序来做的，实际上就相当于对树进行了前序遍历，因此可以在处理的过程中维护一个root_pos，表示当前子树的根节点在前序遍历中的位置。每次递归进入左子树时加1，而进入右子树时则需要往后移动左子树节点数量的长度。

这样做的好处是递归时只需要维护当前树在中序遍历序列中的左右边界以及这个root_pos，而不需要对前序遍历或是中序遍历进行切分，提高了计算的效率。

最后附上python代码，其中build方法的left和right分别表示当前树在中序遍历序列中的左右边界，pos_dict则是用来查询根节点在中序遍历中的位置：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: TreeNode
        """

        if not preorder:
            return None

        pos_dict = {}
        for index, val in enumerate(inorder):
            pos_dict[val] = index

        return self.build(0, len(inorder), preorder, inorder, 0, pos_dict)

    def build(self, left, right, preorder, inorder, root_pos, pos_dict):
        if left == right:
            return None

        root_val = preorder[root_pos]
        inorder_pos = pos_dict[root_val]
        root = TreeNode(root_val)
        if inorder_pos > left:
            root.left = self.build(left, inorder_pos, preorder, inorder, root_pos + 1, pos_dict)
        if inorder_pos < right:
            root.right = self.build(inorder_pos + 1, right, preorder, inorder, root_pos + inorder_pos - left + 1, pos_dict)
        return root
```
