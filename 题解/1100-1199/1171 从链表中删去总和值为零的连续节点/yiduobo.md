---
title: "1171. 从链表中删去总和值为零的连续节点"
aliases: ["yiduobo的每日leetcode 1171.从链表中删去总和值为零的连续节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379362098"
zhihu_id: "379362098"
zhihu_title: "yiduobo的每日leetcode 1171.从链表中删去总和值为零的连续节点"
question_id: "1171"
question: "从链表中删去总和值为零的连续节点"
problem_url: "https://leetcode.cn/problems/remove-zero-sum-consecutive-nodes-from-linked-list/"
created: "2021-06-09T23:41:36+08:00"
updated: "2021-06-09T23:41:36+08:00"
upvotes: 0
comments: 0
---

# 1171. 从链表中删去总和值为零的连续节点

> **[yiduobo的每日leetcode 1171.从链表中删去总和值为零的连续节点](https://zhuanlan.zhihu.com/p/379362098) · 知乎 · 2021-06-09 · 赞同 0**
> 力扣：[1171. 从链表中删去总和值为零的连续节点](https://leetcode.cn/problems/remove-zero-sum-consecutive-nodes-from-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1171.从链表中删去总和值为零的连续节点

[力扣](https://leetcode-cn.com/problems/remove-zero-sum-consecutive-nodes-from-linked-list/)

题目要求删去链表中子段和为零的节点，那么对于子段和问题，第一想法就是将其转化成前缀和来解决。值得注意的是，题目并没有要求删去节点之后链表最短，而只是需要删到不能继续删位置。

不妨设我们处理到节点p时的前缀和为s，一种可行的做法就是找到s最后一次出现时对应的节点q，那么p + 1到q之间所有的节点之和恰好为0，我们可以将这些节点全部删去，于是此时将p的next指向q的next，然后继续向后处理即可。

为了求出s最后一次出现的位置，我们则需要先遍历一趟链表，使用一个dict来储存当前前缀和s对应的最后一个节点的位置。

得到dict之后，再从头开始进行一趟遍历，按上面所说的做法调整next的指向即可。

需要注意的是，由于当前链表的头结点也可能被删去，那么我们需要设立一个假头p_head指向head，其值为0，然后从p_head开始进行遍历。

最后附上python代码：

```
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def removeZeroSumSublists(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        p_head = ListNode(0)
        p_head.next = head
        now = p_head
        s = 0
        pos_dict = {}
        while now:
            s += now.val
            pos_dict[s] = now
            now = now.next
        
        now = p_head
        s = 0
        while now:
            s += now.val
            now.next = pos_dict[s].next
            now = now.next

        return p_head.next
```
