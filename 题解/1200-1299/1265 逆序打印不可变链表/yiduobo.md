---
title: "1265. 逆序打印不可变链表"
aliases: ["yiduobo的每日leetcode 1265.逆序打印不可变链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615298490"
zhihu_id: "615298490"
zhihu_title: "yiduobo的每日leetcode 1265.逆序打印不可变链表"
question_id: "1265"
question: "逆序打印不可变链表"
problem_url: "https://leetcode.cn/problems/print-immutable-linked-list-in-reverse/"
created: "2023-03-19T22:25:33+08:00"
updated: "2023-03-19T22:25:33+08:00"
upvotes: 0
comments: 0
---

# 1265. 逆序打印不可变链表

> **[yiduobo的每日leetcode 1265.逆序打印不可变链表](https://zhuanlan.zhihu.com/p/615298490) · 知乎 · 2023-03-19 · 赞同 0**
> 力扣：[1265. 逆序打印不可变链表](https://leetcode.cn/problems/print-immutable-linked-list-in-reverse/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1265.逆序打印不可变链表

[力扣](https://leetcode.cn/problems/print-immutable-linked-list-in-reverse/)

题目无法记录链表中的节点，因此只能按照类似树的后续遍历的处理方法，从链表头开始，先递归处理后续节点，然后再输出当前节点的值。

最后附上python代码：

```python
#   """
#   This is the ImmutableListNode's API interface.
#   You should not implement it, or speculate about its implementation.
#   """
#   class ImmutableListNode(object):
#      def printValue(self): # print the value of this node.
# .        """
#          :rtype None
#          """
#
#      def getNext(self): # return the next node.
# .        """
#          :rtype ImmutableListNode
#          """

class Solution(object):
    def printLinkedListInReverse(self, head):
        """
        :type head: ImmutableListNode
        :rtype: None
        """

        next = head.getNext()
        if next:
            self.printLinkedListInReverse(next)
        
        head.printValue()
```
