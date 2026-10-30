---
title: "61. 旋转链表"
aliases: ["yiduobo的每日leetcode 61.旋转链表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129090039"
zhihu_id: "129090039"
zhihu_title: "yiduobo的每日leetcode 61.旋转链表"
question_id: "61"
question: "旋转链表"
problem_url: "https://leetcode.cn/problems/rotate-list/"
difficulty: "Medium"
created: "2020-04-11T23:10:36+08:00"
updated: "2020-04-11T23:10:36+08:00"
upvotes: 0
comments: 0
---

# 61. 旋转链表

> **[yiduobo的每日leetcode 61.旋转链表](https://zhuanlan.zhihu.com/p/129090039) · 知乎 · 2020-04-11 · 赞同 0**
> 力扣：[61. 旋转链表](https://leetcode.cn/problems/rotate-list/) · Medium · 灵茶山艾府：[首尾相连再断开（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

61.旋转链表<https://leetcode-cn.com/problems/rotate-list/>

链表操作的题目。根据样例2可以发现，长度为l的链表在移动l个位置之后将无事发生，因此最终链表将进行k % l次操作。

不妨将链表尾部的next指向链表头部，将链表当做一个环，那么一次操作就意味着将链表的头部往前移动了一位。于是，题目就相当于将链表的头部往前移动k % l个位置。

当然，这里的单向链表是无法往前移动的，于是可以对应的，往后移动l - (k % l)个位置。找到新的头部之后，将新的尾部与新的头部断开即可。

一次遍历确定链表的长度，并将链表的尾部的next指向链表头部。接下来在一次遍历找到新的头部和新的尾部，断开链接即可。因此最后的时间复杂度为O(l)，l为链表的长度。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def rotateRight(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        if not head:
            return None
        
        if not head.next:
            return head

        now = head
        l = 1
        while now.next:
            now = now.next
            l += 1
        now.next = head

        k %= l
        k = l - k
        now = head
        for index in range(k - 1):
            now = now.next
        head = now.next
        now.next = None
        return head
```
