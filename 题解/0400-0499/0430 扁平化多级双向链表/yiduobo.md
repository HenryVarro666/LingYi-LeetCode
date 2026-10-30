---
title: "430. 扁平化多级双向链表"
aliases: ["yiduobo的每日leetcode 430.扁平化多级双向链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/196784278"
zhihu_id: "196784278"
zhihu_title: "yiduobo的每日leetcode 430.扁平化多级双向链表"
question_id: "430"
question: "扁平化多级双向链表"
problem_url: "https://leetcode.cn/problems/flatten-a-multilevel-doubly-linked-list/"
created: "2020-08-24T21:53:43+08:00"
updated: "2020-08-24T21:53:43+08:00"
upvotes: 0
comments: 0
---

# 430. 扁平化多级双向链表

> **[yiduobo的每日leetcode 430.扁平化多级双向链表](https://zhuanlan.zhihu.com/p/196784278) · 知乎 · 2020-08-24 · 赞同 0**
> 力扣：[430. 扁平化多级双向链表](https://leetcode.cn/problems/flatten-a-multilevel-doubly-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

430.扁平化多级双向链表<https://leetcode-cn.com/problems/flatten-a-multilevel-doubly-linked-list/>

看题目描述还是蛮复杂的，不过看题目给出的样例图就比较清晰了。

对于样例中出现的两个child，题目都是将其扶正到了next的位置上，同时原先的next则是接到了child部分中最后一个节点的后面。例如3的child是7，被移动到了3的next位子上，而3初始的next节点8则是移动到了以3为首的这一堆节点的最后一个节点10的后面。

于是一个自然的想法就是维护一个栈。每处理到一个节点，先将其next节点入栈，然后将其child节点入栈，接下来从栈顶弹出一个节点作为下一个节点进行处理。

需要注意的是，题目除了next和child之外，还存在prev指针，因此每次操作时需要保存住上一个处理的节点的信息。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
"""

class Solution(object):
    def flatten(self, head):
        """
        :type head: Node
        :rtype: Node
        """

        if not head:
            return head

        stack = [head]
        prev_node = None
        while stack:
            now = stack.pop()
            now.prev = prev_node
            if prev_node:
                prev_node.next = now

            if now.next:
                stack.append(now.next)
            if now.child:
                stack.append(now.child)
                now.child = None
            prev_node = now

        return head
```
