---
title: "95. 不同的二叉搜索树II"
aliases: ["yiduobo的每日leetcode 95.不同的二叉搜索树II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137083830"
zhihu_id: "137083830"
zhihu_title: "yiduobo的每日leetcode 95.不同的二叉搜索树II"
question_id: "95"
question: "不同的二叉搜索树II"
problem_url: "https://leetcode.cn/problems/unique-binary-search-trees-ii/"
created: "2020-04-28T23:04:19+08:00"
updated: "2020-04-28T23:04:19+08:00"
upvotes: 0
comments: 0
---

# 95. 不同的二叉搜索树II

> **[yiduobo的每日leetcode 95.不同的二叉搜索树II](https://zhuanlan.zhihu.com/p/137083830) · 知乎 · 2020-04-28 · 赞同 0**
> 力扣：[95. 不同的二叉搜索树II](https://leetcode.cn/problems/unique-binary-search-trees-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

95.不同的二叉搜索树II <https://leetcode-cn.com/problems/unique-binary-search-trees-ii/>

经典的分治题。

对于一颗节点编号为left到right的树，枚举root节点，然后分别用left到root - 1和root + 1到right构造左右子树，最后将所有可能的左右子树与root组合起来即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def generateTrees(self, n):
        """
        :type n: int
        :rtype: List[TreeNode]
        """
        if n == 0:
            return []
        
        return self.dfs(1, n)

    def dfs(self, left, right):
        if left > right:
            return [None]

        f = []
        for root in range(left, right + 1):
            left_res = self.dfs(left, root - 1)
            right_res = self.dfs(root + 1, right)
            for left_tree in left_res:
                for right_tree in right_res:
                    tmp = TreeNode(root)
                    tmp.left = left_tree
                    tmp.right = right_tree
                    f.append(tmp)

        return f
```
