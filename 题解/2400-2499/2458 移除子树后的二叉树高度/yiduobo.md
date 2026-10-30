---
title: "2458. 移除子树后的二叉树高度"
aliases: ["yiduobo的每日leetcode 2458.移除子树后的二叉树高度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/binary-tree", "leetcode/dfs", "leetcode/dp", "leetcode/dp-2", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586493676"
zhihu_id: "586493676"
zhihu_title: "yiduobo的每日leetcode 2458.移除子树后的二叉树高度"
question_id: "2458"
question: "移除子树后的二叉树高度"
problem_url: "https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/"
difficulty: "Hard"
rating: 2299
created: "2022-11-25T03:33:43+08:00"
updated: "2022-11-25T03:33:43+08:00"
upvotes: 0
comments: 0
---

# 2458. 移除子树后的二叉树高度

> **[yiduobo的每日leetcode 2458.移除子树后的二叉树高度](https://zhuanlan.zhihu.com/p/586493676) · 知乎 · 2022-11-25 · 赞同 0**
> 力扣：[2458. 移除子树后的二叉树高度](https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/) · Hard · 灵茶山艾府：[两遍 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2458.移除子树后的二叉树高度

<https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/>

首先不妨思考一下二叉树高度是如何定义的。按照题目的说法，树的高度是树根到其某个叶子节点路径的长度的最大值，而另一种常见的表示方法则是设树根的深度为0，然后按照孩子节点深度等于父亲节点深度加1的计算方式，使用bfs或者dfs遍历整颗树并计算出每个节点的深度，那么所有节点深度的最大值就是树的高度。

题目要求的是移除掉一颗子树之后二叉树的高度，可以发现，移除子树并不会对其他节点的深度造成影响，也就是说这里要求的其实是剩余节点深度的最大值。而对于移除整颗子树这种操作，一种常见的做法就是利用dfs序，将树的问题转化为区间问题。

关于dfs序的简单说明可以参考

[yiduobo：yiduobo的每日leetcode 1993.树上的操作](https://zhuanlan.zhihu.com/p/500177848)

在得到dfs序之后，每个询问实际上就变成了对于一个区间，删除其中某个子区间后剩余数中的最大值是多少。由于每个询问只会删除掉一个区间，那么剩下的数必然会形成一个前缀区间和一个后缀区间，题目要求的这两个剩下区间的最大值。对于这个问题，则可以先正反两趟遍历，分别预处理出区间的前缀最大值和后缀最大值，然后对于某个询问，就可以通过其移除节点在dfs序中管辖的范围来确定移除区间的左右边界，然后进一步转化为前缀区间和后缀区间的最大值进行求解。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def treeQueries(self, root, queries):
        """
        :type root: Optional[TreeNode]
        :type queries: List[int]
        :rtype: List[int]
        """

        depth = {}
        dfs_order = []
        start = {}
        end = {}

        def dfs(now, level):
            depth[now.val] = level
            dfs_order.append(now.val)
            start[now.val] = len(dfs_order) - 1

            if now.left:
                dfs(now.left, level + 1)
            if now.right:
                dfs(now.right, level + 1)
            end[now.val] = len(dfs_order) - 1

        dfs(root, 0)
        
        prefix_max = [depth[dfs_order[0]]]
        for index in range(1, len(dfs_order)):
            prefix_max.append(max(prefix_max[-1], depth[dfs_order[index]]))
        
        suffix_max = [depth[dfs_order[-1]]]
        for index in range(len(dfs_order) - 2, -1, -1):
            suffix_max.append(max(suffix_max[-1], depth[dfs_order[index]]))
        suffix_max.reverse()

        res = []
        for q in queries:
            res.append(0)
            print start[q], end[q]
            if start[q] > 0:
                res[-1] = max(res[-1], prefix_max[start[q] - 1])
            if end[q] < len(dfs_order) - 1:
                res[-1] = max(res[-1], suffix_max[end[q] + 1])
        
        return res
```
