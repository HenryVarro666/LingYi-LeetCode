---
title: "104. 二叉树的最大深度"
aliases: ["yiduobo的每日leetcode 104.二叉树的最大深度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138000614"
zhihu_id: "138000614"
zhihu_title: "yiduobo的每日leetcode 104.二叉树的最大深度"
question_id: "104"
question: "二叉树的最大深度"
problem_url: "https://leetcode.cn/problems/maximum-depth-of-binary-tree/"
difficulty: "Easy"
created: "2020-05-03T23:04:26+08:00"
updated: "2020-05-03T23:04:26+08:00"
upvotes: 0
comments: 0
---

# 104. 二叉树的最大深度

> **[yiduobo的每日leetcode 104.二叉树的最大深度](https://zhuanlan.zhihu.com/p/138000614) · 知乎 · 2020-05-03 · 赞同 0**
> 力扣：[104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) · Easy · 灵茶山艾府：[【视频讲解】让你对递归的理解更上一层楼！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

104.二叉树的最大深度<https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/>

比较基础的树操作的题目。

当前树的深度为左子树深度和右子树深度中较深的那一个，再加上当前这一层，因此可以递归求解左子树的深度left_depth与右子树的深度right_depth，然后当前树的深度就是max(left_depth, right_depth) + 1。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def maxDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)

    def dfs(self, now):
        if now is None:
            return 0

        if now.left:
            left_depth = self.dfs(now.left)
        else:
            left_depth = 0
        if now.right:
            right_depth = self.dfs(now.right)
        else:
            right_depth = 0
            
        return max(left_depth, right_depth) + 1
```
