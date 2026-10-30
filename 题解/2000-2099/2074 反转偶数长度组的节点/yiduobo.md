---
title: "2074. 反转偶数长度组的节点"
aliases: ["yiduobo的每日leetcode 2074.反转偶数长度组的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/516498485"
zhihu_id: "516498485"
zhihu_title: "yiduobo的每日leetcode 2074.反转偶数长度组的节点"
question_id: "2074"
question: "反转偶数长度组的节点"
problem_url: "https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/"
difficulty: "Medium"
created: "2022-05-18T21:02:11+08:00"
updated: "2022-05-18T21:02:11+08:00"
upvotes: 0
comments: 0
---

# 2074. 反转偶数长度组的节点

> **[yiduobo的每日leetcode 2074.反转偶数长度组的节点](https://zhuanlan.zhihu.com/p/516498485) · 知乎 · 2022-05-18 · 赞同 0**
> 力扣：[2074. 反转偶数长度组的节点](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/) · Medium · 灵茶山艾府：[交换元素值的写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2074.反转偶数长度组的节点

[力扣](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/)

经典的反转链表问题，不过在这里需要先对链表进行分组，只翻转其中偶数长度的组。

按照题目1、2、3、4这样的长度变化，看上去很容易判断哪些组应该翻转，但是最后一组的长度可能达不到预期，且在遍历完整个链表前是无从得知其长度的，因此还是需要先遍历，再决定是否反转。

对于常规的反转链表，一般来说有利用栈辅助和直接递归这两种做法。在这里由于必须要先执行遍历，所以我才用了栈辅助的做法，在遍历过程中使用栈储存当前这一组的节点，然后通过栈的长度判断当前组是否需要翻转。如果需要，从栈顶依次弹出节点然后调整next即可。如果不需要翻转，那么将栈清空然后继续向后遍历就行了。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reverseEvenLengthGroups(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        stack = []
        p_head = ListNode()
        p_head.next = head

        now = p_head
        l = 0
        while now.next:
            l += 1
            last = now
            for index in range(l):
                if now.next:
                    stack.append(now.next)
                    now = now.next
                       
            if len(stack) % 2 == 0:
                stack[0].next = now.next
                while stack:
                    last.next = stack[-1]
                    last = last.next
                    stack.pop()

                now = last

            else:
                stack = []
        
        return p_head.next
```
