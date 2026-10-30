---
title: "1080. 根到叶路径上的不足节点"
aliases: ["yiduobo的每日leetcode 1080.根到叶路径上的不足节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373110105"
zhihu_id: "373110105"
zhihu_title: "yiduobo的每日leetcode 1080.根到叶路径上的不足节点"
question_id: "1080"
question: "根到叶路径上的不足节点"
problem_url: "https://leetcode.cn/problems/insufficient-nodes-in-root-to-leaf-paths/"
difficulty: "Medium"
rating: 1805
created: "2021-05-17T23:49:48+08:00"
updated: "2021-05-17T23:49:48+08:00"
upvotes: 0
comments: 0
---

# 1080. 根到叶路径上的不足节点

> **[yiduobo的每日leetcode 1080.根到叶路径上的不足节点](https://zhuanlan.zhihu.com/p/373110105) · 知乎 · 2021-05-17 · 赞同 0**
> 力扣：[1080. 根到叶路径上的不足节点](https://leetcode.cn/problems/insufficient-nodes-in-root-to-leaf-paths/) · Medium · 灵茶山艾府：[简洁写法，调用自身！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1080.根到叶路径上的不足节点

[力扣](https://leetcode-cn.com/problems/insufficient-nodes-in-root-to-leaf-paths/)

由于这里涉及到删除节点的操作，那么有两种可行的做法，一种是对于当前节点，计算出其左孩子和右孩子是否需要删除，然后对当前节点进行操作；另一种则是对于当前节点，记录其父亲节点，若当前节点需要删除，则操作其父亲节点进行删除。

我在这里采用的是第一种做法，那么对于当前节点，我们需要先分别递归求出其左子树和右子树中路径和的最大值，若左子树的路径和最大值小于limit，那么将当前节点的左孩子删去；同样地，若右子树的路径和最大值小于limit，那么将当前节点的右孩子删去。删除完毕后，返回这两个最大值中较大的那一个，作为以当前节点为根节点的子树中最大的路径和。

对于路径和的求解，则可以在递归过程中携带一个变量，表示从根节点到当前节点的路径之和。每处理到一个节点，就将这个值加上当前节点的值。

需要注意边界情况，若当前节点为叶子节点，那么直接返回路径和即可。若最终整棵树中的最大路径和都小于limit，那么此时应该返回空，否则返回root。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sufficientSubset(self, root, limit):
        """
        :type root: TreeNode
        :type limit: int
        :rtype: TreeNode
        """

        max_s = self.dfs(root, 0, limit)
        if max_s < limit:
            return None
        else:
            return root
    
    def dfs(self, now, s, limit):
        s += now.val
        if not now.left:
            if not now.right:
                return s
            else:
                max_r = self.dfs(now.right, s, limit)
                if max_r < limit:
                    now.right = None
                return max_r
        elif not now.right:
            max_l = self.dfs(now.left, s, limit)
            if max_l < limit:
                now.left = None
            return max_l
        else:
            max_l = self.dfs(now.left, s, limit)
            max_r = self.dfs(now.right, s, limit)
            if max_l < limit:
                now.left = None
            if max_r < limit:
                now.right = None
            return max(max_l, max_r)
```
