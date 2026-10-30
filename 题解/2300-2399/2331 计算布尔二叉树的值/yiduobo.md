---
title: "2331. 计算布尔二叉树的值"
aliases: ["yiduobo的每日leetcode 2331.计算布尔二叉树的值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/binary-tree", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558576604"
zhihu_id: "558576604"
zhihu_title: "yiduobo的每日leetcode 2331.计算布尔二叉树的值"
question_id: "2331"
question: "计算布尔二叉树的值"
problem_url: "https://leetcode.cn/problems/evaluate-boolean-binary-tree/"
difficulty: "Easy"
rating: 1304
created: "2022-08-27T22:45:04+08:00"
updated: "2022-08-27T22:45:04+08:00"
upvotes: 0
comments: 0
---

# 2331. 计算布尔二叉树的值

> **[yiduobo的每日leetcode 2331.计算布尔二叉树的值](https://zhuanlan.zhihu.com/p/558576604) · 知乎 · 2022-08-27 · 赞同 0**
> 力扣：[2331. 计算布尔二叉树的值](https://leetcode.cn/problems/evaluate-boolean-binary-tree/) · Easy · 灵茶山艾府：[简洁写法，自身递归](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2331.计算布尔二叉树的值

[力扣](https://leetcode.cn/problems/evaluate-boolean-binary-tree/)

从树的根节点开始递归求解，对于当前节点now：

1、若now是叶子节点，那么根据now.val返回true或者false

2、若now不是叶子节点，那么先递归求解now.left和now.right，然后根据now.val选择与运算或者或运算

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def evaluateTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """

        def dfs(now):
            if now.left:
                if now.val == 2:
                    return dfs(now.left) or dfs(now.right)
                else:
                    return dfs(now.left) and dfs(now.right)
            else:
                return now.val == 1

        return dfs(root)
```
