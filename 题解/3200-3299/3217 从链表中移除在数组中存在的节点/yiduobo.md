---
title: "3217. 从链表中移除数组中存在的节点"
aliases: ["yiduobo的每日leetcode 3217.从链表中移除数组中存在的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719090485"
zhihu_id: "719090485"
zhihu_title: "yiduobo的每日leetcode 3217.从链表中移除数组中存在的节点"
question_id: "3217"
question: "从链表中移除在数组中存在的节点"
problem_url: "https://leetcode.cn/problems/delete-nodes-from-linked-list-present-in-array/"
difficulty: "Medium"
created: "2024-09-09T22:50:14+08:00"
updated: "2024-09-09T22:50:14+08:00"
upvotes: 0
comments: 0
---

# 3217. 从链表中移除数组中存在的节点

> **[yiduobo的每日leetcode 3217.从链表中移除数组中存在的节点](https://zhuanlan.zhihu.com/p/719090485) · 知乎 · 2024-09-09 · 赞同 0**
> 力扣：[3217. 从链表中移除在数组中存在的节点](https://leetcode.cn/problems/delete-nodes-from-linked-list-present-in-array/) · Medium · 灵茶山艾府：[哨兵节点+一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3217.从链表中移除数组中存在的节点

[. - 力扣（LeetCode）](https://leetcode.cn/problems/delete-nodes-from-linked-list-present-in-array/description/)

题目给出一个整数数组nums以及一个链表头head，要求移除链表中所有值在nums中出现过的节点。

首先，为了方便判断链表中的节点的值是否在nums中出现过，可以先将nums转换成一个集合nums_set，接下来就可以通过nums_set高效判断某个值是否出现在nums中出现过了。

另一方面，对于链表中移除节点的操作，一般是通过移除当前节点now的next而不是now自身，理由是移除now后需要将now的上一个节点的next指向当前now.next，需要额外记录上一个节点。而如果移除的是now.next，那么只需将now.next指向到now.next的next，即now.next.next，就相当于将now.next从链表中移除了。

需要注意的是，为了适配这个移除next的操作，则需要额外添加一个假头节点p_head，将其next指向head，然后从p_head开始向后遍历，删除所有值出现在nums_set的节点即可。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def modifiedList(self, nums, head):
        """
        :type nums: List[int]
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        p_head = ListNode()
        p_head.next = head
        nums_set = set(nums)
        p = p_head
        while p.next:
            if p.next.val in nums_set:
                p.next = p.next.next
            else:
                p = p.next
        
        return p_head.next
```
