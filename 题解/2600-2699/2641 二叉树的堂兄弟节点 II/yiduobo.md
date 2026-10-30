---
title: "2641. 二叉树的堂兄弟节点II"
aliases: ["yiduobo的每日leetcode 2641.二叉树的堂兄弟节点II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646651138"
zhihu_id: "646651138"
zhihu_title: "yiduobo的每日leetcode 2641.二叉树的堂兄弟节点II"
question_id: "2641"
question: "二叉树的堂兄弟节点 II"
problem_url: "https://leetcode.cn/problems/cousins-in-binary-tree-ii/"
difficulty: "Medium"
rating: 1677
created: "2023-07-29T03:12:02+08:00"
updated: "2023-07-29T03:12:02+08:00"
upvotes: 0
comments: 0
---

# 2641. 二叉树的堂兄弟节点II

> **[yiduobo的每日leetcode 2641.二叉树的堂兄弟节点II](https://zhuanlan.zhihu.com/p/646651138) · 知乎 · 2023-07-29 · 赞同 0**
> 力扣：[2641. 二叉树的堂兄弟节点 II](https://leetcode.cn/problems/cousins-in-binary-tree-ii/) · Medium · 灵茶山艾府：[BFS+算两次（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2641.二叉树的堂兄弟节点II

[力扣](https://leetcode.cn/problems/cousins-in-binary-tree-ii/)

题目需要将树中每个节点的值替换为其堂兄弟节点值之和，这里的堂兄弟节点值之和可以认为是该节点所在层中所有节点值之和，减去该节点父亲节点的所有子节点之和，于是可以从根节点开始向下进行一次层序遍历，在层序遍历的过程中可以同时将每一层节点值之和以及每个节点的子节点之和都计算好，接下来再进行一次层序遍历，利用第一轮遍历计算出的层和以及父节点的所有子节点之和计算当前节点的最终值即可。

需要特别注意的是，根节点由于没有堂兄弟节点，因此其最终值必然为0，因此遍历时可以直接从根节点的下一层开始执行，在计算完所有节点值之后最后再将根节点值置为0。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def replaceValueInTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: Optional[TreeNode]
        """

        level_s = []
        q = [root]
        sons_s = []
        head, tail = 0, 1
        while head < tail:
            level_s.append(0)
            for index in range(head, tail):
                now = q[index]
                sons_s.append(0)
                level_s[-1] += now.val
                if now.left:
                    sons_s[index] += now.left.val
                    q.append(now.left)
                if now.right:
                    sons_s[index] += now.right.val
                    q.append(now.right)
            
            head, tail = tail, len(q)

        q = [root]
        head, tail = 0, 1
        level = 0
        while head < tail:
            level += 1
            for index in range(head, tail):
                now = q[index]
                if now.left:
                    now.left.val = level_s[level] - sons_s[index]
                    q.append(now.left)
                if now.right:
                    now.right.val = level_s[level] - sons_s[index]
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        root.val = 0
        return root
```
