---
title: "284. 顶端迭代器"
aliases: ["yiduobo的每日leetcode 284.顶端迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/154601903"
zhihu_id: "154601903"
zhihu_title: "yiduobo的每日leetcode 284.顶端迭代器"
question_id: "284"
question: "顶端迭代器"
problem_url: "https://leetcode.cn/problems/peeking-iterator/"
created: "2020-07-03T22:38:53+08:00"
updated: "2020-07-03T22:38:53+08:00"
upvotes: 0
comments: 0
---

# 284. 顶端迭代器

> **[yiduobo的每日leetcode 284.顶端迭代器](https://zhuanlan.zhihu.com/p/154601903) · 知乎 · 2020-07-03 · 赞同 0**
> 力扣：[284. 顶端迭代器](https://leetcode.cn/problems/peeking-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

284.顶端迭代器<https://leetcode-cn.com/problems/peeking-iterator/>

实际上我半天都没有读懂这个题目要干什么。。我的理解是，现在有一个容器和一个迭代器，然后这个迭代器可以逐个弹出容器中的元素，要求实现一个peek操作，作用是查看当前容器的顶端，且不会弹出该元素。

我的思路也比较简单，就是维护一个peek缓存。

当peek操作过来时，若peek缓存为空，那么就调用原迭代器获取对应元素并返回。若peek缓存不为空，那么就直接返回peek。

当next操作过来时，若peek缓存为空，那么调用原迭代器的next方法。若peek缓存不为空，那么就返回peek缓存，并将改缓存清空。

当has_next操作过来时，若peek缓存为空且原迭代器的has_next为False，那么就返回False，否则返回True。

最后附上python代码：

```python
# Below is the interface for Iterator, which is already defined for you.
#
# class Iterator(object):
#     def __init__(self, nums):
#         """
#         Initializes an iterator object to the beginning of a list.
#         :type nums: List[int]
#         """
#
#     def hasNext(self):
#         """
#         Returns true if the iteration has more elements.
#         :rtype: bool
#         """
#
#     def next(self):
#         """
#         Returns the next element in the iteration.
#         :rtype: int
#         """

class PeekingIterator(object):
    def __init__(self, iterator):
        """
        Initialize your data structure here.
        :type iterator: Iterator
        """
        self.peek_res = None
        self.iterator = iterator
        

    def peek(self):
        """
        Returns the next element in the iteration without advancing the iterator.
        :rtype: int
        """
        if self.peek_res is None:
            self.peek_res = self.iterator.next()
            return self.peek_res
        return self.peek_res

    def next(self):
        """
        :rtype: int
        """
        if self.peek_res is not None:
            tmp = self.peek_res
            self.peek_res = None
            return tmp
        else:
            return self.iterator.next()

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.peek_res is not None or self.iterator.hasNext()

# Your PeekingIterator object will be instantiated and called as such:
# iter = PeekingIterator(Iterator(nums))
# while iter.hasNext():
#     val = iter.peek()   # Get the next element but not advance the iterator.
#     iter.next()         # Should return the same value as [val].
```
