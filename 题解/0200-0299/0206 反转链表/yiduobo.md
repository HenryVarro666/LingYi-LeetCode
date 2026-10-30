---
title: "206. 反转链表"
aliases: ["yiduobo的每日leetcode 206.反转链表"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146768772"
zhihu_id: "146768772"
zhihu_title: "yiduobo的每日leetcode 206.反转链表"
question_id: "206"
question: "反转链表"
problem_url: "https://leetcode.cn/problems/reverse-linked-list/"
difficulty: "Easy"
created: "2020-06-08T21:36:24+08:00"
updated: "2020-06-08T21:36:24+08:00"
upvotes: 0
comments: 0
---

# 206. 反转链表

> **[yiduobo的每日leetcode 206.反转链表](https://zhuanlan.zhihu.com/p/146768772) · 知乎 · 2020-06-08 · 赞同 0**
> 力扣：[206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/) · Easy · 灵茶山艾府：[两种方法：递归 / 迭代，本质是尾插法和头插法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

206.反转链表<https://leetcode-cn.com/problems/reverse-linked-list/>

基础的链表操作题目。以前写的都是迭代版本的，这里用递归来做一下。

首先检测当前节点now是否拥有next，若没有，说明now是链表的最后一个节点，直接返回即可。若有，那么先递归反转now.next以及之后的部分，返回反转的链表头部new_head。此时now.next就是反转的链表的尾部，因此将now.next.next指向now，将now加入反转后的链表中，然后将now.next指向null即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head:
            return head
        return self.dfs(head)

    def dfs(self, now):
        if not now.next:
            return now
        
        new_head = self.dfs(now.next)
        now.next.next = now
        now.next = None
        return new_head
```
