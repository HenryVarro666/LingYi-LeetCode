---
title: "971. 翻转二叉树以匹配先序遍历"
aliases: ["yiduobo的每日leetcode 971.翻转二叉树以匹配先序遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362120299"
zhihu_id: "362120299"
zhihu_title: "yiduobo的每日leetcode 971.翻转二叉树以匹配先序遍历"
question_id: "971"
question: "翻转二叉树以匹配先序遍历"
problem_url: "https://leetcode.cn/problems/flip-binary-tree-to-match-preorder-traversal/"
created: "2021-04-03T19:28:23+08:00"
updated: "2021-04-03T19:28:23+08:00"
upvotes: 0
comments: 0
---

# 971. 翻转二叉树以匹配先序遍历

> **[yiduobo的每日leetcode 971.翻转二叉树以匹配先序遍历](https://zhuanlan.zhihu.com/p/362120299) · 知乎 · 2021-04-03 · 赞同 0**
> 力扣：[971. 翻转二叉树以匹配先序遍历](https://leetcode.cn/problems/flip-binary-tree-to-match-preorder-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

971.翻转二叉树以匹配先序遍历

[力扣](https://leetcode-cn.com/problems/flip-binary-tree-to-match-preorder-traversal/)

由于是先序遍历，我们也需要按照根-左-右的顺序对树进行dfs，同时需要关注遍历的顺序是否能匹配先序遍历。

对于当前处理到的节点now，设当前匹配到先序遍历中的位置p，那么：

1、若now.val不等于voyage[p]，那么根的节点就无法匹配，直接返回[-1]，否则将p往后移动一位。

2、接下来考察now的左右孩子。

若now没有左右孩子，那么直接返回[]即可。

若now只有一侧孩子，也没有翻转这一说，那么直接递归求解这一侧孩子并返回递归的结果。

若now有两侧的孩子，且此时now左孩子的值不等于voyage[p]，说明如果不进行翻转，左子树是无法匹配先序遍历的，因此必须进行翻转。由于这里进行了翻转，因此需要先递归求解右子树，然后递归求解左子树。若递归的结果都不为[-1]，那么说明可以成功匹配，于是返回当前节点编号加上右子树递归结果再加上左子树递归结果。

同样地，若now有两侧的孩子，且此时now左孩子的值等于voyage[p]，由于树中节点的值都不一样，因此这里不能进行翻转，于是直接按照正常先左后右的顺序递归求解子树。若递归的结果都不为[-1]，那么说明可以成功匹配，于是返回左子树递归结果加上右子树递归结果。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def flipMatchVoyage(self, root, voyage):
        """
        :type root: TreeNode
        :type voyage: List[int]
        :rtype: List[int]
        """

        self.p = 0
        return self.dfs(root, voyage)

    def dfs(self, now, voyage):
        if now.val != voyage[self.p]:
            return [-1]
        
        self.p += 1

        if not now.left:
            if not now.right:
                return []
            else:
                return self.dfs(now.right, voyage)
        elif not now.right:
            return self.dfs(now.left, voyage)
        elif now.left.val != voyage[self.p]:
            left_ret = self.dfs(now.right, voyage)
            if left_ret == [-1]:
                return [-1]
            right_ret = self.dfs(now.left, voyage)
            if right_ret == [-1]:
                return [-1]
            return [now.val] + left_ret + right_ret
        else:
            left_ret = self.dfs(now.left, voyage)
            if left_ret == [-1]:
                return [-1]
            right_ret = self.dfs(now.right, voyage)
            if right_ret == [-1]:
                return [-1]
            return left_ret + right_ret
```
