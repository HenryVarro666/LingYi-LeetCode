---
title: "2130. 链表最大孪生和"
aliases: ["yiduobo的每日leetcode 2130.链表最大孪生和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/two-pointers", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/526725632"
zhihu_id: "526725632"
zhihu_title: "yiduobo的每日leetcode 2130.链表最大孪生和"
question_id: "2130"
question: "链表最大孪生和"
problem_url: "https://leetcode.cn/problems/maximum-twin-sum-of-a-linked-list/"
difficulty: "Medium"
created: "2022-06-10T00:26:26+08:00"
updated: "2022-06-10T00:26:26+08:00"
upvotes: 2
comments: 0
---

# 2130. 链表最大孪生和

> **[yiduobo的每日leetcode 2130.链表最大孪生和](https://zhuanlan.zhihu.com/p/526725632) · 知乎 · 2022-06-10 · 赞同 2**
> 力扣：[2130. 链表最大孪生和](https://leetcode.cn/problems/maximum-twin-sum-of-a-linked-list/) · Medium · 灵茶山艾府：[两种方法：递归 / 找中点+反转右半（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2130.链表最大孪生和

[力扣](https://leetcode.cn/problems/maximum-twin-sum-of-a-linked-list/)

题目对于孪生和的定义是从前往后数和从后往前位置相同的数之和，现在要求找出其中的最大值。最直观的做法当然是一趟遍历，使用数组储存链表中的数，然后两个指针从两端向中间遍历，在过程中计算孪生和并更新答案。

除此之外，也存在空间复杂度O(1)的做法。

对于上面从两端往中间扫的做法，当前主要的困难是链表只能单向遍历，那么一个自然的想法就是将链表的后半部分先反转，然后就可以采用上面的从两端往中间扫的做法了。

对于反转链表则是经典的问题，很早之前应该是有原题的，这里就不展开了。

另外，反转链表只需要反转后半部分，那么就需要找到链表的中心位置。对于这个问题，之前也遇到过，使用快慢指针就可以解决了。

于是现在就有了一种做法：

1、使用快慢指针找到链表的中心位置

2、从中心位置开始向后，将链表的后半部分反转

3、从链表的头和尾同时向中心位置遍历，计算孪生和并更新答案

最后附上python代码，三段代码分别就对应了上面三个步骤：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def pairSum(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: int
        """

        p_head = ListNode()
        p_head.next = head
        fast = slow = p_head
        while slow.next:
            fast = fast.next
            slow = slow.next.next
        
        now = fast.next
        last = None
        while now.next:
            tmp = now.next
            now.next = last
            last = now
            now = tmp
        now.next = last

        left = head
        right = now
        res = 0
        while right:
            res = max(res, left.val + right.val)
            left = left.next
            right = right.next
        
        return res
```
