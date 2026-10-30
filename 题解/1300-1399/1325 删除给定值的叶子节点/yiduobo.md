---
title: "1325. 删除给定值的叶子节点"
aliases: ["yiduobo的每日leetcode 1325.删除给定值的叶子节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394119340"
zhihu_id: "394119340"
zhihu_title: "yiduobo的每日leetcode 1325.删除给定值的叶子节点"
question_id: "1325"
question: "删除给定值的叶子节点"
problem_url: "https://leetcode.cn/problems/delete-leaves-with-a-given-value/"
created: "2021-07-28T23:00:28+08:00"
updated: "2021-07-28T23:00:28+08:00"
upvotes: 0
comments: 1
---

# 1325. 删除给定值的叶子节点

> **[yiduobo的每日leetcode 1325.删除给定值的叶子节点](https://zhuanlan.zhihu.com/p/394119340) · 知乎 · 2021-07-28 · 赞同 0**
> 力扣：[1325. 删除给定值的叶子节点](https://leetcode.cn/problems/delete-leaves-with-a-given-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1325.删除给定值的叶子节点

[力扣](https://leetcode-cn.com/problems/delete-leaves-with-a-given-value/)

题目要求删除的是叶子节点，同时当某个节点被删除后，其父亲节点可能成为新的叶子节点从而成为下一个删除目标。

树中的删除操作有一个特点，就是若我们需要删除节点now，实际上我们需要执行的操作是将now的父亲节点在now的这一侧断开连接，于是我们需要先设置一个假根节点p_head，并将root设置为p_head的孩子节点，然后从p_head节点开始向下进行dfs。

对于当前节点now，若now有左右孩子，我们先递归处理其左右孩子，并根据递归处理的结果决定是否断开对应的连接。处理完之后，若当前节点左右孩子为空，且节点值等于target，那么说明now也应该被删去，那么我们就将这一信息返回到上一层。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def removeLeafNodes(self, root, target):
        """
        :type root: TreeNode
        :type target: int
        :rtype: TreeNode
        """

        p_root = TreeNode(0)
        p_root.left = root
        self.dfs(p_root, target)
    
        return p_root.left

    def dfs(self, now, target):
        if now.left is not None and self.dfs(now.left, target):
            now.left = None

        if now.right is not None and self.dfs(now.right, target):
            now.right = None

        return now.left is None and now.right is None and now.val == target
```
