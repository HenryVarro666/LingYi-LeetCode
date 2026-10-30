---
title: "814. 二叉树剪枝"
aliases: ["yiduobo的每日leetcode 814.二叉树剪枝"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343826757"
zhihu_id: "343826757"
zhihu_title: "yiduobo的每日leetcode 814.二叉树剪枝"
question_id: "814"
question: "二叉树剪枝"
problem_url: "https://leetcode.cn/problems/binary-tree-pruning/"
created: "2021-01-14T22:57:11+08:00"
updated: "2021-01-14T22:57:11+08:00"
upvotes: 0
comments: 0
---

# 814. 二叉树剪枝

> **[yiduobo的每日leetcode 814.二叉树剪枝](https://zhuanlan.zhihu.com/p/343826757) · 知乎 · 2021-01-14 · 赞同 0**
> 力扣：[814. 二叉树剪枝](https://leetcode.cn/problems/binary-tree-pruning/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

814.二叉树剪枝

[力扣](https://leetcode-cn.com/problems/binary-tree-pruning/)

对于某棵子树来说，我们判断其是否包含值为1的节点，可以分为三个步骤：

1、判断其左子树中是否包含值为1的节点

2、判断其右子树中是否包含值为1的节点

3、判断当前子树的根节点的值是否为1

于是现在就有了一种做法：

对于一个子树，设当前的根节点为now，那么递归求解now.left以及now.right，同时使用left_flag和right_flag记录左右子树中是否含有值为1的节点。

若left_flag为false，那么置now.left为空。

若right_flag为false，那么置now.right为空。

最后若left_flag为true，或者right_flag为true，或者当前节点值为1，那么返回true，否则返回false。

从根节点root开始递归求解，若整棵树中都没有值为1的节点，那么返回空，否则返回root。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def pruneTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        if(self.remove(root)):
            return root
        return None
    
    def remove(self, now):
        if not now:
            return False
        
        left = self.remove(now.left)
        if not left:
            now.left = None
        
        right = self.remove(now.right)
        if not right:
            now.right = None
        
        if left or right or (now.val == 1):
            return True

        return False
```
