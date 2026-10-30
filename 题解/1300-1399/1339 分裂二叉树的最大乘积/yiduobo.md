---
title: "1339. 分裂二叉树的最大乘积"
aliases: ["yiduobo的每日leetcode 1339.分裂二叉树的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396050468"
zhihu_id: "396050468"
zhihu_title: "yiduobo的每日leetcode 1339.分裂二叉树的最大乘积"
question_id: "1339"
question: "分裂二叉树的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-splitted-binary-tree/"
difficulty: "Medium"
rating: 1675
created: "2021-08-03T22:46:36+08:00"
updated: "2021-08-03T22:46:36+08:00"
upvotes: 1
comments: 0
---

# 1339. 分裂二叉树的最大乘积

> **[yiduobo的每日leetcode 1339.分裂二叉树的最大乘积](https://zhuanlan.zhihu.com/p/396050468) · 知乎 · 2021-08-03 · 赞同 1**
> 力扣：[1339. 分裂二叉树的最大乘积](https://leetcode.cn/problems/maximum-product-of-splitted-binary-tree/) · Medium · 灵茶山艾府：[两次 DFS，或者提前保存子树和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1339.分裂二叉树的最大乘积

[力扣](https://leetcode-cn.com/problems/maximum-product-of-splitted-binary-tree/)

设删除的边连接的孩子节点为x，那么观察后可以发现，此时新的两棵树的节点权重之和分别是以x为根节点的子树的节点和，以及除了以x为根节点的子树之外的其他节点和。

于是一个自然的想法就是先求解出以每个节点为根节点的子树的和，然后枚举每个非根节点x，那么此时得到的乘积就是f[x] \* (f[root] - f[x])，其中的最大值即为最终答案。

对于求解子树节点和，可以从root开始进行dfs。对于当前节点now，先递归求解左右孩子，得到其左右子树的节点和l_sum和r_sum，那么以now为根节点的子树节点和就是l_sum + r_sum + now.val。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxProduct(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        weight_list = []
        self.dfs(root, weight_list)
        res = 0
        for weight in weight_list:
            res = max(res, (weight_list[-1] - weight) * weight)
        
        return res % (10 ** 9 + 7)
    
    def dfs(self, now, weight_list):
        weight = now.val
        if now.left:
            weight += self.dfs(now.left, weight_list)
        if now.right:
            weight += self.dfs(now.right, weight_list)
        
        weight_list.append(weight)
        return weight
```
