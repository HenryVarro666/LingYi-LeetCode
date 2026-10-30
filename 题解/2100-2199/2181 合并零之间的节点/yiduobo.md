---
title: "2181. 合并零之间的节点"
aliases: ["yiduobo的每日leetcode 2181.合并零之间的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/535606490"
zhihu_id: "535606490"
zhihu_title: "yiduobo的每日leetcode 2181.合并零之间的节点"
question_id: "2181"
question: "合并零之间的节点"
problem_url: "https://leetcode.cn/problems/merge-nodes-in-between-zeros/"
difficulty: "Medium"
created: "2022-06-29T23:56:41+08:00"
updated: "2022-06-29T23:56:41+08:00"
upvotes: 0
comments: 0
---

# 2181. 合并零之间的节点

> **[yiduobo的每日leetcode 2181.合并零之间的节点](https://zhuanlan.zhihu.com/p/535606490) · 知乎 · 2022-06-29 · 赞同 0**
> 力扣：[2181. 合并零之间的节点](https://leetcode.cn/problems/merge-nodes-in-between-zeros/) · Medium · 灵茶山艾府：[原地做法，O(1) 空间（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2181.合并零之间的节点

[力扣](https://leetcode.cn/problems/merge-nodes-in-between-zeros/)

题目要求将零之间的节点合并到一个节点上，同时去除掉所有的零节点。

由于涉及到删除节点，为了最后处理方便，可以按照常规做法，先设置一个假头节点phead，将phead.next置为head，然后从phead开始向后遍历处理：

1、首先需要找到当前节点now之后的首个值不为零的节点，该节点就是这一轮合并的目标节点，同时在这个过程中移除掉所有值等于零的节点。当然也有一种可能是now之后不存在值不为零的节点，此时返回phead.next即可

2、继续向后遍历，若now存在next，且now.next.val不为零，那么就需要将now.next合并到now中，具体来说就是将now.next.val累加到now.val中，同时将now.next删去。重复这个过程直到now.next为空或者now.next.val等于零

3、此时相当于完成了now这一轮的合并，需要继续执行下一轮合并，那么只需回到步骤1就行了

由于题目保证了链表的最后一个节点为零，因此上述过程必然会在步骤1结束。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def mergeNodes(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        phead = ListNode()
        phead.next = head

        now = phead
        while now.next:
            while now.next and now.next.val == 0:
                now.next = now.next.next
            
            if now.next:
                now = now.next
                while now.next and now.next.val != 0:
                    now.val += now.next.val
                    now.next = now.next.next
        
        return phead.next
```
