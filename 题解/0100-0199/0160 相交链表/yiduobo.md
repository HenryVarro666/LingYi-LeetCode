---
title: "160. 相交链表"
aliases: ["yiduobo的每日leetcode 160.相交链表"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/graph", "leetcode/linked-list", "leetcode/math", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143779524"
zhihu_id: "143779524"
zhihu_title: "yiduobo的每日leetcode 160.相交链表"
question_id: "160"
question: "相交链表"
problem_url: "https://leetcode.cn/problems/intersection-of-two-linked-lists/"
difficulty: "Easy"
created: "2020-05-26T20:18:52+08:00"
updated: "2020-05-26T20:18:52+08:00"
upvotes: 1
comments: 0
---

# 160. 相交链表

> **[yiduobo的每日leetcode 160.相交链表](https://zhuanlan.zhihu.com/p/143779524) · 知乎 · 2020-05-26 · 赞同 1**
> 力扣：[160. 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/) · Easy · 灵茶山艾府：[【图解】一张图秒懂相交链表！（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

中间有几道题需要高贵的vip才能做，于是先跳过。

160.相交链表<https://leetcode-cn.com/problems/intersection-of-two-linked-lists/>

不妨设两条链表list1与list2的长度分别为L1与L2，且L1 >\= L2。若二者相交，设相交后需要从list1走step1步，从list2走step2步，那么一定有step1 - step2 \= L1 - L2。证明也很简单，设相交后链表中还有k个节点，那么(step1 + k) - (step2 + k) \= L1 - L2，即step1 - step2 \= L1 - L2。

于是可以先想办法从list1中走L1 - L2步，然后再从list1的当前节点与list2表头同时往后走，如果能走到同一节点，说明两条链表相交，若能走到链表结尾，则不相交。

那么现在的目标是在list1中先走L1 - L2步，具体做法为：

1、用两个指针p1与p2分别从list1与list2的表头开始往后走，当p2走到list2末尾时，p1还需要走L1 - L2步才能走到list1末尾。

2、此时让p1从当前节点，p2从list1表头开始同时往后走，当p1走到list1末尾时，p2已经在list1中走了L1 - L2步。

3、最后让p1从list2表头，p2从当前节点同时开始往后走，在走的过程中判断二者是否相交或者走到链表结尾即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """

        p1 = headA
        p2 = headB
        while p1 and p2:
            p1 = p1.next
            p2 = p2.next

        if not p1:
            p1 = headB
        else:
            p2 = headA

        while p1 and p2:
            p1 = p1.next
            p2 = p2.next

        if not p1:
            p1 = headB
        else:
            p2 = headA

        while p1 and p2:
            if p1 == p2:
                return p1
            p1 = p1.next
            p2 = p2.next

        return None
```
