---
title: "203. 移除链表元素"
aliases: ["yiduobo的每日leetcode 203.移除链表元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146539498"
zhihu_id: "146539498"
zhihu_title: "yiduobo的每日leetcode 203.移除链表元素"
question_id: "203"
question: "移除链表元素"
problem_url: "https://leetcode.cn/problems/remove-linked-list-elements/"
difficulty: "Easy"
created: "2020-06-07T23:03:30+08:00"
updated: "2020-06-07T23:03:30+08:00"
upvotes: 0
comments: 0
---

# 203. 移除链表元素

> **[yiduobo的每日leetcode 203.移除链表元素](https://zhuanlan.zhihu.com/p/146539498) · 知乎 · 2020-06-07 · 赞同 0**
> 力扣：[203. 移除链表元素](https://leetcode.cn/problems/remove-linked-list-elements/) · Easy · 灵茶山艾府：[【套路】如何优雅地删除链表节点？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

203.移除链表元素<https://leetcode-cn.com/problems/remove-linked-list-elements/>

基础的链表操作题目。方便起见还是弄一个假头p_head指向head，然后从p_head开始往后扫描。若now.next.val等于val，那么需要删去now.next，于是有now.next \= now.next.next，否则就将now移动到now.next继续检测即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def removeElements(self, head, val):
        """
        :type head: ListNode
        :type val: int
        :rtype: ListNode
        """

        p_head = ListNode(0)
        p_head.next = head

        now = p_head
        while now.next:
            if now.next.val == val:
                now.next = now.next.next
            else:
                now = now.next

        return p_head.next
```
