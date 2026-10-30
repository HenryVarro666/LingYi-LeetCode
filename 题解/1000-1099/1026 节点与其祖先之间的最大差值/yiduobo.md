---
title: "1026. 节点与其祖先之间的最大差值"
aliases: ["yiduobo的每日leetcode 1026.节点与其祖先之间的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369325485"
zhihu_id: "369325485"
zhihu_title: "yiduobo的每日leetcode 1026.节点与其祖先之间的最大差值"
question_id: "1026"
question: "节点与其祖先之间的最大差值"
problem_url: "https://leetcode.cn/problems/maximum-difference-between-node-and-ancestor/"
difficulty: "Medium"
rating: 1446
created: "2021-05-01T23:00:14+08:00"
updated: "2021-05-01T23:00:14+08:00"
upvotes: 0
comments: 0
---

# 1026. 节点与其祖先之间的最大差值

> **[yiduobo的每日leetcode 1026.节点与其祖先之间的最大差值](https://zhuanlan.zhihu.com/p/369325485) · 知乎 · 2021-05-01 · 赞同 0**
> 力扣：[1026. 节点与其祖先之间的最大差值](https://leetcode.cn/problems/maximum-difference-between-node-and-ancestor/) · Medium · 灵茶山艾府：[两种方法：自顶向下/自底向上（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1026.节点与其祖先之间的最大差值

[力扣](https://leetcode-cn.com/problems/maximum-difference-between-node-and-ancestor/)

对于节点now为根节点的子树而言，now必然是树中其他节点的祖先节点，因此now与子树种其他节点形成的节点对都可能是最终答案。更进一步地，由于题目这里要求的是节点值之差的绝对值，那么在now.val固定的情况下，我们只需要找出子树中其他节点的最大值ma以及最小值mi，那么以now为祖先的节点对的最大差值就是max(|now.val - ma|, |now.val - mi|)，然后用这个值更新答案即可。

对于子树中其他节点的最大值以及最小值，我们则可以递归求解，先分别递归求解左子树和右子树中节点的最大值和最小值，然后对比左右的最大值和最小值从而得到树中除now之外的其他节点的最大值和最小值。

于是现在就有了一种做法，从根节点开始向下递归求解。对于以now为根节点的子树，我们需要求解的是子树中的最优解、最大值以及最小值，那么：

1、首先可以递归求解左右子树，分别得到l_res、l_max、l_min以及r_res、r_max、r_min，分别表示左右子树的最优解、最大值以及最小值。

2、接下来可以通过max(now.val, l_max, r_max)来得到以now为根节点的子树中的最大值，同样地，通过min(now.val, l_min, r_min)则可以得到以now为根节点地子树中的最小值

3、最后更新以now为根节点的子树的最优解，那么此时地最优解可能来自左右子树中的某个节点对，或者就来自now与子树中某个节点，于是应该对比l_res、r_res、abs(now.val - max(l_max, r_max))以及abs(now.val - min(l_min, r_min))这几个值，其中的最大值就是以now为根节点的子树的最优解。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxAncestorDiff(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)[0]
    
    def dfs(self, now):
        res = 0
        ma = mi = now.val

        if now.left:
            l_res, l_max, l_min = self.dfs(now.left)
            res = max(res, l_res, abs(now.val - l_max), abs(now.val - l_min))
            ma = max(ma, l_max)
            mi = min(mi, l_min)
        
        if now.right:
            r_res, r_max, r_min = self.dfs(now.right)
            res = max(res, r_res, abs(now.val - r_max), abs(now.val - r_min))
            ma = max(ma, r_max)
            mi = min(mi, r_min)
        
        return res, ma, mi
```
