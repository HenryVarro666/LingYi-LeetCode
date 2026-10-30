---
title: "86. 分隔链表"
aliases: ["yiduobo的每日leetcode 86.分隔链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134181230"
zhihu_id: "134181230"
zhihu_title: "yiduobo的每日leetcode 86.分隔链表"
question_id: "86"
question: "分隔链表"
problem_url: "https://leetcode.cn/problems/partition-list/"
created: "2020-04-24T23:10:15+08:00"
updated: "2020-04-24T23:10:15+08:00"
upvotes: 0
comments: 0
---

# 86. 分隔链表

> **[yiduobo的每日leetcode 86.分隔链表](https://zhuanlan.zhihu.com/p/134181230) · 知乎 · 2020-04-24 · 赞同 0**
> 力扣：[86. 分隔链表](https://leetcode.cn/problems/partition-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

86.分隔链表<https://leetcode-cn.com/problems/partition-list/>

链表操作的题目。

我在这里的做法是设一个left，next指向head，表示小于x的部分，然后设一个right，起始为空，表示大于x的部分。

接下来扫描left_head，若当前节点存在next，且next.val小于x，那么无事发生，继续往后扫描left。否则将next接在right部分，然后继续扫描left。最后将left的next指向right即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def partition(self, head, x):
        """
        :type head: ListNode
        :type x: int
        :rtype: ListNode
        """

        left_head = ListNode(0)
        right_head = ListNode(0)
        left_head.next = head

        left_now = left_head
        right_now = right_head

        while left_now.next:
            if left_now.next.val >= x:
                right_now.next = left_now.next
                right_now = right_now.next
                left_now.next = right_now.next
            else:
                left_now = left_now.next

        left_now.next = right_head.next
        right_now.next = None
        return left_head.next
```
