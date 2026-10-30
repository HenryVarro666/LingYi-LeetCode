---
title: "102. 二叉树的层序遍历"
aliases: ["yiduobo的每日leetcode 102.二叉树的层序遍历"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树层次遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137850637"
zhihu_id: "137850637"
zhihu_title: "yiduobo的每日leetcode 102.二叉树的层序遍历"
question_id: "102"
question: "二叉树的层序遍历"
problem_url: "https://leetcode.cn/problems/binary-tree-level-order-traversal/"
difficulty: "Medium"
created: "2020-05-02T22:53:48+08:00"
updated: "2020-05-02T22:53:48+08:00"
upvotes: 0
comments: 0
---

# 102. 二叉树的层序遍历

> **[yiduobo的每日leetcode 102.二叉树的层序遍历](https://zhuanlan.zhihu.com/p/137850637) · 知乎 · 2020-05-02 · 赞同 0**
> 力扣：[102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) · Medium · 灵茶山艾府：[BFS 为什么要用队列？一个视频讲透！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

102.二叉树的层序遍历<https://leetcode-cn.com/problems/binary-tree-level-order-traversal/>

树操作的题目，做法也比较简单。从根节点开始往下搜索回溯，在搜索过程中记录下当前的层级，然后每碰到一个节点就将其加入到当前层级的list中即可。

最后附上python代码，其中level表示当前的层级：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """

        res = []

        self.dfs(root, 1, res)
        return res
    
    def dfs(self, now, level, res):
        if now is None:
            return 

        if len(res) < level:
            res.append([])
        res[level - 1].append(now.val)
        if now.left:
            self.dfs(now.left, level + 1, res)
        if now.right:
            self.dfs(now.right, level + 1, res)
```
