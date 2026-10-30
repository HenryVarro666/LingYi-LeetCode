---
title: "83. 删除排序链表中的重复元素"
aliases: ["yiduobo的每日leetcode 83.删除排序链表中的重复元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/linked-list", "leetcode/bian-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134174578"
zhihu_id: "134174578"
zhihu_title: "yiduobo的每日leetcode 83.删除排序链表中的重复元素"
question_id: "83"
question: "删除排序链表中的重复元素"
problem_url: "https://leetcode.cn/problems/remove-duplicates-from-sorted-list/"
difficulty: "Easy"
created: "2020-04-22T21:43:19+08:00"
updated: "2020-04-22T21:43:19+08:00"
upvotes: 0
comments: 0
---

# 83. 删除排序链表中的重复元素

> **[yiduobo的每日leetcode 83.删除排序链表中的重复元素](https://zhuanlan.zhihu.com/p/134174578) · 知乎 · 2020-04-22 · 赞同 0**
> 力扣：[83. 删除排序链表中的重复元素](https://leetcode.cn/problems/remove-duplicates-from-sorted-list/) · Easy · 灵茶山艾府：[【视频】如何去重？一个视频讲透！附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

83.删除排序链表中的重复元素<https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list/>

还是链表操作的题目，不过这里是只保留住一个。对于一个节点p，若p.val \=\= p.next.val那么需要删去p.next这个节点。

链表操作中删除next的经典操作是将p.next指向p.next.next。

最后附上python代码：

```
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head:
            return head
            
        now = head
        while now.next:
            if now.next.val == now.val:
                now.next = now.next.next
            else:
                now = now.next

        return head
```
