---
title: "1669. 合并两个链表"
aliases: ["yiduobo的每日leetcode 1669.合并两个链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/443430164"
zhihu_id: "443430164"
zhihu_title: "yiduobo的每日leetcode 1669.合并两个链表"
question_id: "1669"
question: "合并两个链表"
problem_url: "https://leetcode.cn/problems/merge-in-between-linked-lists/"
created: "2021-12-09T23:53:41+08:00"
updated: "2021-12-09T23:53:41+08:00"
upvotes: 1
comments: 0
---

# 1669. 合并两个链表

> **[yiduobo的每日leetcode 1669.合并两个链表](https://zhuanlan.zhihu.com/p/443430164) · 知乎 · 2021-12-09 · 赞同 1**
> 力扣：[1669. 合并两个链表](https://leetcode.cn/problems/merge-in-between-linked-lists/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1669.合并两个链表

[力扣](https://leetcode-cn.com/problems/merge-in-between-linked-lists/)

很常规的链表操作问题。首先从list1开始向后遍历，找到第a - 1个节点，记为pre_a。接下来从pre_a向后继续走走到第b个节点，记为b。然后将pre_a的next指向list2，然后从pre_a开始向后继续走直到走到list2的尾部，然后将这个末尾节点的next指向b.next即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def mergeInBetween(self, list1, a, b, list2):
        """
        :type list1: ListNode
        :type a: int
        :type b: int
        :type list2: ListNode
        :rtype: ListNode
        """

        cnt = 0
        now = list1
        while cnt < a - 1:
            now = now.next
            cnt += 1
        
        pre_a = now
        while cnt < b:
            now = now.next
            cnt += 1
        
        pre_a.next = list2
        while pre_a.next:
            pre_a = pre_a.next
        
        pre_a.next = now.next
        return list1
```
