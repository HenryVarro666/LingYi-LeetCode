---
title: "2674. 拆分循环链表"
aliases: ["yiduobo的每日leetcode 2674.拆分循环链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649318437"
zhihu_id: "649318437"
zhihu_title: "yiduobo的每日leetcode 2674.拆分循环链表"
question_id: "2674"
question: "拆分循环链表"
problem_url: "https://leetcode.cn/problems/split-a-circular-linked-list/"
created: "2023-08-11T02:30:27+08:00"
updated: "2023-08-11T02:30:27+08:00"
upvotes: 0
comments: 0
---

# 2674. 拆分循环链表

> **[yiduobo的每日leetcode 2674.拆分循环链表](https://zhuanlan.zhihu.com/p/649318437) · 知乎 · 2023-08-11 · 赞同 0**
> 力扣：[2674. 拆分循环链表](https://leetcode.cn/problems/split-a-circular-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2674.拆分循环链表

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/split-a-circular-linked-list/description/)

题目要求将循环链表从正中间切成两端，然后将前半段的最后一个节点的next指针指向原链表的头部，将原链表的尾部节点的next指针指向后半段的第一个节点，因此本题实际上就是要找出这中间的两个节点。又因为通过前半段的最后一个节点的next节点可以直接得到后半段的第一个节点，因此只需找出链表正中间的节点就行了。

对于这个问题，一种经典的处理方法是快慢指针。使用两个指针fast和slow分别从链表的第二个节点和链表的头结点开始向后行走，fast每轮走两步，slow每轮走一步，当fast走到无法继续向后走时，slow恰好就来到了链表的正中间。

通过这个方法找到前半段的最后一个节点，也就是当前的slow指向的节点，先将原链表的头节点以及slow的next节点加入到答案数组中，然后将原链表的最后一个节点，即当前的fast指向的节点，将其next节点指向slow的next节点，需要注意此时slow的next节点指向的依然是后半段的头部节点。最后，再将slow的next节点指向原链表的头节点即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def splitCircularLinkedList(self, list):
        """
        :type list: Optional[ListNode]
        :rtype: List[Optional[ListNode]]
        """

        fast = list.next
        slow = list

        while fast.next != list:
            slow = slow.next
            fast = fast.next
            if fast.next != list:
                fast = fast.next

        res = [list, slow.next]
        fast.next = slow.next
        slow.next = list
        return res
```
