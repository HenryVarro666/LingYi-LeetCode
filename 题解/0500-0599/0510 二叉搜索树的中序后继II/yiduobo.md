---
title: "510. 二叉搜索树的中序后继II"
aliases: ["yiduobo的每日leetcode 510.二叉搜索树的中序后继II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600542653"
zhihu_id: "600542653"
zhihu_title: "yiduobo的每日leetcode 510.二叉搜索树的中序后继II"
question_id: "510"
question: "二叉搜索树的中序后继II"
problem_url: "https://leetcode.cn/problems/inorder-successor-in-bst-ii/"
created: "2023-01-23T00:28:16+08:00"
updated: "2023-01-23T00:28:16+08:00"
upvotes: 0
comments: 0
---

# 510. 二叉搜索树的中序后继II

> **[yiduobo的每日leetcode 510.二叉搜索树的中序后继II](https://zhuanlan.zhihu.com/p/600542653) · 知乎 · 2023-01-23 · 赞同 0**
> 力扣：[510. 二叉搜索树的中序后继II](https://leetcode.cn/problems/inorder-successor-in-bst-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

510.二叉搜索树的中序后继II

[力扣](https://leetcode.cn/problems/inorder-successor-in-bst-ii/)

对于bst中的某个节点node，其中序后继有三种可能性：

1、node没有中序后继

2、node的中序后继位于其右子树中

3、node的中序后继是node的某个祖先节点

对于情况1，node就是bst中值最大的节点，换言之node并没有右子树，同时其所有的祖先节点的值都小于node的值。

对于情况2和情况3，若node存在某个值大于node的祖先节点anc，同时node也有右子树，那么右子树中所有节点的值都必然小于anc的值。理由是只有当node位于anc的左子树中时，node的值才可能小于anc的值。若node位于anc的左子树中，那么node右子树中的所有节点也同样位于anc的左子树中，因此node右子树中的所有节点值都小于anc的值。

根据上面两个结论，就可以确定求解的顺序：

1、若node存在右子树，那么答案就是node右子树中最左侧的节点

2、若node不存在右子树，那么就从node开始不停向上行走，直到遇到某个值大于node的祖先节点为止，而这个节点就是最终答案。一个简单的证明是不妨设p是从node向上行走的路径中第一个值大于node的节点，那么对于p的任意祖先节点q而言，若q的值小于p的值，说明p位于q的右子树中，那么node作为p的子孙结点，同样也位于q的右子树中，从而可知node的值将大于q的值，q不会是最终答案。反过来，若q的值大于p的值，那么由于p的存在，那么q也不是最终答案。

3、若上面两种操作都找不到答案，说明node没有中序后继，直接返回空

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
    def inorderSuccessor(self, node):
        """
        :type node: Node
        :rtype: Node
        """

        if node.right:
            now = node.right
            while now.left:
                now = now.left
            return now
        
        while node.parent:
            if node.parent.val > node.val:
                return node.parent
            node = node.parent

        return None
```
