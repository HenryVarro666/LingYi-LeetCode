---
title: "707. 设计链表"
aliases: ["yiduobo的每日leetcode 707.设计链表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/324674582"
zhihu_id: "324674582"
zhihu_title: "yiduobo的每日leetcode 707.设计链表"
question_id: "707"
question: "设计链表"
problem_url: "https://leetcode.cn/problems/design-linked-list/"
created: "2020-12-01T22:17:55+08:00"
updated: "2020-12-01T22:17:55+08:00"
upvotes: 0
comments: 0
---

# 707. 设计链表

> **[yiduobo的每日leetcode 707.设计链表](https://zhuanlan.zhihu.com/p/324674582) · 知乎 · 2020-12-01 · 赞同 0**
> 力扣：[707. 设计链表](https://leetcode.cn/problems/design-linked-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

707.设计链表

[力扣](https://leetcode-cn.com/problems/design-linked-list/)

就是普通的链表操作问题。注意到题目有插入头部和插入尾部的操作，因此可以维护head节点和tail节点，初始状态下二者互联。当要在头部插入时，就将新节点插入到head与head.next之间；当要在尾部插入时，则是插入到tail与tail.prev之间。

剩下的插入到index以及删除index的操作，则可以先从head或tail开始找到链表中对应的节点然后进行操作即可。

最后附上python代码：

```python
class Node(object):

    def __init__(self, val=0):
        self.val = val
        self.next = None
        self.prev = None

class MyLinkedList(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def findIndex(self, k):
        if k + 1 < self.length - k:
            now = self.head
            for index in range(k + 1):
                now = now.next
        else:
            now = self.tail
            for index in range(self.length - k):
                now = now.prev
        
        return now

    def get(self, index):
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        :type index: int
        :rtype: int
        """
        if index < 0 or index >= self.length:
            return -1

        return self.findIndex(index).val

    def addAtHead(self, val):
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        :type val: int
        :rtype: None
        """
        node = Node(val)
        node.next = self.head.next
        self.head.next.prev = node
        node.prev = self.head
        self.head.next = node
        self.length += 1

    def addAtTail(self, val):
        """
        Append a node of value val to the last element of the linked list.
        :type val: int
        :rtype: None
        """
        node = Node(val)
        node.prev = self.tail.prev
        self.tail.prev.next = node
        node.next = self.tail
        self.tail.prev = node
        self.length += 1

    def addAtIndex(self, index, val):
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        :type index: int
        :type val: int
        :rtype: None
        """
        if index < 0:
            self.addAtHead(val)
        elif index == self.length:
            self.addAtTail(val)
        elif index > self.length:
            return
        else:
            tmp = self.findIndex(index)
            node = Node(val)
            tmp.prev.next = node
            node.prev = tmp.prev
            tmp.prev = node
            node.next = tmp
            self.length += 1

    def deleteAtIndex(self, index):
        """
        Delete the index-th node in the linked list, if the index is valid.
        :type index: int
        :rtype: None
        """
        if index >= 0 and index < self.length:
            tmp = self.findIndex(index)
            tmp.prev.next = tmp.next
            tmp.next.prev = tmp.prev
            del tmp
            self.length -= 1

# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
```
