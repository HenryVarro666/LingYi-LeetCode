---
title: "701. 二叉搜索树中的插入操作"
aliases: ["yiduobo的每日leetcode 701.二叉搜索树中的插入操作"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/317672005"
zhihu_id: "317672005"
zhihu_title: "yiduobo的每日leetcode 701.二叉搜索树中的插入操作"
question_id: "701"
question: "二叉搜索树中的插入操作"
problem_url: "https://leetcode.cn/problems/insert-into-a-binary-search-tree/"
created: "2020-11-28T15:30:34+08:00"
updated: "2020-11-28T15:30:34+08:00"
upvotes: 2
comments: 0
---

# 701. 二叉搜索树中的插入操作

> **[yiduobo的每日leetcode 701.二叉搜索树中的插入操作](https://zhuanlan.zhihu.com/p/317672005) · 知乎 · 2020-11-28 · 赞同 2**
> 力扣：[701. 二叉搜索树中的插入操作](https://leetcode.cn/problems/insert-into-a-binary-search-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

701.二叉搜索树中的插入操作

[力扣](https://leetcode-cn.com/problems/insert-into-a-binary-search-tree/)

题目保证了要插入的值与树中节点的值不同，那么依然是从根节点开始向下：

1、若now.val小于val，说明我们需要将val插入到now的右侧。若此时now.right为空，那么now.right \= Node(val)，否则继续考察now.right.val与val的关系。

2、若now.val大于val，说明我们需要将val插入到now的左侧。若此时now.left为空，那么now.left \= Node(val)，否则继续考察now.left.val与val的关系。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def insertIntoBST(self, root, val):
        """
        :type root: TreeNode
        :type val: int
        :rtype: TreeNode
        """

        if not root:
            return TreeNode(val)

        now = root
        while True:
            if now.val < val:
                if now.right:
                    now = now.right
                else:
                    now.right = TreeNode(val)
                    break
            else:
                if now.left:
                    now = now.left
                else:
                    now.left = TreeNode(val)
                    break
        
        return root
```
