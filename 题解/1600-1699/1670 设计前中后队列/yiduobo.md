---
title: "1670. 设计前中后队列"
aliases: ["yiduobo的每日leetcode 1670.设计前中后队列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/design", "leetcode/queue", "leetcode/linked-list", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/443430964"
zhihu_id: "443430964"
zhihu_title: "yiduobo的每日leetcode 1670.设计前中后队列"
question_id: "1670"
question: "设计前中后队列"
problem_url: "https://leetcode.cn/problems/design-front-middle-back-queue/"
difficulty: "Medium"
rating: 1610
created: "2021-12-10T00:01:26+08:00"
updated: "2021-12-10T00:01:26+08:00"
upvotes: 0
comments: 0
---

# 1670. 设计前中后队列

> **[yiduobo的每日leetcode 1670.设计前中后队列](https://zhuanlan.zhihu.com/p/443430964) · 知乎 · 2021-12-10 · 赞同 0**
> 力扣：[1670. 设计前中后队列](https://leetcode.cn/problems/design-front-middle-back-queue/) · Medium · 灵茶山艾府：[【图解】两个双端队列+简洁写法（Python/Java/C++/Go/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1670.设计前中后队列

[力扣](https://leetcode-cn.com/problems/design-front-middle-back-queue/)

本题与之前的某一题数据流的中位数很类似，在这里同样是拆成两个部分。对于这两个部分都需要双端的插入和弹出操作，因此可以使用分别维护两个双端队列。

方便起见，在这里可以默认左侧队列的长度小于等于右侧队列的长度，若在某一次操作后左侧队列的长度大于右侧队列，那么就将左侧队列的末尾弹出然后插入到右侧队列的头部。

对于题目中涉及队列头部的操作，对应的是左侧队列的头部；涉及队列尾部的操作，对应的是右侧队列的尾部；涉及到队列中部的操作，则需要根据当前左右队列的长度决定对应到左侧队列的维护还是右侧队列的头部。具体操作并不难但是文字描述比较复杂，这里就不展开了。

除此之外，还需特别注意两个队列为空或者左侧队列为空的情况。

具体实现方面，可以使用语言自带的数据结构，也可以手动实现双向链表。

最后附上python代码：

```python
class Node(object):

    def __init__(self, val):
        self.next = None
        self.prev = None
        self.val = val

class LinkedList(object):

    def __init__(self):
        self.head = Node(0)
        self.tail = Node(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cnt = 0
    
    def addHead(self, node):
        self.head.next.prev = node
        node.next = self.head.next
        self.head.next = node
        node.prev = self.head
        self.cnt += 1
    
    def addTail(self, node):
        self.tail.prev.next = node
        node.prev = self.tail.prev
        self.tail.prev = node
        node.next = self.tail
        self.cnt += 1
    
    def removeHead(self):
        if self.cnt > 0:
            node = self.head.next
            self.head.next = node.next
            node.next.prev = self.head
            self.cnt -= 1
            return node
        
        return None
    
    def removeTail(self):
        if self.cnt > 0:
            node = self.tail.prev
            self.tail.prev = node.prev
            node.prev.next = self.tail
            self.cnt -= 1
            return node
        
        return None

class FrontMiddleBackQueue(object):

    def __init__(self):
        self.left = LinkedList()
        self.right = LinkedList()

    def pushFront(self, val):
        """
        :type val: int
        :rtype: None
        """
        node = Node(val)
        self.left.addHead(node)
        if self.left.cnt > self.right.cnt:
            node = self.left.removeTail()
            self.right.addHead(node)

    def pushMiddle(self, val):
        """
        :type val: int
        :rtype: None
        """
        node = Node(val)
        if self.left.cnt < self.right.cnt:
            self.left.addTail(node)
        else:
            self.right.addHead(node)

    def pushBack(self, val):
        """
        :type val: int
        :rtype: None
        """
        node = Node(val)
        self.right.addTail(node)
        if self.right.cnt - self.left.cnt == 2:
            node = self.right.removeHead()
            self.left.addTail(node)

    def popFront(self):
        """
        :rtype: int
        """
        if self.left.cnt > 0:
            res = self.left.removeHead().val
            if self.right.cnt - self.left.cnt == 2:
               node = self.right.removeHead()
               self.left.addTail(node)
            return res

        elif self.right.cnt > 0:
            return self.right.removeHead().val
        
        else:
            return -1

    def popMiddle(self):
        """
        :rtype: int
        """
        if self.left.cnt == self.right.cnt:
            if self.left.cnt == 0:
                return -1
            else:
                return self.left.removeTail().val
        
        else:
            return self.right.removeHead().val

    def popBack(self):
        """
        :rtype: int
        """
        if self.right.cnt == 0:
            return -1
        
        res = self.right.removeTail().val
        if self.right.cnt < self.left.cnt:
            node = self.left.removeTail()
            self.right.addHead(node)
        
        return res

# Your FrontMiddleBackQueue object will be instantiated and called as such:
# obj = FrontMiddleBackQueue()
# obj.pushFront(val)
# obj.pushMiddle(val)
# obj.pushBack(val)
# param_4 = obj.popFront()
# param_5 = obj.popMiddle()
# param_6 = obj.popBack()
```
