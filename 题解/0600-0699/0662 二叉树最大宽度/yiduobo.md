---
title: "662. 二叉树最大宽度"
aliases: ["yiduobo的每日leetcode 662.二叉树最大宽度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/286781588"
zhihu_id: "286781588"
zhihu_title: "yiduobo的每日leetcode 662.二叉树最大宽度"
question_id: "662"
question: "二叉树最大宽度"
problem_url: "https://leetcode.cn/problems/maximum-width-of-binary-tree/"
created: "2020-11-11T23:56:15+08:00"
updated: "2020-11-11T23:56:15+08:00"
upvotes: 0
comments: 0
---

# 662. 二叉树最大宽度

> **[yiduobo的每日leetcode 662.二叉树最大宽度](https://zhuanlan.zhihu.com/p/286781588) · 知乎 · 2020-11-11 · 赞同 0**
> 力扣：[662. 二叉树最大宽度](https://leetcode.cn/problems/maximum-width-of-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

662.二叉树最大宽度

[力扣](https://leetcode-cn.com/problems/maximum-width-of-binary-tree/)

题目要求二叉树中所有层中的最大宽度，那么我们可以将每一层的宽度都求出来，然后取最大值。对于每一层而言，其宽度就是当前层最左侧的节点与最右侧的节点位置之差，因此执行一趟层序遍历，对于每一层都计算两侧节点位置之差，取最大的差即可。

做法已经明确了，但是现在还需要想办法确定节点的位置。

注意到题目描述的是二叉树，且我们在计算位置的时候是按照满二叉树的位置来进行计算的，因此我们可以仿照用数组表示堆的做法来为节点进行编号，而节点最终的编号差就是位置之差。具体来说就是对于某个节点，若其编号为x，那么其左右孩子的编号分别为2x+1以及2x+2，我们在层序遍历的过程中维护这个位置信息然后计算每层的差值即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def widthOfBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        if not root:
            return 0
        q = [[root, 0]]
        l = 0
        r = 1
        res = 0
        while l < r:
            res = max(res, q[r - 1][1] - q[l][1] + 1)
            for index in range(l, r):
                node, pos = q[index]
                if node.left:
                    q.append([node.left, pos * 2 + 1])
                if node.right:
                    q.append([node.right, pos * 2 + 2])
            l = r
            r = len(q)

        return res
```
