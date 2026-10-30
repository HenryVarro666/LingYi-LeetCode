---
title: "114. 二叉树展开为链表"
aliases: ["yiduobo的每日leetcode 114.二叉树展开为链表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/138850520"
zhihu_id: "138850520"
zhihu_title: "yiduobo的每日leetcode 114.二叉树展开为链表"
question_id: "114"
question: "二叉树展开为链表"
problem_url: "https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/"
difficulty: "Medium"
created: "2020-05-07T22:11:46+08:00"
updated: "2020-05-07T22:11:46+08:00"
upvotes: 1
comments: 0
---

# 114. 二叉树展开为链表

> **[yiduobo的每日leetcode 114.二叉树展开为链表](https://zhuanlan.zhihu.com/p/138850520) · 知乎 · 2020-05-07 · 赞同 1**
> 力扣：[114. 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) · Medium · 灵茶山艾府：[两种方法：头插法/分治（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

114.二叉树展开为链表<https://leetcode-cn.com/problems/flatten-binary-tree-to-linked-list/>

很有意思的题目，与94题有些类似（传送门在这里[yiduobo：yiduobo的每日leetcode 94.二叉树的中序遍历](https://zhuanlan.zhihu.com/p/137080593)。

对于树中的一个节点p，可能有下面几种情况：

1、p是一个叶子结点：此时什么都不需要做。

2、p只有右子树：直接计算右子树即可。

3、p拥有左子树：可以发现，这个链表是树的前序遍历，于是左孩子应该接在p后面，成为p的右孩子，而p原来的右孩子则应该接在**左子树最右边节点的后面**。于是可以先通过94题相同的方式找到该节点，然后将该节点的右孩子指向p的右子树。接下来将p的左子树变成p的右子树，然后计算右子树即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def flatten(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """

        now = root
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now.right
                now.right = now.left
                now.left = None
                now = now.right
            else:
                now = now.right
        
        return root
```
