---
title: "146. LRU缓存机制"
aliases: ["yiduobo的每日leetcode 146.LRU缓存机制"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/linked-list", "leetcode/doubly-linked-list", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/编程能力强化训练", "题单/链表-二叉树与回溯/一-链表", "题单/LeetCode-热题-100/链表", "题单/面试经典-150-题/链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/142673459"
zhihu_id: "142673459"
zhihu_title: "yiduobo的每日leetcode 146.LRU缓存机制"
question_id: "146"
question: "LRU 缓存"
problem_url: "https://leetcode.cn/problems/lru-cache/"
difficulty: "Medium"
created: "2020-05-21T23:07:15+08:00"
updated: "2020-05-21T23:07:15+08:00"
upvotes: 2
comments: 0
---

# 146. LRU缓存机制

> **[yiduobo的每日leetcode 146.LRU缓存机制](https://zhuanlan.zhihu.com/p/142673459) · 知乎 · 2020-05-21 · 赞同 2**
> 力扣：[146. LRU 缓存](https://leetcode.cn/problems/lru-cache/) · Medium · 灵茶山艾府：[【图解】一张图秒懂 LRU！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

146.LRU缓存机制<https://leetcode-cn.com/problems/lru-cache/>

首先，对于key-value的存取过程，使用dict可以满足题目需求，那么问题就变成了如何找到最久未使用的key。

一种直观的想法对于每个key维护一个时间戳，然后每次操作的时候更新时间戳，同时维护最老的时间戳用于替换。但是数值类比较在这个里面时间复杂度的下限应该是O(logn)的（不确定，不过应该可以证明），不满足题目的要求。

另一种思路就是维护一个队列，将新来的放在队列的尾部，同时将队列的头部踢出去。但是，遇到cache命中的情况，需要将队列中的某个值移动到队列的尾部，这种时候就需要链表的帮助了。

于是，现在的做法就变成了：

1、对于每次get，先检测其是否存在，若存在，将其从链表中删去，然后插入到链表的尾部。

2、对于每次set，先检测其是否存在，若存在，将其从链表中删去，更新value之后插入到链表的尾部。若不存在，则删去链表的头部元素，然后新加入节点设置好key，value之后插入到链表的尾部。

对于链表中的插入删除，使用双向链表会非常方便，即删除节点now只需要

now.prev.next \= now.next

now.next.prev \= now.prev

此时，now还未从内存中删去，那么如果想恢复now节点，只需要

now.prev.next \= now

now.next.prev \= now

当然，恢复操作在这里用不上，但是在某些搜索回溯场景中，例如使用dlx解决数独问题时，这种删除与恢复操作是非常高效的。

另外，为了方便起见，可以在链表中先设置一个假头head与一个假尾tail，就不需要判断now是否存在prev与next了。

最后附上python代码：

```python
class ListNode(object):

    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """

        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.head = ListNode()
        self.tail = ListNode()
        self.head.prev = self.tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.tail.next = self.head

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_tail(self, node):
        self.tail.prev.next = node
        node.prev = self.tail.prev
        self.tail.prev = node
        node.next = self.tail

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.remove_node(node)
        self.move_tail(node)
        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.remove_node(node)
        else:
            if self.size == self.capacity:
                node = self.head.next
                self.remove_node(node)
                self.cache.pop(node.key)
                node.key = key
                node.val = value
            else:
                node = ListNode(key, value)
                self.cache[key] = node
                self.size += 1
            
            self.cache[key] = node

        self.move_tail(node)

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```
