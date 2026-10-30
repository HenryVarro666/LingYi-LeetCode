---
title: "1206. 设计跳表"
aliases: ["yiduobo的每日leetcode 1206.设计跳表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382017240"
zhihu_id: "382017240"
zhihu_title: "yiduobo的每日leetcode 1206.设计跳表"
question_id: "1206"
question: "设计跳表"
problem_url: "https://leetcode.cn/problems/design-skiplist/"
created: "2021-06-18T23:50:47+08:00"
updated: "2021-06-18T23:50:47+08:00"
upvotes: 1
comments: 0
---

# 1206. 设计跳表

> **[yiduobo的每日leetcode 1206.设计跳表](https://zhuanlan.zhihu.com/p/382017240) · 知乎 · 2021-06-18 · 赞同 1**
> 力扣：[1206. 设计跳表](https://leetcode.cn/problems/design-skiplist/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1206.设计跳表

[力扣](https://leetcode-cn.com/problems/design-skiplist/)

老实说，我个人是不太喜欢跳表这种数据结构，因为总感觉其设计不是太优美。对于静态数据而言，性能最好的跳表自然是类似线段树式的结构，区别在于其子树的根节点是区间链表头。而对于动态的数据而言，跳表的索引结构本身是不太好维护的，这也就意味着在大量的增删操作之后跳表可能会退化回链表。

跳表的实现实际上可以认为是一种单向的十字链表，对于查找操作而言，每次查找都是从最顶层索引的头部开始向后遍历，找到该层最后一个满足值小于等于要查找的值的节点。若该节点的值就等于要查找的节点的值，那么说明该节点就是要找的节点，否则就通过该节点向下的指针来到下一层，然后继续寻找。重复此过程直到找到对应的节点或者没法再继续找下去。

对于插入操作来说，由于存在上面提到的退化的问题，那么一种常见的做法是利用随机数来对抗这些操作，即在增加节点时不根据当前跳表的长度和索引判断当前节点应当有几层索引，而是按照一个概率随机当前节点的索引层数。接下来在对应的层数中找到其前置节点，并将其插入，然后通过其前置节点来到下一层，并寻找下一层的前置节点进行插入。重复此过程直到完成最后一层的插入。

删除操作也类似，同样是找到对应的节点的前置节点，然后删除该节点之后通过前置节点来到下一层，并寻找下一层的前置节点进行删除。重复此过程直到完成最后一层的删除。

最后附上python代码：

```python
class Node(object):

    def __init__(self, v):
        self.next = None
        self.down = None
        self.val = v

class Skiplist(object):

    def __init__(self):
        self.head = None
        self.rate = 0.5
        self.level = 0
        self.max_level = 15

    def search(self, target):
        """
        :type target: int
        :rtype: bool
        """
        now = self.head
        now_level = self.level
        while now_level > 0:
            while now.next is not None and now.next.val <= target:
                now = now.next
            if now.val == target:
                return True
            now = now.down
            now_level -= 1
        
        return False

    def add(self, num):
        """
        :type num: int
        :rtype: None
        """
        add_level = 1
        while add_level < self.max_level and random.random() < self.rate:
            add_level += 1
        
        while self.level < add_level:
            tmp = Node(-1)
            tmp.down = self.head
            self.head = tmp
            self.level += 1
        
        now = self.head
        now_level = self.level
        last_level_node = None
        while now_level > 0:
            while now.next is not None and now.next.val <= num:
                now = now.next
            if now_level <= add_level:
                tmp = Node(num)
                tmp.next = now.next
                now.next = tmp
                if last_level_node is not None:
                    last_level_node.down = tmp
                last_level_node = tmp
            now = now.down
            now_level -= 1

    def erase(self, num):
        """
        :type num: int
        :rtype: bool
        """
        now = self.head
        now_level = self.level
        flag = False
        while now_level > 0:
            while now.next and now.next.val < num:
                now = now.next
            if now.next and now.next.val == num:
                flag = True
                now.next = now.next.next
            now = now.down
            now_level -= 1

        return flag

# Your Skiplist object will be instantiated and called as such:
# obj = Skiplist()
# param_1 = obj.search(target)
# obj.add(num)
# param_3 = obj.erase(num)
```
