---
title: "708. 循环有序列表的插入"
aliases: ["yiduobo的每日leetcode 708.循环有序列表的插入"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604355834"
zhihu_id: "604355834"
zhihu_title: "yiduobo的每日leetcode 708.循环有序列表的插入"
question_id: "708"
question: "循环有序列表的插入"
problem_url: "https://leetcode.cn/problems/insert-into-a-sorted-circular-linked-list/"
created: "2023-02-07T23:24:39+08:00"
updated: "2023-02-07T23:24:39+08:00"
upvotes: 0
comments: 0
---

# 708. 循环有序列表的插入

> **[yiduobo的每日leetcode 708.循环有序列表的插入](https://zhuanlan.zhihu.com/p/604355834) · 知乎 · 2023-02-07 · 赞同 0**
> 力扣：[708. 循环有序列表的插入](https://leetcode.cn/problems/insert-into-a-sorted-circular-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

708.循环有序列表的插入

[力扣](https://leetcode.cn/problems/insert-into-a-sorted-circular-linked-list/)

首先考虑边界情况。当链表为空时，新建节点并返回该节点即可。

接下来是一般情况。对于插入的数值insertVal，有以下几种可能：

1、其数值位于两个相邻的节点now和prev之间，即

prev.val \<\= insertVal \<\= now.val

这种情况下，应该将其插入到prev和now之间，也就是新建一个next指向now的节点，其值为insertVal，然后将prev的next指向该节点

2、其数值大于等于链表中的最大值，即

ma.val \<\= insertVal

其中ma为链表中的最大值，即ma.val > ma.next.val

这种情况下，应该将其插入到ma的后面。此时不妨将ma视为prev，ma.next视为now，就可以套用情况1中的操作来完成插入了

3、其数值小于等于链表中的最小值，即

insertVal \<\= mi.val

其中mi为链表中的最小值。设mi的上一个节点为p，那么就有p.val > mi.val

这种情况下，应该将其插入到mi的前面。此时如果将mi的前一个节点视为prev，mi视为now，则同样可以套用情况1中的操作来完成插入。

对于上面这几种情况，就可以从head开始向后遍历直到回到head，期间每一轮操作都记录上一个节点prev以及当前节点now，若出现以上三种情况之一，则可以按照上面的处理方法完成插入操作。

需要特别注意的是，情况2和情况3为了确保当前处理的就是ma或mi，设置的限制条件是严格的大于或小于，但是也可能出现一种情况就是链表中的所有节点值都相等，此时通过情况2和情况3中的限制条件是无法找到ma和mi的。若出现了这种情况，那么now就会走回到head，也就是走完一轮依然没有完成插入操作。对于这种情况，由于链表中所有节点的值都相等，因此随便找个位置将insertVal插入进去就行了。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next
"""

class Solution(object):
    def insert(self, head, insertVal):
        """
        :type head: Node
        :type insertVal: int
        :rtype: Node
        """

        if not head:
            head = Node(insertVal)
            head.next = head
            return head
        
        now = head
        while True:
            prev = now
            now = now.next
            if (prev.val <= insertVal <= now.val) or (now.val < prev.val <= insertVal) or (insertVal <= now.val < prev.val):
                tmp = Node(insertVal, now)
                prev.next = tmp
                return head
        
            if now == head:
                break
        
    
        tmp = Node(insertVal, head.next)
        head.next = tmp
        return head
```
