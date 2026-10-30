---
title: "3879. 二叉树中的最大不同路径和"
aliases: ["yiduobo的每日leetcode 3879.二叉树中的最大不同路径和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2021744023749044086"
zhihu_id: "2021744023749044086"
zhihu_title: "yiduobo的每日leetcode 3879.二叉树中的最大不同路径和"
question_id: "3879"
question: "二叉树中的最大不同路径和"
problem_url: "https://leetcode.cn/problems/maximum-distinct-path-sum-in-a-binary-tree/"
created: "2026-03-30T00:29:17+08:00"
updated: "2026-03-30T00:29:18+08:00"
upvotes: 3
comments: 0
---

# 3879. 二叉树中的最大不同路径和

> **[yiduobo的每日leetcode 3879.二叉树中的最大不同路径和](https://zhuanlan.zhihu.com/p/2021744023749044086) · 知乎 · 2026-03-30 · 赞同 3**
> 力扣：[3879. 二叉树中的最大不同路径和](https://leetcode.cn/problems/maximum-distinct-path-sum-in-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3879.二叉树中的最大不同路径和

<https://leetcode.cn/problems/maximum-distinct-path-sum-in-a-binary-tree/description/>

题目给出一颗二叉树，其中每个节点不超过1000，且每个节点除了左右孩子外，还包含一个节点值val。另外给出节点为root，表示二叉树的根节点。

树中的有效路径值的是一系列相连的节点，满足：

- 路径可以在树中的任意节点开始和结束
- 路径不需要经过根节点
- 路径上所有节点值互不相同

问所有有效路径中，最大可能得到的节点值之和是多少。

由于题目的数据规模不大，因此可以考虑O(n^2)的算法。已知从某个节点开始遍历整棵树的时间复杂度为O(n)，那么在这里完全可以枚举路径的起点start，然后从start开始做dfs，找出所有以start为起点的合法路径，并使用这个路径值更新答案。在这里选择dfs而不是bfs的理由是题目中的合法路径中不允许出现节点值相同的节点，因此在这里需要使用一个集合记录目前路径上所有出现过的节点值，同时随着dfs的递归或者回溯来修改这个结合。

由于题目中仅给出了左右孩子，因此还需要额外先执行一次dfs或者bfs，使用哈希表fa记录每个节点的父亲节点是什么，然后再开始上面的枚举起点然后dfs的做法。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxSum(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        
        fa = {}
        fa[root] = None
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            if now.left:
                fa[now.left] = now
                q.append(now.left)
                tail += 1
            if now.right:
                fa[now.right] = now
                q.append(now.right)
                tail += 1
        
        global res
        res = None

        def dfs(now, vis, dis):
            global res
            if res is None or res < dis:
                res = dis
            if fa[now] is not None and fa[now].val not in vis:
                vis.add(fa[now].val)
                dfs(fa[now], vis, dis + fa[now].val)
                vis.remove(fa[now].val)
            
            if now.left and now.left.val not in vis:
                vis.add(now.left.val)
                dfs(now.left, vis, dis + now.left.val)
                vis.remove(now.left.val)
            
            if now.right and now.right.val not in vis:
                vis.add(now.right.val)
                dfs(now.right, vis, dis + now.right.val)
                vis.remove(now.right.val)

        for start in fa:
            vis = set()
            vis.add(start.val)
            dfs(start, vis, start.val)
        
        return res
```
