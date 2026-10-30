---
title: "111. 二叉树的最小深度"
aliases: ["yiduobo的每日leetcode 111.二叉树的最小深度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138539140"
zhihu_id: "138539140"
zhihu_title: "yiduobo的每日leetcode 111.二叉树的最小深度"
question_id: "111"
question: "二叉树的最小深度"
problem_url: "https://leetcode.cn/problems/minimum-depth-of-binary-tree/"
difficulty: "Easy"
created: "2020-05-06T17:58:42+08:00"
updated: "2020-05-06T17:58:42+08:00"
upvotes: 1
comments: 0
---

# 111. 二叉树的最小深度

> **[yiduobo的每日leetcode 111.二叉树的最小深度](https://zhuanlan.zhihu.com/p/138539140) · 知乎 · 2020-05-06 · 赞同 1**
> 力扣：[111. 二叉树的最小深度](https://leetcode.cn/problems/minimum-depth-of-binary-tree/) · Easy · 灵茶山艾府：[两种方法：自顶向下/自底向上（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

111.二叉树的最小深度<https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/>

比较基础的题目。做法与上一题类似，也是先递归求解左右子树的最小深度，然后取较小的那一边加一作为当前树的最小深度返回。需要注意左右子树为空的情况。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def minDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return 0

        if not now.left:
            if not now.right:
                return 1
            else:
                return self.dfs(now.right) + 1
        else:
            if not now.right:
                return self.dfs(now.left) + 1
            else:
                return min(self.dfs(now.left), self.dfs(now.right)) + 1
```
