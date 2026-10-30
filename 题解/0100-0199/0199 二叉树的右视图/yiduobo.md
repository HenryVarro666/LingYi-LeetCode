---
title: "199. 二叉树的右视图"
aliases: ["yiduobo的每日leetcode 199.二叉树的右视图"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树层次遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146194075"
zhihu_id: "146194075"
zhihu_title: "yiduobo的每日leetcode 199.二叉树的右视图"
question_id: "199"
question: "二叉树的右视图"
problem_url: "https://leetcode.cn/problems/binary-tree-right-side-view/"
difficulty: "Medium"
created: "2020-06-05T22:27:25+08:00"
updated: "2020-06-05T22:27:25+08:00"
upvotes: 0
comments: 0
---

# 199. 二叉树的右视图

> **[yiduobo的每日leetcode 199.二叉树的右视图](https://zhuanlan.zhihu.com/p/146194075) · 知乎 · 2020-06-05 · 赞同 0**
> 力扣：[199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/) · Medium · 灵茶山艾府：[两种方法：BFS / DFS（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

199.二叉树的右视图<https://leetcode-cn.com/problems/binary-tree-right-side-view/>

实际上就是先求出二叉树的层序遍历，然后将每一层的最后一个节点组合起来就是答案了。由于题目只需要每一层的最后一个节点，那么可以将层序遍历的顺序改成从右往左遍历，然后通过答案数组的长度来判断当前遍历到的节点是否为本层的最右侧节点，就不用记录整个层序遍历的结果了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def rightSideView(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        if not root:
            return []

        res = []
        self.dfs(root, 0, res)
        return res

    def dfs(self, now, level, res):
        if len(res) == level:
            res.append(now.val)

        if now.right:
            self.dfs(now.right, level + 1, res)
        if now.left:
            self.dfs(now.left, level + 1, res)
```
