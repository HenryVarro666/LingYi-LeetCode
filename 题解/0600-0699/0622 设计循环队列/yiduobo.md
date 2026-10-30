---
title: "622. 设计循环队列"
aliases: ["yiduobo的每日leetcode 622.设计循环队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/269643466"
zhihu_id: "269643466"
zhihu_title: "yiduobo的每日leetcode 622.设计循环队列"
question_id: "622"
question: "设计循环队列"
problem_url: "https://leetcode.cn/problems/design-circular-queue/"
created: "2020-10-28T23:59:03+08:00"
updated: "2020-10-28T23:59:03+08:00"
upvotes: 0
comments: 0
---

# 622. 设计循环队列

> **[yiduobo的每日leetcode 622.设计循环队列](https://zhuanlan.zhihu.com/p/269643466) · 知乎 · 2020-10-28 · 赞同 0**
> 力扣：[622. 设计循环队列](https://leetcode.cn/problems/design-circular-queue/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

622.设计循环队列<https://leetcode-cn.com/problems/design-circular-queue/>

题目要求实现循环队列，具体为插入、删除、获取队首或队尾元素值这几种操作。队列是先进先出，因此插入需要我们维护队尾元素，而删除则需要维护队首元素，恰好与获取队首队尾元素重叠。

由于题目没有要求我们展现出“循环”这个性质，因此我们只需要想办法维护住队首和队尾即可，而最简单的做法就是维护一条单链表的头尾节点。

对于插入操作，我们新建一个节点。若当前链表为空，那么将头尾节点都置为该节点，否则将尾结点的next指向当前结点，然后将尾结点置为该节点。

对于删除操作，若链表中只有一个元素，那么将头尾节点都置为空，否则将头结点置为头结点的next节点，然后删去原先的头结点。

最后附上python代码：

```python
class Node(object):

    def __init__(self, val):
        self.val = val
        self.next = None

class MyCircularQueue(object):

    def __init__(self, k):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        :type k: int
        """
        self.head = self.tail = None
        self.k = k
        self.cnt = 0

    def enQueue(self, value):
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        :type value: int
        :rtype: bool
        """
        if self.cnt == self.k:
            return False

        tmp = Node(value)
        if self.cnt == 0:
            self.head = self.tail = tmp
        else:
            self.tail.next = tmp
            self.tail = tmp
        self.cnt += 1
        return True

    def deQueue(self):
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        :rtype: bool
        """
        if self.cnt == 0:
            return False

        tmp = self.head

        if self.cnt == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
        self.cnt -= 1
        del tmp
        return True

    def Front(self):
        """
        Get the front item from the queue.
        :rtype: int
        """
        if self.head:
            return self.head.val
        return -1

    def Rear(self):
        """
        Get the last item from the queue.
        :rtype: int
        """
        if self.tail:
            return self.tail.val
        return -1

    def isEmpty(self):
        """
        Checks whether the circular queue is empty or not.
        :rtype: bool
        """
        return self.cnt == 0

    def isFull(self):
        """
        Checks whether the circular queue is full or not.
        :rtype: bool
        """
        return self.cnt == self.k

# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()
```
