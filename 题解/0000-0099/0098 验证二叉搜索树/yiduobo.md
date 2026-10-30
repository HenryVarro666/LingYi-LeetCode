---
title: "98. 验证二叉搜索树"
aliases: ["yiduobo的每日leetcode 98.验证二叉搜索树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/二-二叉树", "题单/LeetCode-热题-100/二叉树", "题单/面试经典-150-题/二叉搜索树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137571183"
zhihu_id: "137571183"
zhihu_title: "yiduobo的每日leetcode 98.验证二叉搜索树"
question_id: "98"
question: "验证二叉搜索树"
problem_url: "https://leetcode.cn/problems/validate-binary-search-tree/"
difficulty: "Medium"
created: "2020-04-30T22:42:14+08:00"
updated: "2020-04-30T22:42:14+08:00"
upvotes: 0
comments: 0
---

# 98. 验证二叉搜索树

> **[yiduobo的每日leetcode 98.验证二叉搜索树](https://zhuanlan.zhihu.com/p/137571183) · 知乎 · 2020-04-30 · 赞同 0**
> 力扣：[98. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/) · Medium · 灵茶山艾府：[【视频】前序中序后序，三种方法，一个视频讲透！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

98.验证二叉搜索树<https://leetcode-cn.com/problems/validate-binary-search-tree/>

递归的题目。分别验证左右子树是否合法，同时在验证的过程中统计出左子树与右子树中最大和最小值是多少，然后再判断当前树是否合法，并更新当前树的最大和最小值。

我们约定当一棵树不合法时，就返回None作为最大与最小值。接下来考察树中的某个节点，设其为root：

1、首先min_val \= max_val \= root.val。

2、若root有左子树，递归计算出左子树中的最大与最小值max_left, min_left。

若max_left为None，即左子树不合法，或者max_left >\= root.val，那么以root为根的树也不合法，直接返回None, None。

否则使用min_left来更新min_val，即min_val \= min(min_val, min_left)。

3、若root有右子树，同样递归计算出右子树中的最大与最小值max_right, min_right。

若min_right为None，即右子树不合法，或者min_right \<\= root.val，那么以root为根的树也不合法，直接返回None, None。

否则使用max_right来更新max_val，即max_val \= max(max_val, max_right)。

最后检测整棵树的min_val与max_val是否为None即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        if not root:
            return True

        min_tree, max_tree = self.dfs(root)
        return min_tree is not None

    def dfs(self, root):
        min_val = max_val = root.val

        if root.left:
            min_left, max_left = self.dfs(root.left)
            if max_left is None or max_left >= root.val:
                return None, None
            min_val = min(min_val, min_left)

        if root.right:
            min_right, max_right = self.dfs(root.right)
            if min_right is None or min_right <= root.val:
                return None, None
            max_val = max(max_val, max_right)

        return min_val, max_val
```
