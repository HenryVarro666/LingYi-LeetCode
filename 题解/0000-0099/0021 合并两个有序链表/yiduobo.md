---
title: "21. 合并两个有序链表"
aliases: ["yiduobo的每日leetcode 21.合并两个有序链表"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115643550"
zhihu_id: "115643550"
zhihu_title: "yiduobo的每日leetcode 21.合并两个有序链表"
question_id: "21"
question: "合并两个有序链表"
problem_url: "https://leetcode.cn/problems/merge-two-sorted-lists/"
difficulty: "Easy"
created: "2020-03-23T22:38:40+08:00"
updated: "2020-03-23T22:38:40+08:00"
upvotes: 0
comments: 0
---

# 21. 合并两个有序链表

> **[yiduobo的每日leetcode 21.合并两个有序链表](https://zhuanlan.zhihu.com/p/115643550) · 知乎 · 2020-03-23 · 赞同 0**
> 力扣：[21. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/) · Easy · 灵茶山艾府：[两种方法：迭代（尾插法）/ 递归（头插法）Python/Java/C++/C/Go/JS/Rust](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

21.合并两个有序链表<https://leetcode-cn.com/problems/merge-two-sorted-lists/>

经典的二路归并，归并排序中就是这个思路，区别是这个题目是在链表上完成的，所以可以想象成对于l1中的每一个节点，找到l2中有哪些节点比这个l1中的节点要小，然后将这些节点插到l1中节点的前面，然后依次往后处理l1中的每一个节点即可。如果l1都处理完了，l2中还有节点的话，说明l2中剩余的节点是大于l1中最后一个节点的，此时将剩下的节点接在l1的屁股上就行了。

另外需要特别注意插到l1的头部这种特殊情况，为了简单起见，增加一个假头head指向l1的头部，然后在最后返回的时候返回head.next。增加链表头在链表的问题中是非常实用的操作。

由于l1和l2中的节点都至多遍历依次，因此最终的时间复杂度为O(m + n）。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        head = ListNode(0)
        head.next = l1

        now = head

        while now.next is not None:
            while l2 is not None and l2.val < now.next.val:
                tmp = l2.next
                l2.next = now.next
                now.next = l2
                now = l2
                l2 = tmp
            now = now.next

        if l2 is not None:
            now.next = l2

        return head.next
```
