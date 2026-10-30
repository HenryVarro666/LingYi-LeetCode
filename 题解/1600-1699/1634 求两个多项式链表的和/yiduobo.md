---
title: "1634. 求两个多项式链表的和"
aliases: ["yiduobo的每日leetcode 1634.求两个多项式链表的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618921194"
zhihu_id: "618921194"
zhihu_title: "yiduobo的每日leetcode 1634.求两个多项式链表的和"
question_id: "1634"
question: "求两个多项式链表的和"
problem_url: "https://leetcode.cn/problems/add-two-polynomials-represented-as-linked-lists/"
created: "2023-04-02T19:34:45+08:00"
updated: "2023-04-02T19:34:45+08:00"
upvotes: 0
comments: 1
---

# 1634. 求两个多项式链表的和

> **[yiduobo的每日leetcode 1634.求两个多项式链表的和](https://zhuanlan.zhihu.com/p/618921194) · 知乎 · 2023-04-02 · 赞同 0**
> 力扣：[1634. 求两个多项式链表的和](https://leetcode.cn/problems/add-two-polynomials-represented-as-linked-lists/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1634.求两个多项式链表的和

[力扣](https://leetcode.cn/problems/add-two-polynomials-represented-as-linked-lists/)

题目给出两个链表，要求根据节点的power字段将这两个链表合并。由于power字段是有序的，因此本题可以参照二路归并的思路，使用两个指针p1和p2分别从两个链表头部开始向后移动。若这两个指针当前指向节点的power相同，那么就构造出系数为p1和p2系数之和的节点，同时将这两个指针都向后移动一位，否则就照抄power较小的那个指针指向的节点，同时只将对应的指针向后移动一位。

需要特别注意的是，若当前构造的节点系数为0，那么就不应该将其加入到答案中，因此在这里可能出现最终结果为空的情况。为了方便处理，在这里可以加入一个假头节点p_head，其next指向最终答案的第一个节点从而应对最终结果为空的情况。

最后附上python代码：

```python
# Definition for polynomial singly-linked list.
# class PolyNode:
#     def __init__(self, x=0, y=0, next=None):
#         self.coefficient = x
#         self.power = y
#         self.next = next

class Solution:
    def addPoly(self, poly1, poly2):
        """
        :type poly1: PolyNode
        :type poly2: PolyNode
        :rtype: PolyNode
        """

        p1 = poly1
        p2 = poly2

        p_head = PolyNode()
        p = p_head

        while p1 and p2:
            if p1.power == p2.power:
                node = PolyNode(p1.coefficient + p2.coefficient, p1.power)
                p1 = p1.next
                p2 = p2.next
            elif p1.power > p2.power:
                node = PolyNode(p1.coefficient, p1.power)
                p1 = p1.next
            else:
                node = PolyNode(p2.coefficient, p2.power)
                p2 = p2.next
            
            if node.coefficient != 0:
                p.next = node
                p = node
        
        while p1:
            node = PolyNode(p1.coefficient, p1.power)
            p.next = node
            p = node
            p1 = p1.next
        
        while p2:
            node = PolyNode(p2.coefficient, p2.power)
            p.next = node
            p = node
            p2 = p2.next

        return p_head.next
```
