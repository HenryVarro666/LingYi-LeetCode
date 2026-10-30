---
title: "988. 从叶节点开始的最小字符串"
aliases: ["yiduobo的每日leetcode 988.从叶节点开始的最小字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364331064"
zhihu_id: "364331064"
zhihu_title: "yiduobo的每日leetcode 988.从叶节点开始的最小字符串"
question_id: "988"
question: "从叶节点开始的最小字符串"
problem_url: "https://leetcode.cn/problems/smallest-string-starting-from-leaf/"
created: "2021-04-12T23:03:08+08:00"
updated: "2021-04-12T23:03:08+08:00"
upvotes: 0
comments: 0
---

# 988. 从叶节点开始的最小字符串

> **[yiduobo的每日leetcode 988.从叶节点开始的最小字符串](https://zhuanlan.zhihu.com/p/364331064) · 知乎 · 2021-04-12 · 赞同 0**
> 力扣：[988. 从叶节点开始的最小字符串](https://leetcode.cn/problems/smallest-string-starting-from-leaf/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

988.从叶节点开始的最小字符串

[力扣](https://leetcode-cn.com/problems/smallest-string-starting-from-leaf/)

直接进行dfs，维护一个字符串suffix表示从根节点下来到当前节点形成的字符串是什么，dfs的结果则定义为以当前节点为根节点的子树中，从叶节点开始，到原始的root结束的最小字符串是什么。那么对于当前节点now：

1、首先将now.val根据对应关系转化为小写字符并拼在suffix的头部

2、若now没有左右孩子，那么now是一个叶子节点，此时suffix就代表从now这个叶子节点开始的字符串，于是直接返回suffix

3、若now仅有左孩子或右孩子中的一方，那么直接递归求解

4、若now同时拥有左右孩子，那么需要先递归求解左右子树，然后对于返回左右子树的答案，选择其中较小的那一个返回即可

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def smallestFromLeaf(self, root):
        """
        :type root: TreeNode
        :rtype: str
        """

        return self.dfs(root, "")

    def dfs(self, now, suffix):
        now_suffix = chr(now.val + 97) + suffix
        if not now.left:
            if not now.right:
                return now_suffix
            else:
                return self.dfs(now.right, now_suffix)
        elif not now.right:
            return self.dfs(now.left, now_suffix)
        else:
            return min(self.dfs(now.left, now_suffix), self.dfs(now.right, now_suffix))
```
