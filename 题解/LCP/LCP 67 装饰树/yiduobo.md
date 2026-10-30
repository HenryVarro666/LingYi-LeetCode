---
title: "LCP 67. 装饰树"
aliases: ["yiduobo的每日leetcode LCP67.装饰树"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/binary-tree", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580212630"
zhihu_id: "580212630"
zhihu_title: "yiduobo的每日leetcode LCP67.装饰树"
question_id: "LCP 67"
question: "装饰树"
problem_url: "https://leetcode.cn/problems/KnLfVT/"
difficulty: "Medium"
created: "2022-11-03T23:06:58+08:00"
updated: "2022-11-03T23:06:58+08:00"
upvotes: 0
comments: 0
---

# LCP 67. 装饰树

> **[yiduobo的每日leetcode LCP67.装饰树](https://zhuanlan.zhihu.com/p/580212630) · 知乎 · 2022-11-03 · 赞同 0**
> 力扣：[LCP 67. 装饰树](https://leetcode.cn/problems/KnLfVT/) · Medium · 灵茶山艾府：[极简写法：调用自身](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP67.装饰树

[力扣](https://leetcode.cn/problems/KnLfVT/description/)

题目要求在树中的每一组父子节点中间都插入一个值为-1的节点，那么只需从根节点向下dfs。对于当前节点now，若now.left非空，那么递归求解now.left，然后构造一个值为-1的节点node，将node.left置为now.left，然后将now.left置为node即可。对于now.right也是类似的处理方法。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def expandBinaryTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: Optional[TreeNode]
        """

        def dfs(now):
            if now.left:
                node = TreeNode(-1)
                dfs(now.left)
                node.left = now.left
                now.left = node
            
            if now.right:
                node = TreeNode(-1)
                dfs(now.right)
                node.right = now.right
                now.right = node
        
        dfs(root)
        return root
```
