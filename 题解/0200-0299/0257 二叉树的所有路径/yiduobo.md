---
title: "257. 二叉树的所有路径"
aliases: ["yiduobo的每日leetcode 257.二叉树的所有路径"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150993879"
zhihu_id: "150993879"
zhihu_title: "yiduobo的每日leetcode 257.二叉树的所有路径"
question_id: "257"
question: "二叉树的所有路径"
problem_url: "https://leetcode.cn/problems/binary-tree-paths/"
difficulty: "Easy"
created: "2020-06-27T15:52:39+08:00"
updated: "2020-06-27T15:52:39+08:00"
upvotes: 0
comments: 1
---

# 257. 二叉树的所有路径

> **[yiduobo的每日leetcode 257.二叉树的所有路径](https://zhuanlan.zhihu.com/p/150993879) · 知乎 · 2020-06-27 · 赞同 0**
> 力扣：[257. 二叉树的所有路径](https://leetcode.cn/problems/binary-tree-paths/) · Easy · 灵茶山艾府：[两种写法：路径为参数 / 回溯（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

257.二叉树的所有路径<https://leetcode-cn.com/problems/binary-tree-paths/>

对于树中任意节点：

1、若该节点是叶子节点，那么直接返回该节点。

2、若该节点不是叶子节点，那么递归求解其左孩子与右孩子的所有路径，然后将该节点添加到左孩子与右孩子的所有路径中即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def binaryTreePaths(self, root):
        """
        :type root: TreeNode
        :rtype: List[str]
        """

        if not root:
            return []

        res = []
        return self.dfs(root)

    def dfs(self, now):
        left_res = right_res = []
        if now.left:
            left_res = self.dfs(now.left)
        if now.right:
            right_res = self.dfs(now.right)

        res = ["%d->" % now.val + x for x in left_res] + ["%d->" % now.val + x for x in right_res]
        if not res:
            res = [str(now.val)]

        return res
```
