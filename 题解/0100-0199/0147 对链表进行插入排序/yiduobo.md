---
title: "147. 对链表进行插入排序"
aliases: ["yiduobo的每日leetcode 147.对链表进行插入排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142919563"
zhihu_id: "142919563"
zhihu_title: "yiduobo的每日leetcode 147.对链表进行插入排序"
question_id: "147"
question: "对链表进行插入排序"
problem_url: "https://leetcode.cn/problems/insertion-sort-list/"
created: "2020-05-22T21:40:37+08:00"
updated: "2020-05-22T21:40:37+08:00"
upvotes: 0
comments: 0
---

# 147. 对链表进行插入排序

> **[yiduobo的每日leetcode 147.对链表进行插入排序](https://zhuanlan.zhihu.com/p/142919563) · 知乎 · 2020-05-22 · 赞同 0**
> 力扣：[147. 对链表进行插入排序](https://leetcode.cn/problems/insertion-sort-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

147.对链表进行插入排序<https://leetcode-cn.com/problems/insertion-sort-list/>

题目的动画做得还算形象，就按着这个来实现即可。方便起见，还是设置一个假头p_head放在链表的最前面。

使用指针now从头往后扫描：

1、如果now.val大于等于当前已经排好的部分的最后一个节点tail.val，那么说明now已经在正确的位置上了，此时将now与tail同时往后移动即可。

2、否则，从假头p_head开始往后扫描，找到第一个满足条件p.next.val >\= now.val。此时，我们将now插入到p与p.next之间即可。插入完毕后我们不需要移动tail，但是需要移动now，因此在插入时需要先将now的next保存下来，正好此时tail.next应该指向到now.next，于是先有tail.next \= now.next，然后在now插入完毕后再执行now \= tail.next往后移动now即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def insertionSortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head or not head.next:
            return head

        p_head = ListNode(0)
        p_head.next = head
        now = head.next
        tail = head
        while now:
            if now.val >= tail.val:
                tail = tail.next
                now = now.next
            else:
                tmp = p_head
                while tmp.next != now and tmp.next.val < now.val:
                    tmp = tmp.next

                tail.next = now.next
                now.next = tmp.next
                tmp.next = now
                now = tail.next

        return p_head.next
```
