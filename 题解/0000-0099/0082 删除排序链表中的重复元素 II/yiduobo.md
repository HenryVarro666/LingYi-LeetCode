---
title: "82. 删除排序链表中的重复元素II"
aliases: ["yiduobo的每日leetcode 82.删除排序链表中的重复元素II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134172172"
zhihu_id: "134172172"
zhihu_title: "yiduobo的每日leetcode 82.删除排序链表中的重复元素II"
question_id: "82"
question: "删除排序链表中的重复元素 II"
problem_url: "https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/"
difficulty: "Medium"
created: "2020-04-22T21:43:04+08:00"
updated: "2020-04-22T21:43:04+08:00"
upvotes: 0
comments: 0
---

# 82. 删除排序链表中的重复元素II

> **[yiduobo的每日leetcode 82.删除排序链表中的重复元素II](https://zhuanlan.zhihu.com/p/134172172) · 知乎 · 2020-04-22 · 赞同 0**
> 力扣：[82. 删除排序链表中的重复元素 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/) · Medium · 灵茶山艾府：[【视频】如何去重？一个视频讲透！附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

82.删除排序链表中的重复元素II <https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list-ii/>

链表操作的题目。

题目要求删去链表中的重复元素，即p.val \=\= p.next.val，那么p和p.next都需要删去，因此我们需要在p的前驱节点就开始考虑，即p.next.val \=\= p.next.next.val，那么需要删去p.next与p.next.next。

于是依然使用经典做法，先在head前加入一个假头new_head，然后

1、首先从new_head开始考虑，设当前节点为now，如果now有next，那么设其为p，否则表示已经走到了链表尾部，操作完成可以返回结果new_head.next了。

2、接下来，如果p有next，且p.val \=\= p.next.val，说明p和p.next是需要删去的，于是我们将p移动到p.next，表示这两个节点需要删去。重复这个步骤，直到p没有next或者p.val !\= p.next.val。

3、接下来我们可以判断，如果now.next还是p，说明p在步骤2中未发生过移动，即从一开始p.val就不等于p.next.val，那么此时p是需要保留在链表中的，因此有now \= p。否则，说明now.next到p之间的所有节点val都相同，需要删去，因此有now \= p.next。在移动完now之后，重新从步骤1开始即可。

由于链表中每个节点只被检测过一次，因此虽然是两重循环，但是最终的时间复杂度为O(n)。

最后附上python代码：

```python
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

        new_head = ListNode(0)
        new_head.next = head

        now = new_head
        while now.next:
            p = now.next
            while p.next and p.next.val == now.next.val:
                p = p.next

            if now.next != p:
                now.next = p.next
            else:
                now = p

        return new_head.next
```
