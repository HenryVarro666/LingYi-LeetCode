---
title: "817. 链表组件"
aliases: ["yiduobo的每日leetcode 817.链表组件"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343831085"
zhihu_id: "343831085"
zhihu_title: "yiduobo的每日leetcode 817.链表组件"
question_id: "817"
question: "链表组件"
problem_url: "https://leetcode.cn/problems/linked-list-components/"
created: "2021-01-15T22:31:39+08:00"
updated: "2021-01-15T22:31:39+08:00"
upvotes: 0
comments: 0
---

# 817. 链表组件

> **[yiduobo的每日leetcode 817.链表组件](https://zhuanlan.zhihu.com/p/343831085) · 知乎 · 2021-01-15 · 赞同 0**
> 力扣：[817. 链表组件](https://leetcode.cn/problems/linked-list-components/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

817.链表组件

[力扣](https://leetcode-cn.com/problems/linked-list-components/)

我们直接从头开始往后遍历整个链表，使用一个标记flag来表示之前是否有节点在G当中。flag初始值为flase。对于当前节点：

1、若当前节点在G当中：

置flag为true

2、若当前节点不在G当中：

若当前flag为true，说明当前节点之前存在若干个连续节点在G当中，因此组件数加一，同时置flag为false

当遍历完成后，若flag为true，说明最后的几个节点也是一个组件，因此组件数还需要加一。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def numComponents(self, head, G):
        """
        :type head: ListNode
        :type G: List[int]
        :rtype: int
        """

        num_set = set(G)
        now = head
        flag = False
        res = 0
        while now:
            if now.val in num_set:
                flag = True
            else:
                if flag:
                    res += 1
                flag = False
            now = now.next
        
        if flag:
            res += 1
            
        return res
```
