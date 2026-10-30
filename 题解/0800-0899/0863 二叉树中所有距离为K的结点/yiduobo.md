---
title: "863. 二叉树中所有距离为K的结点"
aliases: ["yiduobo的每日leetcode 863.二叉树中所有距离为K的结点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349823736"
zhihu_id: "349823736"
zhihu_title: "yiduobo的每日leetcode 863.二叉树中所有距离为K的结点"
question_id: "863"
question: "二叉树中所有距离为K的结点"
problem_url: "https://leetcode.cn/problems/all-nodes-distance-k-in-binary-tree/"
created: "2021-02-08T21:53:10+08:00"
updated: "2021-02-08T21:53:10+08:00"
upvotes: 1
comments: 0
---

# 863. 二叉树中所有距离为K的结点

> **[yiduobo的每日leetcode 863.二叉树中所有距离为K的结点](https://zhuanlan.zhihu.com/p/349823736) · 知乎 · 2021-02-08 · 赞同 1**
> 力扣：[863. 二叉树中所有距离为K的结点](https://leetcode.cn/problems/all-nodes-distance-k-in-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

863.二叉树中所有距离为K的结点

[力扣](https://leetcode-cn.com/problems/all-nodes-distance-k-in-binary-tree/)

感觉应该可以参考之前某题计算树中距离和的做法来解决，但是感觉细节比较复杂，因此我这里采用的是比较暴力的做法。

首先从root开始，对整棵树进行一趟dfs，记录下每个节点的父节点是什么。接下来从target开始进行bfs，对于每个节点而言，每次扩展的节点除了当前节点的孩子节点之外，还需要额外考察当前节点的父亲节点。

当bfs进行完第K轮之后，这一轮扩展到的所有节点就是最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def distanceK(self, root, target, K):
        """
        :type root: TreeNode
        :type target: TreeNode
        :type K: int
        :rtype: List[int]
        """

        fa = {root.val:None}
        self.dfs(root, fa)
        q = [target]
        l = 0
        r = 1
        used = set([target.val])
        
        dis = 0
        while l < r:
            if dis == K:
                return [x.val for x in q[l:r]]
            dis += 1
            for now in q[l:r]:
                if fa[now.val] is not None and fa[now.val].val not in used:
                    q.append(fa[now.val])
                    used.add(fa[now.val].val)
                if now.left is not None and now.left.val not in used:
                    q.append(now.left)
                    used.add(now.left.val)
                if now.right is not None and now.right.val not in used:
                    q.append(now.right)
                    used.add(now.right.val)

            l, r = r, len(q)
            
        
        return []

    def dfs(self, now, fa):
        if now.left:
            fa[now.left.val] = now
            self.dfs(now.left, fa)
        if now.right:
            fa[now.right.val] = now
            self.dfs(now.right, fa)
```
