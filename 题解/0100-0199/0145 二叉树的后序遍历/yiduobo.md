---
title: "145. 二叉树的后序遍历"
aliases: ["yiduobo的每日leetcode 145.二叉树的后序遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142669695"
zhihu_id: "142669695"
zhihu_title: "yiduobo的每日leetcode 145.二叉树的后序遍历"
question_id: "145"
question: "二叉树的后序遍历"
problem_url: "https://leetcode.cn/problems/binary-tree-postorder-traversal/"
created: "2020-05-21T22:48:53+08:00"
updated: "2020-05-21T22:48:53+08:00"
upvotes: 0
comments: 0
---

# 145. 二叉树的后序遍历

> **[yiduobo的每日leetcode 145.二叉树的后序遍历](https://zhuanlan.zhihu.com/p/142669695) · 知乎 · 2020-05-21 · 赞同 0**
> 力扣：[145. 二叉树的后序遍历](https://leetcode.cn/problems/binary-tree-postorder-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

145.二叉树的后序遍历<https://leetcode-cn.com/problems/binary-tree-postorder-traversal/>

这次轮到了后序遍历。与前序遍历和中序遍历不同，后续遍历需要先计算左子树和右子树，如果使用之前修改树结构的方式来做，需要搞清楚左子树和右子树中第一个遍历到的节点以及最后一个遍历到的节点，而因为树的结构不确定，且遍历方式是后序遍历，因此确定这两个节点的复杂度就太高了，所以在这里不适合用之前的方法来做。

但是，如果换一个思路，我们反过来看这个后序遍历，就会发现实际上后序遍历就是**将根-右-左这种遍历方式得到的结果反过来**。

于是，我们可以按之前的方法（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)）先完成根-右-左的遍历，然后将结果反过来输出即可。具体的说，就是我们每次找到当前节点右子树的最左侧节点，将其左孩子指向到当前节点的左孩子即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def postorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        if not root:
            return []

        res = []

        now = root
        while now:
            res.append(now.val)
            if now.right:
                leftest = now.right
                while leftest.left:
                    leftest = leftest.left
                leftest.left = now.left
                now = now.right
            else:
                now = now.left

        res.reverse()
        return res
```
