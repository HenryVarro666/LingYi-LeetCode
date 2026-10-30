---
title: "876. 链表的中间节点"
aliases: ["yiduobo的每日leetcode 876.链表的中间节点"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/linked-list", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350564510"
zhihu_id: "350564510"
zhihu_title: "yiduobo的每日leetcode 876.链表的中间节点"
question_id: "876"
question: "链表的中间结点"
problem_url: "https://leetcode.cn/problems/middle-of-the-linked-list/"
difficulty: "Easy"
created: "2021-02-15T23:21:23+08:00"
updated: "2021-02-15T23:21:23+08:00"
upvotes: 0
comments: 0
---

# 876. 链表的中间节点

> **[yiduobo的每日leetcode 876.链表的中间节点](https://zhuanlan.zhihu.com/p/350564510) · 知乎 · 2021-02-15 · 赞同 0**
> 力扣：[876. 链表的中间结点](https://leetcode.cn/problems/middle-of-the-linked-list/) · Easy · 灵茶山艾府：[龟兔赛跑（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

876.链表的中间节点

[力扣](https://leetcode-cn.com/problems/middle-of-the-linked-list/)

经典的链表问题，一个自然的想法是先遍历一趟链表，计算出其长度l，然后从头开始往后走l/2步。这个做法需要进行两次遍历。

另一个经典的做法是维护一组快慢指针，其中快指针每轮往后走两个节点，而慢指针则是往后走一个节点，那么当快指针在走到链表末尾时，慢指针就恰好走到中间节点了。相比于上面的做法，这个做法只需要进行一次遍历。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def middleNode(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        phead = ListNode(0)
        phead.next = head
        one_step = two_step = phead
        while True:
            one_step = one_step.next
            if two_step.next is None or two_step.next.next is None:
                break
            two_step = two_step.next.next

        return one_step
```
