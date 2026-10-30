---
title: "92. 反转链表II"
aliases: ["yiduobo的每日leetcode 92.反转链表II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/136817658"
zhihu_id: "136817658"
zhihu_title: "yiduobo的每日leetcode 92.反转链表II"
question_id: "92"
question: "反转链表 II"
problem_url: "https://leetcode.cn/problems/reverse-linked-list-ii/"
difficulty: "Medium"
created: "2020-04-27T23:29:30+08:00"
updated: "2020-04-27T23:29:30+08:00"
upvotes: 0
comments: 0
---

# 92. 反转链表II

> **[yiduobo的每日leetcode 92.反转链表II](https://zhuanlan.zhihu.com/p/136817658) · 知乎 · 2020-04-27 · 赞同 0**
> 力扣：[92. 反转链表 II](https://leetcode.cn/problems/reverse-linked-list-ii/) · Medium · 灵茶山艾府：[【视频讲解】反转链表 O(1) 空间写法（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

92.反转链表II <https://leetcode-cn.com/problems/reverse-linked-list-ii/>

链表操作的题目。

首先，若m等于n，说明只需要翻转一个节点，那么无事发生。

接下来，考察正常的位置m到位置n的翻转。一个链表初始状态如下：

P1 -> P2 -> P3 -> ... -> Pm-1 -> Pm -> ... -> Pn -> Pn+1 -> ...

那么在翻转完成之后，将变成

P1 -> P2 -> P3 -> ... -> Pm-1 -> Pn -> ... -> Pm -> Pn+1 -> ...

由于题目要求一趟扫描完成，因此我们需要先走到Pm的位置，同时需要记录下Pm-1这个节点，因为这是翻转后的头部。这里依然是加入一个假头节点来覆盖住m\=1这种特殊情况。

接下来往后逐个扫描，同时将next反转过来。需要注意的是，当后一个节点的next指向前一个节点后，将丢失后一个节点原始的next，即下一个需要处理的节点，因此也需要先将其记录下来，然后再执行next的反转。

当执行完Pn的next反转之后，记录下来的下一个节点应该是Pn+1。此时Pm-1的next任然是Pm，于是只需要将Pm的next指向Pn+1，即Pm-1.next.next \= Pn+1，然后再将Pm-1的next指向Pn即可。

最后附上python代码，其中left_tail表示Pm-1，now表示当前处理的节点，reverse_head表示now原始的上一个节点，而next_node则表示now原始的下一个节点：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseBetween(self, head, m, n):
        """
        :type head: ListNode
        :type m: int
        :type n: int
        :rtype: ListNode
        """

        if m == n:
            return head

        new_head = ListNode(0)
        new_head.next = head
        now = new_head
        for index in range(m - 1):
            now = now.next
        left_tail = now
        now = now.next
        reverse_head = now
        now = now.next

        for index in range(n - m):
            next_node = now.next
            now.next = reverse_head
            reverse_head = now
            now = next_node

        left_tail.next.next = now
        left_tail.next = reverse_head

        return new_head.next
```
