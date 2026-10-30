---
title: "328. 奇偶链表"
aliases: ["yiduobo的每日leetcode 328.奇偶链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161401293"
zhihu_id: "161401293"
zhihu_title: "yiduobo的每日leetcode 328.奇偶链表"
question_id: "328"
question: "奇偶链表"
problem_url: "https://leetcode.cn/problems/odd-even-linked-list/"
created: "2020-07-18T01:28:16+08:00"
updated: "2020-07-18T01:28:16+08:00"
upvotes: 0
comments: 0
---

# 328. 奇偶链表

> **[yiduobo的每日leetcode 328.奇偶链表](https://zhuanlan.zhihu.com/p/161401293) · 知乎 · 2020-07-18 · 赞同 0**
> 力扣：[328. 奇偶链表](https://leetcode.cn/problems/odd-even-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

328.奇偶链表<https://leetcode-cn.com/problems/odd-even-linked-list/>

比较基础的链表操作题目。两个指针分别指向链表的第一个和第二个节点，设其为odd和even。那么odd的下一个节点应该是第三个节点，即even的下一个节点，于是有

odd->next \= even->next

在此之后我们将odd移动至odd->next，那么此时even的下一个节点应该是第四个节点，即新odd的下一个节点，于是有

even->next \= odd->next

在此之后我们将even移动至even->next，那么情况又相当于变回到初始情况了，于是依次往下做，直至链表结尾。可以发现，无论是奇数长度的链表还是偶数长度的链表，判断链表走到末尾都可以通过判断even->next是否为空来实现。

最后，将整条偶数节点的链表接在奇数节点链表的末尾即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def oddEvenList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        if not head or not head.next or not head.next.next:
            return head

        odd = head
        even = head.next

        now_odd = odd
        now_even = even
        while now_even.next:
            now_odd.next = now_even.next
            now_odd = now_odd.next
            now_even.next = now_odd.next
            if now_even.next:
                now_even = now_even.next

        now_odd.next = even
        return odd
```
