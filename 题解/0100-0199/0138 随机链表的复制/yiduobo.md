---
title: "138. 复制带随机指针的链表"
aliases: ["yiduobo的每日leetcode 138.复制带随机指针的链表"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141903338"
zhihu_id: "141903338"
zhihu_title: "yiduobo的每日leetcode 138.复制带随机指针的链表"
question_id: "138"
question: "随机链表的复制"
problem_url: "https://leetcode.cn/problems/copy-list-with-random-pointer/"
difficulty: "Medium"
created: "2020-05-18T23:54:17+08:00"
updated: "2020-05-18T23:54:17+08:00"
upvotes: 0
comments: 0
---

# 138. 复制带随机指针的链表

> **[yiduobo的每日leetcode 138.复制带随机指针的链表](https://zhuanlan.zhihu.com/p/141903338) · 知乎 · 2020-05-18 · 赞同 0**
> 力扣：[138. 随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/) · Medium · 灵茶山艾府：[不用哈希表，简洁写法（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

138.复制带随机指针的链表<https://leetcode-cn.com/problems/copy-list-with-random-pointer/>

经典的链表问题。我在这里的做法是对于每个节点p，复制节点p'接在p的后面。

设p的random为q，那么我们需要将p'的random指向到q'。由于q'为q的next，于是就有p的random实际上就是q的next，而q又是p的random，于是最终p的random就是q的next的random了。

连接好random指针后，只需要再逐个断开p与p'，重新回到原先的连接方式就行了。

最后附上python代码，其中第一段while为复制节点获得p'，第二段while则是设置random指针，最后一段while为调整回原始的连接方式：

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution(object):
    def copyRandomList(self, head):
        """
        :type head: Node
        :rtype: Node
        """

        if not head:
            return head

        now = head
        while now:
            copy_now = Node(now.val)
            copy_now.next = now.next
            now.next = copy_now
            now = copy_now.next

        now = head
        while now:
            if now.random is not None:
                now.next.random = now.random.next
            now = now.next.next
            
        old_head = head
        res = new_head = head.next
        while old_head:
            old_head.next = new_head.next
            old_head = old_head.next
            if old_head:
                new_head.next = old_head.next
                new_head = new_head.next
                
        return res
```
