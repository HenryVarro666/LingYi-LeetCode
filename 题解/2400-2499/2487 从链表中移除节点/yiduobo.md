---
title: "2487. 从链表中移除节点"
aliases: ["yiduobo的每日leetcode 2487.从链表中移除节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589809568"
zhihu_id: "589809568"
zhihu_title: "yiduobo的每日leetcode 2487.从链表中移除节点"
question_id: "2487"
question: "从链表中移除节点"
problem_url: "https://leetcode.cn/problems/remove-nodes-from-linked-list/"
difficulty: "Medium"
created: "2022-12-07T02:14:49+08:00"
updated: "2022-12-07T02:14:49+08:00"
upvotes: 0
comments: 0
---

# 2487. 从链表中移除节点

> **[yiduobo的每日leetcode 2487.从链表中移除节点](https://zhuanlan.zhihu.com/p/589809568) · 知乎 · 2022-12-07 · 赞同 0**
> 力扣：[2487. 从链表中移除节点](https://leetcode.cn/problems/remove-nodes-from-linked-list/) · Medium · 灵茶山艾府：[两种做法：递归 / 迭代（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2487.从链表中移除节点

[力扣](https://leetcode.cn/problems/remove-nodes-from-linked-list/)

从题目给出的样例中可以发现，可能出现某个节点移除了多个前缀节点的情况出现。由于题目给出的是单链表，因此在某个节点被移除后，并不能直接访问到其上一个节点，因此在这里需要使用某种数据结构来进行辅助。根据题目删除节点的顺序，很容易想到使用一个栈来储存当前链表中剩余的节点，那么对于接下来遍历到的节点now，若当前栈不为空，且栈顶节点值小于now.val，那么就将栈顶节点从栈中弹出。重复此过程直到栈为空或者栈顶节点值大于等于now.val为止。接下来将now加入到栈中，然后继续向后处理now.next即可。

遍历完成后，栈中剩余节点就是要求的答案。需要注意的是，此时需要从栈底开始将这些节点串起来。当然，在删除节点后将now加入栈中的的同时将栈顶节点的next指针也是可行的选择，此时直接返回栈顶元素就行了。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def removeNodes(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        stack = []

        now = head
        while now:
            while stack and now.val > stack[-1].val:
                stack.pop()
            
            if stack:
                stack[-1].next = now
            stack.append(now)
            now = now.next
        
        return stack[0]
```
