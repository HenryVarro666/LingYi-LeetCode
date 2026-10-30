---
title: "993. 二叉树的堂兄弟节点"
aliases: ["yiduobo的每日leetcode 993.二叉树的堂兄弟节点"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/depth-first-search", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364932839"
zhihu_id: "364932839"
zhihu_title: "yiduobo的每日leetcode 993.二叉树的堂兄弟节点"
question_id: "993"
question: "二叉树的堂兄弟节点"
problem_url: "https://leetcode.cn/problems/cousins-in-binary-tree/"
difficulty: "Easy"
rating: 1288
created: "2021-04-14T23:32:24+08:00"
updated: "2021-04-14T23:32:24+08:00"
upvotes: 0
comments: 0
---

# 993. 二叉树的堂兄弟节点

> **[yiduobo的每日leetcode 993.二叉树的堂兄弟节点](https://zhuanlan.zhihu.com/p/364932839) · 知乎 · 2021-04-14 · 赞同 0**
> 力扣：[993. 二叉树的堂兄弟节点](https://leetcode.cn/problems/cousins-in-binary-tree/) · Easy · 灵茶山艾府：[DFS+记录深度和父节点（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

993.二叉树的堂兄弟节点

[力扣](https://leetcode-cn.com/problems/cousins-in-binary-tree/)

题目要求判别两个节点是否深度相同且父节点不同，注意到深度相同这一条件，很自然想到利用层序遍历来处理。

首先判断特殊情况，若某个节点是根节点，那么答案显然是false。

接下来开始进行层序遍历，当处理完某一层时，若某个节点已经被处理过：

1、若另一个节点还没有被处理，说明两个节点深度不同，返回false

2、若两个节点的父节点相同，返回false

3、若不满足1和2，那么就返回true

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isCousins(self, root, x, y):
        """
        :type root: TreeNode
        :type x: int
        :type y: int
        :rtype: bool
        """

        if root.val == x or root.val == y:
            return False

        fa_x = fa_y = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            for now in q[l : r]:
                if now.left:
                    q.append(now.left)
                    if now.left.val == x:
                        fa_x = now.val
                    if now.left.val == y:
                        fa_y = now.val
                if now.right:
                    q.append(now.right)
                    if now.right.val == x:
                        fa_x = now.val
                    if now.right.val == y:
                        fa_y = now.val
            
            if fa_x or fa_y:
                return fa_x and fa_y and fa_x != fa_y
            
            l, r = r, len(q)
```
