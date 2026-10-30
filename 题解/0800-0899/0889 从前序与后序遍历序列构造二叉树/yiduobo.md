---
title: "889. 根据前序和后序遍历构造二叉树"
aliases: ["yiduobo的每日leetcode 889.根据前序和后序遍历构造二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/array", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351916718"
zhihu_id: "351916718"
zhihu_title: "yiduobo的每日leetcode 889.根据前序和后序遍历构造二叉树"
question_id: "889"
question: "从前序与后序遍历序列构造二叉树"
problem_url: "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-postorder-traversal/"
difficulty: "Medium"
rating: 1732
created: "2021-02-21T20:13:07+08:00"
updated: "2021-02-21T20:13:07+08:00"
upvotes: 0
comments: 0
---

# 889. 根据前序和后序遍历构造二叉树

> **[yiduobo的每日leetcode 889.根据前序和后序遍历构造二叉树](https://zhuanlan.zhihu.com/p/351916718) · 知乎 · 2021-02-21 · 赞同 0**
> 力扣：[889. 从前序与后序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-postorder-traversal/) · Medium · 灵茶山艾府：[【图解】从 O(n^2) 到 O(n)（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

889.根据前序和后序遍历构造二叉树

[力扣](https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/)

首先，仅根据前序和后序遍历可能无法唯一确定一颗二叉树，但是由于题目只要求给出一种可能的情况，那么可以按照某些规则构造出一种可能的情况。

前序遍历的顺序为根-左-右，而后序遍历则是左-右-根，那么对于当前子树而言，前序遍历pre中的pre[0]以及后续遍历post中的post[-1]显然为当前子树的根。我们可以认为pre[1]为当前子树根节点的左孩子，那么找到pre[1]在后续遍历post中的位置p，就可以确定从post[0]到post[p]这一段就是当前子树后序遍历中左子树的那一部分，那么剩下的除根节点之外就是右子树的那一部分，于是接下来就可以继续递归求解左右子树直到完成整棵树的构造。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def constructFromPrePost(self, pre, post):
        """
        :type pre: List[int]
        :type post: List[int]
        :rtype: TreeNode
        """

        pos_dict = {x : index for index, x in enumerate(post)}
        return self.build(0, len(pre) - 1, 0, len(post) - 1, pre, post, pos_dict)

    def build(self, pre_l, pre_r, post_l, post_r, pre, post, pos_dict):
        now = TreeNode(pre[pre_l])
        if pre_l < pre_r:       
            left_len = pos_dict[pre[pre_l + 1]] - post_l + 1
            if left_len > 0:
                now.left = self.build(pre_l + 1, pre_l + left_len, post_l, post_l + left_len - 1, pre, post, pos_dict)
            if pre_r - pre_l - left_len > 0:
                now.right = self.build(pre_l + left_len + 1, pre_r, post_l + left_len, post_r - 1, pre, post, pos_dict)
        return now
```
