---
title: "2095. 删除链表的中间节点"
aliases: ["yiduobo的每日leetcode 2095.删除链表的中间节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/520548108"
zhihu_id: "520548108"
zhihu_title: "yiduobo的每日leetcode 2095.删除链表的中间节点"
question_id: "2095"
question: "删除链表的中间节点"
problem_url: "https://leetcode.cn/problems/delete-the-middle-node-of-a-linked-list/"
difficulty: "Medium"
created: "2022-05-27T01:07:53+08:00"
updated: "2022-05-27T01:07:53+08:00"
upvotes: 0
comments: 0
---

# 2095. 删除链表的中间节点

> **[yiduobo的每日leetcode 2095.删除链表的中间节点](https://zhuanlan.zhihu.com/p/520548108) · 知乎 · 2022-05-27 · 赞同 0**
> 力扣：[2095. 删除链表的中间节点](https://leetcode.cn/problems/delete-the-middle-node-of-a-linked-list/) · Medium · 灵茶山艾府：[龟兔赛跑（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2095.删除链表的中间节点

[力扣](https://leetcode.cn/problems/delete-the-middle-node-of-a-linked-list/)

非常经典的链表操作问题，常规的做法是利用快慢指针来找中心节点。

首先按惯例为链表设置一个假头p_head，并将p_head的next指向真正的head，然后使用两个指针fast和slow，从p_head开始向后移动，fast每一轮移动两步，slow每一轮移动一步。

当某一时刻fast无法继续向后移动时，此时的两个指针移动的轮次都是n / 2，这里的n为链表的长度。也就是说，此时的slow移动了n / 2轮，恰好位于链表中第n / 2 - 1个节点，而答案要求移除的是第n / 2个节点，那么只需要将slow的next指向slow的next的next即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def deleteMiddle(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        p_head = ListNode()
        p_head.next = head

        slow = fast = p_head
        while fast.next and fast.next.next:
            fast = fast.next.next
            slow = slow.next
        
        slow.next = slow.next.next
        return p_head.next
```
