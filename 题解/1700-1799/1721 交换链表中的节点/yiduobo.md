---
title: "1721. 交换链表中的节点"
aliases: ["yiduobo的每日leetcode 1721.交换链表中的节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451437097"
zhihu_id: "451437097"
zhihu_title: "yiduobo的每日leetcode 1721.交换链表中的节点"
question_id: "1721"
question: "交换链表中的节点"
problem_url: "https://leetcode.cn/problems/swapping-nodes-in-a-linked-list/"
created: "2021-12-29T23:20:54+08:00"
updated: "2021-12-29T23:20:54+08:00"
upvotes: 0
comments: 0
---

# 1721. 交换链表中的节点

> **[yiduobo的每日leetcode 1721.交换链表中的节点](https://zhuanlan.zhihu.com/p/451437097) · 知乎 · 2021-12-29 · 赞同 0**
> 力扣：[1721. 交换链表中的节点](https://leetcode.cn/problems/swapping-nodes-in-a-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1721.交换链表中的节点

[力扣](https://leetcode-cn.com/problems/swapping-nodes-in-a-linked-list/)

题目要求交换单向链表中的第k个节点以及倒数第k个节点，那么必须先知道整个链表的长度l，才能确定倒数第k个节点是什么。

首先一趟遍历确定链表的长度l，那么要交换的就是第k个节点以及第l - k + 1个节点。方便起见在这里默认k \<\= l - k + 1，如果不符合那么可以将k变成l - k + 1，结果是不变的。

由于是单向链表，因此要交换第k个节点以及第l - k + 1个节点，实际上就是要找到第k - 1个节点和第l - k个节点，然后对这两个节点的next进行操作。为了处理k \= 1的这种情况，可以在链表头部加上假头p_head，然后从p_head出发向后找出第k - 1个节点以及第l - k个节点，分别记为p1和p2。

此时需要交换p1和p2的next，那么使用常规的中间变量交换法就好了。

交换完毕后，还需要交换第k个节点以及第l - k + 1个节点的next。此时这两个节点分别就是p1.next和p2.next，那么p1和p2分别向后走一步，然后再次使用中间变量交换法交换二者的next即可。

处理完毕后返回p_head.next即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def swapNodes(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        p_head = ListNode()
        p_head.next = head
        now = p_head
        l = 0
        while now.next:
            now = now.next
            l += 1

        if l & 1 and k == (l + 1) / 2:
            return head
        
        if k > (l + 1) / 2:
            k = l + 1 - k

        cnt1 = k - 1
        cnt2 = l - k
        cnt = 0
        now = p_head
        while now.next:
            if cnt == cnt1:
                p1 = now
            if cnt == cnt2:
                p2 = now
                break
            
            cnt += 1
            now = now.next
        
        tmp = p1.next
        p1.next = p2.next
        p2.next = tmp

        p1 = p1.next
        p2 = p2.next
        tmp = p1.next
        p1.next = p2.next
        p2.next = tmp
        return p_head.next
```
