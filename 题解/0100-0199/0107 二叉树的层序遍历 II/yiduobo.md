---
title: "107. 二叉树的层次遍历II"
aliases: ["yiduobo的每日leetcode 107.二叉树的层次遍历II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/array", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138148239"
zhihu_id: "138148239"
zhihu_title: "yiduobo的每日leetcode 107.二叉树的层次遍历II"
question_id: "107"
question: "二叉树的层序遍历 II"
problem_url: "https://leetcode.cn/problems/binary-tree-level-order-traversal-ii/"
difficulty: "Medium"
created: "2020-05-04T21:16:43+08:00"
updated: "2020-05-04T21:16:43+08:00"
upvotes: 0
comments: 0
---

# 107. 二叉树的层次遍历II

> **[yiduobo的每日leetcode 107.二叉树的层次遍历II](https://zhuanlan.zhihu.com/p/138148239) · 知乎 · 2020-05-04 · 赞同 0**
> 力扣：[107. 二叉树的层序遍历 II](https://leetcode.cn/problems/binary-tree-level-order-traversal-ii/) · Medium · 灵茶山艾府：[BFS 为什么要用队列？一个视频讲透！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

107.二叉树的层次遍历II <https://leetcode-cn.com/problems/binary-tree-level-order-traversal-ii/>

与102题一样（传送门在这里[yiduobo：yiduobo的每日leetcode 102.二叉树的层序遍历](https://zhuanlan.zhihu.com/p/137850637)），这里求出层次遍历之后将结果reverse即可。当然在过程中使用栈来做也行。

最后附上python代码，我选择的是简单的reverse做法：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def levelOrderBottom(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        res = []

        self.dfs(root, 1, res)
        res.reverse()
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
