---
title: "226. 翻转二叉树"
aliases: ["yiduobo的每日leetcode 226.翻转二叉树"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149312948"
zhihu_id: "149312948"
zhihu_title: "yiduobo的每日leetcode 226.翻转二叉树"
question_id: "226"
question: "翻转二叉树"
problem_url: "https://leetcode.cn/problems/invert-binary-tree/"
difficulty: "Easy"
created: "2020-06-18T23:35:19+08:00"
updated: "2020-06-18T23:35:19+08:00"
upvotes: 0
comments: 0
---

# 226. 翻转二叉树

> **[yiduobo的每日leetcode 226.翻转二叉树](https://zhuanlan.zhihu.com/p/149312948) · 知乎 · 2020-06-18 · 赞同 0**
> 力扣：[226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/) · Easy · 灵茶山艾府：[两种递归写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

226.翻转二叉树<https://leetcode-cn.com/problems/invert-binary-tree/>

非常经典的树操作的题目，递归或者迭代都可以做。我在这里选择的递归。具体做法为对于树中某个节点，先递归翻转其左子树和右子树，然后将左右子树互换，就完成了以该节点为根的子树的翻转了。

每个节点只会访问一次，因此最终的时间复杂度为O(n)。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def invertTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return now

        left_tree = self.dfs(now.left)
        right_tree = self.dfs(now.right)
        now.left = right_tree
        now.right = left_tree
        return now
```
