---
title: "543. 二叉树的直径"
aliases: ["yiduobo的每日leetcode 543.二叉树的直径"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP", "题单/LeetCode-热题-100/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261215960"
zhihu_id: "261215960"
zhihu_title: "yiduobo的每日leetcode 543.二叉树的直径"
question_id: "543"
question: "二叉树的直径"
problem_url: "https://leetcode.cn/problems/diameter-of-binary-tree/"
difficulty: "Easy"
created: "2020-10-09T21:13:22+08:00"
updated: "2020-10-09T21:13:22+08:00"
upvotes: 1
comments: 0
---

# 543. 二叉树的直径

> **[yiduobo的每日leetcode 543.二叉树的直径](https://zhuanlan.zhihu.com/p/261215960) · 知乎 · 2020-10-09 · 赞同 1**
> 力扣：[543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/) · Easy · 灵茶山艾府：[【视频】彻底掌握直径 DP，从二叉树到一般树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

543.二叉树的直径<https://leetcode-cn.com/problems/diameter-of-binary-tree/>

一般来说，求解二叉树直径的做法是从其中任意节点开始进行dfs，走到最远处的节点，然后从这个最远处的节点再进行一趟dfs，第二趟dfs的路径即为树的直径。

不过在这里，由于树储存的形式是自顶向下的，从儿子节点回溯不到父亲节点，因此需要另想办法。

首先可以明确的一点是，树的直径必然是由某棵子树的根节点，加上其左子树中到达左孩子的最长路径，再加上右子树中到达右孩子的最长路径组成，在这里左右子树都可能为空。

那么我们就可以对于每个节点，先递归求解其结果左右孩子的最长路径长度，以及左右子树中到达左孩子和右孩子的最长路径长度left_depth以及right_depth。

经过当前节点的最长路径长度就是left_depth + right_depth +1，用这个值来更新答案，然后返回max(left_depth, right_depth) + 1，即到达当前节点最路径。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def diameterOfBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        self.res = 1

        self.dfs(root)
        return self.res - 1

    def dfs(self, now):
        if not now:
            return 0

        left_depth = self.dfs(now.left)
        right_depth = self.dfs(now.right)
        self.res = max(self.res, left_depth + right_depth + 1)
        return max(left_depth, right_depth) + 1
```
