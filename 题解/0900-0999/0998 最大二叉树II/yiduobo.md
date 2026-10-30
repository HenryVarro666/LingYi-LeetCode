---
title: "998. 最大二叉树II"
aliases: ["yiduobo的每日leetcode 998.最大二叉树II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365669652"
zhihu_id: "365669652"
zhihu_title: "yiduobo的每日leetcode 998.最大二叉树II"
question_id: "998"
question: "最大二叉树II"
problem_url: "https://leetcode.cn/problems/maximum-binary-tree-ii/"
created: "2021-04-17T20:46:00+08:00"
updated: "2021-04-17T20:46:00+08:00"
upvotes: 0
comments: 0
---

# 998. 最大二叉树II

> **[yiduobo的每日leetcode 998.最大二叉树II](https://zhuanlan.zhihu.com/p/365669652) · 知乎 · 2021-04-17 · 赞同 0**
> 力扣：[998. 最大二叉树II](https://leetcode.cn/problems/maximum-binary-tree-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

998.最大二叉树II

[力扣](https://leetcode-cn.com/problems/maximum-binary-tree-ii/)

首先判断特殊情况。当val大于root.val时，说明此时val是B中的最大值，因此应该构造值为val的节点node作为新的根节点，同时递归复制树root作为node的左子树。

接下来考察val小于root.val的情况。设当前处理到节点now：

1、这里有大前提now.val > val，因此复制now，得到节点ret作为当前子树的根节点。

2、now.val将当前的B分割成两个部分，其中左侧的部分与A中完全一致，因此可以直接递归复制以now.left为根的子树作为ret的左子树。

3、对于now.val分割出来的右侧部分，为A的右侧部分加上val，实际上就是原始问题的一个子问题，只不过变成了以now.right为根节点的子树以及val。

依然是先判断val是否大于now.right.val，若大于，那么就构造值为val的节点node，这里的node就是ret新的右孩子，同时还需要递归复制now.right作为node的左子树。若小于，那么递归求解now.right以及val即可。

另外还需要注意边界情况，当now.val分割出来的右侧部分为空时，那么此时只需新建值为val的节点node，然后置node为ret的右孩子即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def insertIntoMaxTree(self, root, val):
        """
        :type root: TreeNode
        :type val: int
        :rtype: TreeNode
        """

        if val > root.val:
            res = TreeNode(val)
            res.left = self.dfs(root, 0)
        else:
            res = self.dfs(root, val)
        
        return res
    
    def dfs(self, now, val):
        ret = TreeNode(now.val)
        if now.left:
            ret.left = self.dfs(now.left, 0)
        if now.right:
            if now.right.val < val:
                ret.right = TreeNode(val)
                ret.right.left = self.dfs(now.right, 0)
            else:
                ret.right = self.dfs(now.right, val)
        elif val > 0:
            ret.right = TreeNode(val)
        
        return ret
```
