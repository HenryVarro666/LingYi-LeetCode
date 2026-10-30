---
title: "426. 将二叉搜索树转化为排序的双向链表"
aliases: ["yiduobo的每日leetcode 426.将二叉搜索树转化为排序的双向链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599326756"
zhihu_id: "599326756"
zhihu_title: "yiduobo的每日leetcode 426.将二叉搜索树转化为排序的双向链表"
question_id: "426"
question: "将二叉搜索树转化为排序的双向链表"
problem_url: "https://leetcode.cn/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/"
created: "2023-01-16T04:14:25+08:00"
updated: "2023-01-16T04:14:25+08:00"
upvotes: 0
comments: 0
---

# 426. 将二叉搜索树转化为排序的双向链表

> **[yiduobo的每日leetcode 426.将二叉搜索树转化为排序的双向链表](https://zhuanlan.zhihu.com/p/599326756) · 知乎 · 2023-01-16 · 赞同 0**
> 力扣：[426. 将二叉搜索树转化为排序的双向链表](https://leetcode.cn/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

426.将二叉搜索树转化为排序的双向链表

[力扣](https://leetcode.cn/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/)

题目要求最终结果是排好序的，那么在这里就需要对二叉搜索树进行中序遍历，这样得到的序列才是排好序的。

为了构造链表，在遍历的过程中就需要一个变量prev记录上一个遍历到的节点。每遍历到一个节点now，若prev非空，就都应该对prev和now之间建立双向的连接，同时将prev置为now然后继续进行中序遍历。

由于题目需要返还链表中值最小的节点，因此需要使用一个遍历记录这个节点，其在二叉搜索树中对应的节点应该是中序遍历过程中首次触及的叶子节点，而这个时机恰好就是prev为空的这一轮，因为在此之后prev都会记录上一轮遍历到的节点，这也就意味着当前遍历到的节点并非是最左侧的节点了。

中序遍历完成后，还需要在最终的prev和first之间建立双向的连接，然后返还first作为最终答案。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
"""

class Solution(object):
    def treeToDoublyList(self, root):
        """
        :type root: Node
        :rtype: Node
        """

        if not root:
            return None

        global first, prev
        first = None
        prev = None

        def dfs(now):
            global first, prev
            if now.left:
                dfs(now.left)
            
            if first is None:
                first = now
            else:
                now.left = prev
                prev.right = now

            prev = now
            if now.right:
                dfs(now.right)

        dfs(root)
        
        first.left = prev
        prev.right = first

        return first
```
