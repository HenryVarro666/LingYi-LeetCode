---
title: "3319. 第K大的完美二叉子树的大小"
aliases: ["yiduobo的每日leetcode 3319.第K大的完美二叉子树的大小"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "leetcode/counting-sort", "leetcode/quickselect", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2164538889"
zhihu_id: "2164538889"
zhihu_title: "yiduobo的每日leetcode 3319.第K大的完美二叉子树的大小"
question_id: "3319"
question: "第 K 大的完美二叉子树的大小"
problem_url: "https://leetcode.cn/problems/k-th-largest-perfect-subtree-size-in-binary-tree/"
difficulty: "Medium"
rating: 1603
created: "2024-10-21T02:20:12+08:00"
updated: "2024-10-21T02:20:12+08:00"
upvotes: 1
comments: 0
---

# 3319. 第K大的完美二叉子树的大小

> **[yiduobo的每日leetcode 3319.第K大的完美二叉子树的大小](https://zhuanlan.zhihu.com/p/2164538889) · 知乎 · 2024-10-21 · 赞同 1**
> 力扣：[3319. 第 K 大的完美二叉子树的大小](https://leetcode.cn/problems/k-th-largest-perfect-subtree-size-in-binary-tree/) · Medium · 灵茶山艾府：[二叉树 DFS + 快速排序/计数排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3319.第K大的完美二叉子树的大小

[. - 力扣（LeetCode）](https://leetcode.cn/problems/k-th-largest-perfect-subtree-size-in-binary-tree/description/)

题目给出一颗二叉树的根节点root以及一个整数k，要求找出树中第k大的完美二叉子树的大小。若不存在，则返回-1。完美二叉树指的是所有叶子节点都在同一层，且树中每个父节点都恰有两个孩子。

对于完美二叉树，只有以下两种构成：

1、单独的叶子节点

2、左右子树都为完美二叉树，且左右子树的高度也相同

也就是说，在这里可以从根节点向下做dfs。对于当前处理的节点，先递归求解左右子树是否为完美二叉树，以及左右子树的高度，然后判断当前子树是否为完美二叉树以及高度，最后返回给上层节点使用。

另一方面， 对于一颗高度为height的完美二叉树，其中一共有2^height - 1个节点，也就是说本题只需要找出高度第k大的完美二叉树的树高，然后计算树中的节点数量并返回即可。

在实现上，可以使用一个大小为k的小根堆来储存所有完美二叉树的高度。dfs完成后，若堆的大小为k，那么堆顶元素就是第k大的完美二叉树的树高，计算出对应的节点数目即可；若对的大小不足k，则直接返回-1。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def kthLargestPerfectSubtree(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
        
        heap = []
        def dfs(now):
            left_prefect, left_height = True, 0 
            if now.left:
                left_prefect, left_height = dfs(now.left)
            
            right_prefect, right_height = True, 0
            if now.right:
                right_prefect, right_height = dfs(now.right)
            
            height = max(left_height, right_height) + 1
            if left_prefect and right_prefect and left_height == right_height:
                prefect = True
                heapq.heappush(heap, height)
                if len(heap) > k:
                    heapq.heappop(heap)
            else:
                prefect = False

            return prefect, height
        
        dfs(root)
        if len(heap) < k:
            return -1
        
        return (1 << (heap[0])) - 1
```
