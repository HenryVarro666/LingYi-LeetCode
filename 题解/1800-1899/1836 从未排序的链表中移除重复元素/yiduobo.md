---
title: "1836. 从未排序的链表中移除重复元素"
aliases: ["yiduobo的每日leetcode 1836.从未排序的链表中移除重复元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622077452"
zhihu_id: "622077452"
zhihu_title: "yiduobo的每日leetcode 1836.从未排序的链表中移除重复元素"
question_id: "1836"
question: "从未排序的链表中移除重复元素"
problem_url: "https://leetcode.cn/problems/remove-duplicates-from-an-unsorted-linked-list/"
created: "2023-04-15T03:37:01+08:00"
updated: "2023-04-15T03:37:01+08:00"
upvotes: 0
comments: 0
---

# 1836. 从未排序的链表中移除重复元素

> **[yiduobo的每日leetcode 1836.从未排序的链表中移除重复元素](https://zhuanlan.zhihu.com/p/622077452) · 知乎 · 2023-04-15 · 赞同 0**
> 力扣：[1836. 从未排序的链表中移除重复元素](https://leetcode.cn/problems/remove-duplicates-from-an-unsorted-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1836.从未排序的链表中移除重复元素

[力扣](https://leetcode.cn/problems/remove-duplicates-from-an-unsorted-linked-list/)

本题要求删除链表中出现的重复元素，但是不经过一趟遍历，是无法得知某个节点是否出现过多次，如果想要通过一趟遍历就完成删除操作，就需要想办法确定重复元素第一次在链表中出现的位置，同时想办法将其删除，于是最直观的思路就是使用哈希表记录每种元素值第一次出现位置的前置节点。在这里记录前置节点的理由是删除某个节点的操作实际上是通过其前置节点来完成的。

设这个记录前置节点的哈希表为prev，由于哈希表记录的是前置节点，那么在这里就必须添加一个假头节点p_head，用来适配删除链表头部节点。从p_head开始向后遍历链表，对于当前节点now：

1、若now不存在next：

那么说明来到了链表尾部，此时直接返回p_head.next即可

2、若now.next.val没有在prev中出现过：

说明now.next是首次出现在链表中，此时就应该记录prev[now.next.val]为now，然后将now向后移动

3、若now.next.val在prev中出现过，且now.next.val首次出现的节点已经在之前的操作中被删除：

此时只需将now.next删除即可，也就是将now.next置为now.next.next

在这里为了方便判断now.next.val首次出现的节点是否以及被处理过，可以约定被处理过的节点对应的prev值为None，也就是这种情况的前提是prev[now.next.val] \= None

4、若now.next.val在prev中出现过，且now.next.val首次出现的节点还没有被删除，也就是prev[now.next.val]不等于None。记prev[now.next.val].next为remove_target，也就是待移除的目标，那么此时又有两种情况：

4-1）remove_target就是now：

此时移除的目标实际上就是now以及now.next，但是需要将now向前移动，因此需要想将now置为prev[now.next.val]，然后将now.next置为now.next.next.next，表示删除中间这两个节点

4-2）remove_target不是now：

此时可以放心删除remove_target，不过需要注意的是当remove_target被删除后，其下一个节点的prev就从remove_target变成了remove_target的前置节点，因此需要先将prev[remove_target.next.val]置为prev[now.next.val]。

接下来只需将remove_target以及now.next从链表中删除即可，也就是prev[remove_target.next.val].next \= remove_target.next，然后now.next \= now.next.next

另外，无论是4-1还是4-2，在删除操作完成后都已经将remove_target删除，因此需要将prev[remove_target.val]置为None，表示remove_target.val首次出现的节点以及被处理过

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def deleteDuplicatesUnsorted(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        prev = {}
        p_head = ListNode()
        p_head.next = head

        now = p_head
        while now.next:
            if now.next.val not in prev:
                prev[now.next.val] = now
                now = now.next
            elif prev[now.next.val] is None:
                now.next = now.next.next
            else:
                remove_target = prev[now.next.val].next
                if remove_target == now:
                    now = prev[now.val]
                    now.next = now.next.next.next
                else:
                    prev[remove_target.next.val] = prev[now.next.val]
                    prev[now.next.val].next = remove_target.next
                    now.next = now.next.next
                
                prev[remove_target.val] = None

        return p_head.next
```
