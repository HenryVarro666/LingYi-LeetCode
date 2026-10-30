---
title: "563. 二叉树的坡度"
aliases: ["yiduobo的每日leetcode 563.二叉树的坡度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266051780"
zhihu_id: "266051780"
zhihu_title: "yiduobo的每日leetcode 563.二叉树的坡度"
question_id: "563"
question: "二叉树的坡度"
problem_url: "https://leetcode.cn/problems/binary-tree-tilt/"
created: "2020-10-15T22:01:48+08:00"
updated: "2020-10-15T22:01:48+08:00"
upvotes: 0
comments: 0
---

# 563. 二叉树的坡度

> **[yiduobo的每日leetcode 563.二叉树的坡度](https://zhuanlan.zhihu.com/p/266051780) · 知乎 · 2020-10-15 · 赞同 0**
> 力扣：[563. 二叉树的坡度](https://leetcode.cn/problems/binary-tree-tilt/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

563.二叉树的坡度<https://leetcode-cn.com/problems/binary-tree-tilt/>

对于以节点p为根节点的子树而言，其坡度等于以p.left为根节点的子树的坡度，加上以p.right为根节点的子树的坡度，再加上两颗子树节点之后的差的绝对值，那么就可以优先递归求解以p.left和p.right为根节点的子树的坡度以及节点之后，最后求解以p为根节点的子树的坡度以及节点之和。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def findTilt(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)[1]

    def dfs(self, now):
        if not now:
            return 0, 0

        left_sum, left_tilt = self.dfs(now.left)
        right_sum, right_tilt = self.dfs(now.right)
        return left_sum + right_sum + now.val, left_tilt + right_tilt + abs(left_sum - right_sum)
```
