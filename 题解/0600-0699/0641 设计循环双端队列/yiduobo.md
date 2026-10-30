---
title: "641. 设计循环双端队列"
aliases: ["yiduobo的每日leetcode 641.设计循环双端队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/272857350"
zhihu_id: "272857350"
zhihu_title: "yiduobo的每日leetcode 641.设计循环双端队列"
question_id: "641"
question: "设计循环双端队列"
problem_url: "https://leetcode.cn/problems/design-circular-deque/"
created: "2020-11-03T22:48:35+08:00"
updated: "2020-11-03T22:48:35+08:00"
upvotes: 0
comments: 0
---

# 641. 设计循环双端队列

> **[yiduobo的每日leetcode 641.设计循环双端队列](https://zhuanlan.zhihu.com/p/272857350) · 知乎 · 2020-11-03 · 赞同 0**
> 力扣：[641. 设计循环双端队列](https://leetcode.cn/problems/design-circular-deque/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

641.设计循环双端队列

[力扣](https://leetcode-cn.com/problems/design-circular-deque/)

虽然题目是设计循环双端队列，但是实际上并没有体现到循环的相关操作。注意到这里所有的操作都跟队列头部或者队列尾部相关，那么只需要队列可以两头扩展或者删除就可以达成题目要求了，于是我们可以使用双向链表来实现。

具体来说就是维护一个head以及一个tail，其中head的下一个节点为队列的头部，而tail的上一个节点为队列的尾部。头部的操作涉及到的就是head以及队列的头部元素head.right，而尾部的操作则涉及到tail以及队列的尾部元素tail.left。

注意插入或删除之前需要判断是否还可以插入，或者是否存在节点需要删除。

最后附上python代码：

```python
class ListNode(object):

    def __init__(self, value):
        self.value = value
        self.left = self.right = None

class MyCircularDeque(object):

    def __init__(self, k):
        """
        Initialize your data structure here. Set the size of the deque to be k.
        :type k: int
        """
        self.k = k
        self.l = 0
        self.head = ListNode(-1)
        self.tail = ListNode(-1)
        self.head.right = self.tail
        self.tail.left = self.head

    def insertFront(self, value):
        """
        Adds an item at the front of Deque. Return true if the operation is successful.
        :type value: int
        :rtype: bool
        """
        if self.l == self.k:
            return False
        
        self.l += 1
        node = ListNode(value)
        self.head.right.left = node
        node.right = self.head.right
        self.head.right = node
        node.left = self.head
        return True

    def insertLast(self, value):
        """
        Adds an item at the rear of Deque. Return true if the operation is successful.
        :type value: int
        :rtype: bool
        """
        if self.l == self.k:
            return False

        self.l += 1
        node = ListNode(value)
        self.tail.left.right = node
        node.left = self.tail.left
        self.tail.left = node
        node.right = self.tail
        return True

    def deleteFront(self):
        """
        Deletes an item from the front of Deque. Return true if the operation is successful.
        :rtype: bool
        """
        if self.l == 0:
            return False
        
        self.l -= 1
        tmp = self.head.right
        self.head.right = tmp.right
        tmp.right.left = self.head
        del tmp
        return True

    def deleteLast(self):
        """
        Deletes an item from the rear of Deque. Return true if the operation is successful.
        :rtype: bool
        """
        if self.l == 0:
            return False

        self.l -= 1
        tmp = self.tail.left
        self.tail.left = tmp.left
        tmp.left.right = self.tail
        del tmp
        return True

    def getFront(self):
        """
        Get the front item from the deque.
        :rtype: int
        """
        return self.head.right.value

    def getRear(self):
        """
        Get the last item from the deque.
        :rtype: int
        """
        return self.tail.left.value

    def isEmpty(self):
        """
        Checks whether the circular deque is empty or not.
        :rtype: bool
        """
        return self.l == 0

    def isFull(self):
        """
        Checks whether the circular deque is full or not.
        :rtype: bool
        """
        return self.l == self.k

# Your MyCircularDeque object will be instantiated and called as such:
# obj = MyCircularDeque(k)
# param_1 = obj.insertFront(value)
# param_2 = obj.insertLast(value)
# param_3 = obj.deleteFront()
# param_4 = obj.deleteLast()
# param_5 = obj.getFront()
# param_6 = obj.getRear()
# param_7 = obj.isEmpty()
# param_8 = obj.isFull()
```
