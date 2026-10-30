---
title: "369. 给单链表加一"
aliases: ["yiduobo的每日leetcode 369.给单链表加一"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598383782"
zhihu_id: "598383782"
zhihu_title: "yiduobo的每日leetcode 369.给单链表加一"
question_id: "369"
question: "给单链表加一"
problem_url: "https://leetcode.cn/problems/plus-one-linked-list/"
created: "2023-01-11T22:31:16+08:00"
updated: "2023-01-11T22:31:16+08:00"
upvotes: 0
comments: 0
---

# 369. 给单链表加一

> **[yiduobo的每日leetcode 369.给单链表加一](https://zhuanlan.zhihu.com/p/598383782) · 知乎 · 2023-01-11 · 赞同 0**
> 力扣：[369. 给单链表加一](https://leetcode.cn/problems/plus-one-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

369.给单链表加一

[力扣](https://leetcode.cn/problems/plus-one-linked-list/)

最直观的想法是将链表的最后一个元素加上1，不过在加上1之后可能出现进位的情况，而且是多次连续的进位，那么处理起来就相比麻烦一点了。

可以发现，如果出现进位，那么链表的最后若干个值必然都是9，而进位则会在链表中最后一个不为9的位置停下来。计算完成后，最终的结果就应该是不为9的这一位上的值加上1，而后面所有连续的9都变成0。

根据这个结论，就可以从头开始遍历整个链表，找出最后一个值不为9的节点。

若不存在这样的节点，那么说明链表中全都是9，此时就应该额外添加一个值为1的节点放在链表的头部，然后将原始链表中的节点都置为0。

若找到了这样的节点，那么根据上面的结论，只需将这个节点的值加上1，然后将这个节点后续所有节点的值都置为0即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def plusOne(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        p = None
        now = head
        while now:
            if now.val != 9:
                p = now
            now = now.next
        
        if p is None:
            res = ListNode(val = 1, next = head)
            now = res.next
            while now:
                now.val = 0
                now = now.next
            return res
        else:
            p.val += 1
            now = p.next
            while now:
                now.val = 0
                now = now.next
            return head
```
