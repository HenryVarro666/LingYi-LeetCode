---
title: "103. 二叉树的锯齿形层次遍历"
aliases: ["yiduobo的每日leetcode 103.二叉树的锯齿形层次遍历"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/array", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/面试经典-150-题/二叉树层次遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137851280"
zhihu_id: "137851280"
zhihu_title: "yiduobo的每日leetcode 103.二叉树的锯齿形层次遍历"
question_id: "103"
question: "二叉树的锯齿形层序遍历"
problem_url: "https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/"
difficulty: "Medium"
created: "2020-05-02T22:58:36+08:00"
updated: "2020-05-02T22:58:36+08:00"
upvotes: 0
comments: 0
---

# 103. 二叉树的锯齿形层次遍历

> **[yiduobo的每日leetcode 103.二叉树的锯齿形层次遍历](https://zhuanlan.zhihu.com/p/137851280) · 知乎 · 2020-05-02 · 赞同 0**
> 力扣：[103. 二叉树的锯齿形层序遍历](https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/) · Medium · 灵茶山艾府：[【视频】BFS 为什么要用队列？一个视频讲透！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

103.二叉树的锯齿形层次遍历<https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/>

与上一题类似（传送门在这里[yiduobo：yiduobo的每日leetcode 102.二叉树的层序遍历](https://zhuanlan.zhihu.com/p/137850637)），同样是搜索回溯并记录下当前的层级来求出层次遍历。

由于题目要求的是锯齿形的层次遍历，那么只需要将层次遍历中的奇数层反过来即可。

最后附上python代码，与上一题相比其实就只是多出了level_res.reverse()那一段：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def zigzagLevelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        res = []

        self.dfs(root, 1, res)

        for index, level_res in enumerate(res):
            if index % 2 == 1:
                level_res.reverse()
        return res

    def dfs(self, now, level, res):
        if now is None:
            return
        if level > len(res):
            res.append([])
        res[level - 1].append(now.val)
        if now.left:
            self.dfs(now.left, level + 1, res)
        if now.right:
            self.dfs(now.right, level + 1, res)
```
