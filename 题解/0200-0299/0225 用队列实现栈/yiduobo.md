---
title: "225. 用队列实现栈"
aliases: ["yiduobo的每日leetcode 225.用队列实现栈"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149312311"
zhihu_id: "149312311"
zhihu_title: "yiduobo的每日leetcode 225.用队列实现栈"
question_id: "225"
question: "用队列实现栈"
problem_url: "https://leetcode.cn/problems/implement-stack-using-queues/"
created: "2020-06-18T23:32:12+08:00"
updated: "2020-06-18T23:32:12+08:00"
upvotes: 0
comments: 0
---

# 225. 用队列实现栈

> **[yiduobo的每日leetcode 225.用队列实现栈](https://zhuanlan.zhihu.com/p/149312311) · 知乎 · 2020-06-18 · 赞同 0**
> 力扣：[225. 用队列实现栈](https://leetcode.cn/problems/implement-stack-using-queues/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

225.用队列实现栈<https://leetcode-cn.com/problems/implement-stack-using-queues/>

比较基础的题目。由于队列是先进先出的，因此如果要用队列模拟栈，那么要把晚进来的数据放在队列的头部，才能达成栈后进先出的效果。

具体来说就是在新元素进来的时候，先加入到队尾，需要从头开始将队列中的元素依次弹出并加入到队尾，直到新加入的元素成为队首。

其他的弹出、栈顶等操作就是访问队首元素了。

最后附上python代码：

```python
class MyStack(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.q = []

    def push(self, x):
        """
        Push element x onto stack.
        :type x: int
        :rtype: None
        """
        self.q.append(x)
        size = len(self.q)
        while size > 1:
            self.q.append(self.q.pop(0))
            size -= 1

    def pop(self):
        """
        Removes the element on top of the stack and returns that element.
        :rtype: int
        """
        return self.q.pop(0)

    def top(self):
        """
        Get the top element.
        :rtype: int
        """
        return self.q[0]

    def empty(self):
        """
        Returns whether the stack is empty.
        :rtype: bool
        """
        return len(self.q) == 0

# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
```
