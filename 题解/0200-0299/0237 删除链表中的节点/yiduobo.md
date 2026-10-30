---
title: "237. 删除链表中的节点"
aliases: ["yiduobo的每日leetcode 237.删除链表中的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150601818"
zhihu_id: "150601818"
zhihu_title: "yiduobo的每日leetcode 237.删除链表中的节点"
question_id: "237"
question: "删除链表中的节点"
problem_url: "https://leetcode.cn/problems/delete-node-in-a-linked-list/"
difficulty: "Medium"
created: "2020-06-24T23:13:20+08:00"
updated: "2020-06-24T23:13:20+08:00"
upvotes: 0
comments: 1
---

# 237. 删除链表中的节点

> **[yiduobo的每日leetcode 237.删除链表中的节点](https://zhuanlan.zhihu.com/p/150601818) · 知乎 · 2020-06-24 · 赞同 0**
> 力扣：[237. 删除链表中的节点](https://leetcode.cn/problems/delete-node-in-a-linked-list/) · Medium · 灵茶山艾府：[脑筋急转弯+简洁写法（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

237.删除链表中的节点<https://leetcode-cn.com/problems/delete-node-in-a-linked-list/>

题目要求删除链表中给定的节点node，但是并没有给出上一个节点，于是经典的prev->next \= prev->next->next的写法就不能使用了。

注意到题目保证了给出的节点不是链表中的最后一个节点，于是在这里可以将node->next的值赋给node，然后删去node->next，就相当于变相地删去了node节点。

具体实现也很简单：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """

        node.val = node.next.val
        node.next = node.next.next
```
