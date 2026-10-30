---
title: "232. 用栈实现队列"
aliases: ["yiduobo的每日leetcode 232.用栈实现队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149855088"
zhihu_id: "149855088"
zhihu_title: "yiduobo的每日leetcode 232.用栈实现队列"
question_id: "232"
question: "用栈实现队列"
problem_url: "https://leetcode.cn/problems/implement-queue-using-stacks/"
created: "2020-06-21T20:19:42+08:00"
updated: "2020-06-21T20:19:42+08:00"
upvotes: 0
comments: 0
---

# 232. 用栈实现队列

> **[yiduobo的每日leetcode 232.用栈实现队列](https://zhuanlan.zhihu.com/p/149855088) · 知乎 · 2020-06-21 · 赞同 0**
> 力扣：[232. 用栈实现队列](https://leetcode.cn/problems/implement-queue-using-stacks/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

232.用栈实现队列<https://leetcode-cn.com/problems/implement-queue-using-stacks/>

这里需要用栈来实现队列，主要难点在于pop时需要将当前栈底元素pop出来，于是需要逐个从栈顶pop元素。注意到拿栈底元素之前的一系列pop操作最终得到的序列实际上队列的反序，那么将这个序列再压入栈中，此时栈就跟队列是一样的了。但是这样一来如果有新的数据进来，那么就无法维护这个数据结构了，于是可以一个想法是使用一个辅助栈。当遇到pop操作时，从栈顶开始逐个pop元素并压入辅助栈中，当主栈pop空之后此时辅助栈就是原先主栈的反序。

在获取到辅助栈之后，如果其不为空，那么之后的pop操作都通过pop辅助栈来完成，否则重复上面的操作生成辅助栈。

无论如何，入栈操作都还是压入主栈。

构造辅助栈的时间复杂度为O(n)，但是对于每个元素在主栈和辅助栈都至多会出栈一次，因此pop的均摊复杂度为O(1)。压栈则是都压入主栈，因此时间复杂度为O(1)。

最后附上python代码：

```python
class MyQueue(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack1 = []
        self.stack2 = []
        self.first = None

    def push(self, x):
        """
        Push element x to the back of queue.
        :type x: int
        :rtype: None
        """
        if not self.stack1:
            self.first = x
        self.stack1.append(x)

    def pop(self):
        """
        Removes the element from in front of queue and returns that element.
        :rtype: int
        """
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()

    def peek(self):
        """
        Get the front element.
        :rtype: int
        """
        if self.stack2:
            return self.stack2[-1]
        else:
            return self.first

    def empty(self):
        """
        Returns whether the queue is empty.
        :rtype: bool
        """
        return not self.stack1 and not self.stack2

# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```
