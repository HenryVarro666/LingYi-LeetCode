---
title: "143. 重排链表"
aliases: ["yiduobo的每日leetcode 143.重排链表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142418126"
zhihu_id: "142418126"
zhihu_title: "yiduobo的每日leetcode 143.重排链表"
question_id: "143"
question: "重排链表"
problem_url: "https://leetcode.cn/problems/reorder-list/"
difficulty: "Medium"
created: "2020-05-20T23:46:02+08:00"
updated: "2020-05-20T23:46:02+08:00"
upvotes: 1
comments: 0
---

# 143. 重排链表

> **[yiduobo的每日leetcode 143.重排链表](https://zhuanlan.zhihu.com/p/142418126) · 知乎 · 2020-05-20 · 赞同 1**
> 力扣：[143. 重排链表](https://leetcode.cn/problems/reorder-list/) · Medium · 灵茶山艾府：[【视频】没想明白？一个视频讲透！（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

143.重排链表<https://leetcode-cn.com/problems/reorder-list/>

这算是链表题中的缝合怪。

首先，可以利用快慢指针找出链表的后半部分，接下来将后半部分翻转，最后，将前半部分与后半部分合并即可。

当然，也可以使用dfs来做。首先递归到链表的末尾，然后将头结点head与当前结点tail接在用作答案后面，接下来回溯时将head往后移动一位，回溯后当前节点tail自然也往前移动了一位，将head与tail接在答案后面然后继续回溯即可，停止条件是head与tail相遇。

我在这里采用的是第一种方法，需要注意的是快慢指针需要先设置假头p_head，然后fast与slow同时从p_head开始往后走，才能正确定位到前半部分与后半部分的分界点。另外，对于链表长度为奇数的情况，可以判断通过fast的next是否存在来得知。当链表长度为奇数时，最中间的节点是划在前半部分的，因此要将此时的slow往后移动一位。接下来，翻转与合并都是常规操作，这里就不再赘述了。

最后附上python代码，三段while分别代表了找后半段，翻转以及合并：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reorderList(self, head):
        """
        :type head: ListNode
        :rtype: None Do not return anything, modify head in-place instead.
        """

        if not head or not head.next:
            return

        p_head = ListNode()
        p_head.next = head

        fast = slow = p_head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        if fast.next:
            slow = slow.next

        pre = slow.next
        now = pre.next
        while now:
            tmp = now.next
            now.next = pre
            pre = now
            now = tmp
        slow.next.next = None
        slow.next = None

        now = head
        while pre:
            next1 = now.next
            now.next = pre
            next2 = pre.next
            pre.next = next1
            now = next1
            pre = next2
```
