---
title: "2046. 给按照绝对值排序的链表排序"
aliases: ["yiduobo的每日leetcode 2046.给按照绝对值排序的链表排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625513739"
zhihu_id: "625513739"
zhihu_title: "yiduobo的每日leetcode 2046.给按照绝对值排序的链表排序"
question_id: "2046"
question: "给按照绝对值排序的链表排序"
problem_url: "https://leetcode.cn/problems/sort-linked-list-already-sorted-using-absolute-values/"
created: "2023-04-28T00:57:48+08:00"
updated: "2023-04-28T00:57:48+08:00"
upvotes: 0
comments: 0
---

# 2046. 给按照绝对值排序的链表排序

> **[yiduobo的每日leetcode 2046.给按照绝对值排序的链表排序](https://zhuanlan.zhihu.com/p/625513739) · 知乎 · 2023-04-28 · 赞同 0**
> 力扣：[2046. 给按照绝对值排序的链表排序](https://leetcode.cn/problems/sort-linked-list-already-sorted-using-absolute-values/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2046.给按照绝对值排序的链表排序

[力扣](https://leetcode.cn/problems/sort-linked-list-already-sorted-using-absolute-values/)

由于题目给出的链表已经按照绝对值排好了序，那么对于链表中的正数而言实际上已经是有序的，那么就只需要将其中的负数项逆序接在链表的头部。于是可以一趟遍历，对于当前遍历到的节点，若节点值为正数，那么就跳过，否则就将这个节点移除，然后拼接在链表的头部，并将链表的头部置为这个节点。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def sortLinkedList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        if not head.next:
            return head
        
        last = head
        now = head.next
        while now:
            if now.val >= 0:
                last = now
                now = now.next
            else:
                last.next = now.next
                now.next = head
                head = now
                now = last.next
        
        return head
```
