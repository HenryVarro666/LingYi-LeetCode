---
title: "19. 删除链表的倒数第N个节点"
aliases: ["yiduobo的每日leetcode 19.删除链表的倒数第N个节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115363951"
zhihu_id: "115363951"
zhihu_title: "yiduobo的每日leetcode 19.删除链表的倒数第N个节点"
question_id: "19"
question: "删除链表的倒数第 N 个结点"
problem_url: "https://leetcode.cn/problems/remove-nth-node-from-end-of-list/"
difficulty: "Medium"
created: "2020-03-22T23:44:48+08:00"
updated: "2020-03-22T23:44:48+08:00"
upvotes: 0
comments: 0
---

# 19. 删除链表的倒数第N个节点

> **[yiduobo的每日leetcode 19.删除链表的倒数第N个节点](https://zhuanlan.zhihu.com/p/115363951) · 知乎 · 2020-03-22 · 赞同 0**
> 力扣：[19. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/) · Medium · 灵茶山艾府：[【视频讲解】前后指针，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

19.删除链表的倒数第N个节点<https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/>

链表操作的题目。链表位置相关的问题的一个经典处理方法就是双指针法，简单来说就是一个从头开始正常走，另一个按特定的方法走，当一个走到头时另一个就是要找的节点。

这里倒数第N个节点的处理方法是left指针从头开始，然后right指针先往后走N位。接下来left和right同时一位一位往后走，当right走到末尾时，left就是倒数第N个节点了。

另外需要注意的是，题目是要求删除这个节点，这样对于头或者尾，就需要进行特殊处理，其他的情况直接将要删除节点左侧的next指向next.next即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """

        left = head
        right = head 
        for index in range(n - 1):
            right = right.next

        if right.next is None:
            return head.next
        else:
            n_father = head
            while right.next is not None:
                n_father = left
                left = left.next
                right = right.next

            n_father.next = n_father.next.next
            return head
```
