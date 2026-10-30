---
title: "1115. 交替打印FooBar"
aliases: ["yiduobo的每日leetcode 1115.交替打印FooBar"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375567430"
zhihu_id: "375567430"
zhihu_title: "yiduobo的每日leetcode 1115.交替打印FooBar"
question_id: "1115"
question: "交替打印FooBar"
problem_url: "https://leetcode.cn/problems/print-foobar-alternately/"
created: "2021-05-26T23:22:43+08:00"
updated: "2021-05-26T23:22:43+08:00"
upvotes: 0
comments: 0
---

# 1115. 交替打印FooBar

> **[yiduobo的每日leetcode 1115.交替打印FooBar](https://zhuanlan.zhihu.com/p/375567430) · 知乎 · 2021-05-26 · 赞同 0**
> 力扣：[1115. 交替打印FooBar](https://leetcode.cn/problems/print-foobar-alternately/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1115.交替打印FooBar

[力扣](https://leetcode-cn.com/problems/print-foobar-alternately/)

还是多线程调度的题目，还是老做法，给每个函数弄一个信号量来进行控制。

题目要求foo和bar交替执行，foo先执行，那么初始化计数器的时候应该初始化semo_foo为1，semo_bar为0。在执行printFoo之前需要申请semo_foo，执行完毕之后则需要释放semo_bar；同样地，在执行printBar之前需要申请semo_bar，执行完毕之后则需要释放semo_foo。

最后附上python代码：

```python
import threading

class FooBar(object):
    def __init__(self, n):
        self.n = n
        self.foo_s = threading.Semaphore(1)
        self.bar_s = threading.Semaphore(0)

    def foo(self, printFoo):
        """
        :type printFoo: method
        :rtype: void
        """
        for i in xrange(self.n):
            
            self.foo_s.acquire()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.bar_s.release()

    def bar(self, printBar):
        """
        :type printBar: method
        :rtype: void
        """
        for i in xrange(self.n):
            
            self.bar_s.acquire()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.foo_s.release()
```
