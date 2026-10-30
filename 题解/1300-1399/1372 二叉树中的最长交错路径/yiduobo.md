---
title: "1372. 二叉树中的最长交错路径"
aliases: ["yiduobo的每日leetcode 1372.二叉树中的最长交错路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400848299"
zhihu_id: "400848299"
zhihu_title: "yiduobo的每日leetcode 1372.二叉树中的最长交错路径"
question_id: "1372"
question: "二叉树中的最长交错路径"
problem_url: "https://leetcode.cn/problems/longest-zigzag-path-in-a-binary-tree/"
created: "2021-08-17T23:35:18+08:00"
updated: "2021-08-17T23:36:18+08:00"
upvotes: 0
comments: 0
---

# 1372. 二叉树中的最长交错路径

> **[yiduobo的每日leetcode 1372.二叉树中的最长交错路径](https://zhuanlan.zhihu.com/p/400848299) · 知乎 · 2021-08-17 · 赞同 0**
> 力扣：[1372. 二叉树中的最长交错路径](https://leetcode.cn/problems/longest-zigzag-path-in-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1372.二叉树中的最长交错路径

[力扣](https://leetcode-cn.com/problems/longest-zigzag-path-in-a-binary-tree/)

可以发现，一条长为k的路径上一共有k + 1个节点，因此方便起见我们也可以将题目转化成求最终交错路径上节点的数目。

考虑到二叉树中的每个点都可能成为交错路径的起点，那么对于每个点，我们都需要求出以该点为起点，第一步向左以及第一步向右的最长交错路径中节点的数目。

对于某个点now，我们定义left以及right为以now为起点的，第一步向左以及第一步向右的最长交错路径中节点的数目。

接下来考虑路径的构成。以该点为起点的交错路径的第一步如果向左，那么路径上的下一个点必然是now.left，同时从now.left开始的交错路径的下一步必须向右。如果我们先递归求解now.left，得到对应的l_left以及l_right，分别表示以now.left为起点的，第一步向左以及第一步向右的最长交错路径中节点的数目，那么就有left \= l_right + 1。

同样地，我们也可以得出right \= r_left + 1。

另外，在递归求解的过程中我们也可以顺便求出子树中最长交错路径上节点的数目。简单来说可以分为两种情况。

第一种情况就是以now为根节点的子树中的最长交错路径不经过now，那么其中节点的数目必然等于max(l_res, r_res)，其中l_res和r_res分别表示以now.left和now.right作为根节点的子树中最长交错路径中节点的数目。

第二种情况则是最长交错路径经过now，那么根据定义，其必然是第一步向左或第一步向右中更长的那一条，因此其中节点的数目就等于max(left, right)。

综合起来，就有res \= max(l_res, r_res, left, right)

根据上面的做法，我们从根开始进行dfs，对于当前处理的节点now：

1、若now有左孩子，那么递归求解now.left，得到l_left，l_right以及l_res。若不存在左孩子，那么l_left，l_right以及l_res都为0。

2、若now有右孩子，那么递归求解now.right，得到r_left，r_right以及r_res。若不存在右孩子，那么r_left，r_right以及r_res都为0。

3、接下来考察now，就有

left \= l_right + 1

right \= r_left + 1

res \= max(l_res, r_res, left, right)

另外，dfs完成后需要注意的是，当前得到的res是最长交错路径上节点的数目，其长度应该是res - 1。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def longestZigZag(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)[0] - 1
    
    def dfs(self, now):
        if not now.left:
            l_res = 0
            l_left = 0
            l_right = 0
        else:
            l_res, l_left, l_right = self.dfs(now.left)
        
        if not now.right:
            r_res = 0
            r_left = 0
            r_right = 0
        else:
            r_res, r_left, r_right = self.dfs(now.right)
        
        res = max(l_res, r_res, l_right + 1, r_left + 1)

        return res, l_right + 1, r_left + 1
```
