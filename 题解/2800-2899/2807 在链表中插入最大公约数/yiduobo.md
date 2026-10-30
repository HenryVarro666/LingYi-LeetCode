---
title: "2807. 在链表中插入最大公约数"
aliases: ["yiduobo的每日leetcode 2807.在链表中插入最大公约数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/number-theory", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/一-链表", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657716135"
zhihu_id: "657716135"
zhihu_title: "yiduobo的每日leetcode 2807.在链表中插入最大公约数"
question_id: "2807"
question: "在链表中插入最大公约数"
problem_url: "https://leetcode.cn/problems/insert-greatest-common-divisors-in-linked-list/"
difficulty: "Medium"
rating: 1279
created: "2023-09-22T04:08:39+08:00"
updated: "2023-09-22T04:08:39+08:00"
upvotes: 0
comments: 0
---

# 2807. 在链表中插入最大公约数

> **[yiduobo的每日leetcode 2807.在链表中插入最大公约数](https://zhuanlan.zhihu.com/p/657716135) · 知乎 · 2023-09-22 · 赞同 0**
> 力扣：[2807. 在链表中插入最大公约数](https://leetcode.cn/problems/insert-greatest-common-divisors-in-linked-list/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2807.在链表中插入最大公约数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/insert-greatest-common-divisors-in-linked-list/)

对链表进行一趟遍历，一边遍历一边执行插入操作。

对于当前遍历到的节点now，若now存在后继节点now.next，那么就需要在二者之间插入一个值为gcd(now.val, now.next.val)的新节点node。具体来说，需要先将node.next指向到now.next，然后再将now.next指向到node。

接下来继续向后遍历并重复上面的操作，直到now来到链表末尾为止。需要注意的是每次移动时，当前的now.next已经不是now原先的后继节点，而是新插入的node，因此在这里需要将now置为now.next.next。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def insertGreatestCommonDivisors(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        now = head
        while now.next:
            node = ListNode(gcd(now.val, now.next.val), now.next)
            now.next = node
            now = now.next.next
        
        return head
```
