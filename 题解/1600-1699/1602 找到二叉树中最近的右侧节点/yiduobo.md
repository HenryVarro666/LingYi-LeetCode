---
title: "1602. 找到二叉树中最近的右侧节点"
aliases: ["yiduobo的每日leetcode 1602.找到二叉树中最近的右侧节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618627015"
zhihu_id: "618627015"
zhihu_title: "yiduobo的每日leetcode 1602.找到二叉树中最近的右侧节点"
question_id: "1602"
question: "找到二叉树中最近的右侧节点"
problem_url: "https://leetcode.cn/problems/find-nearest-right-node-in-binary-tree/"
created: "2023-03-31T23:18:20+08:00"
updated: "2023-03-31T23:18:20+08:00"
upvotes: 1
comments: 0
---

# 1602. 找到二叉树中最近的右侧节点

> **[yiduobo的每日leetcode 1602.找到二叉树中最近的右侧节点](https://zhuanlan.zhihu.com/p/618627015) · 知乎 · 2023-03-31 · 赞同 1**
> 力扣：[1602. 找到二叉树中最近的右侧节点](https://leetcode.cn/problems/find-nearest-right-node-in-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1602.找到二叉树中最近的右侧节点

[力扣](https://leetcode.cn/problems/find-nearest-right-node-in-binary-tree/)

从根节点向下开始进行层序遍历，对于当前处理的这一层节点，若其中出现了u，那么返回u的下一个节点。若u是这一层的最后一个节点，那么就返回空。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findNearestRightNode(self, root, u):
        """
        :type root: TreeNode
        :type u: TreeNode
        :rtype: TreeNode
        """

        q = [root]
        head, tail = 0, 1
        while head < tail:
            for index in range(head, tail):
                if q[index] == u:
                    if index + 1 == tail:
                        return None
                    return q[index + 1]
                
                now = q[index]
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
```
