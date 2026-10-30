---
title: "1114. 按序打印"
aliases: ["yiduobo的每日leetcode 1114.按序打印"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375240191"
zhihu_id: "375240191"
zhihu_title: "yiduobo的每日leetcode 1114.按序打印"
question_id: "1114"
question: "按序打印"
problem_url: "https://leetcode.cn/problems/print-in-order/"
created: "2021-05-25T22:01:38+08:00"
updated: "2021-05-25T22:01:38+08:00"
upvotes: 0
comments: 0
---

# 1114. 按序打印

> **[yiduobo的每日leetcode 1114.按序打印](https://zhuanlan.zhihu.com/p/375240191) · 知乎 · 2021-05-25 · 赞同 0**
> 力扣：[1114. 按序打印](https://leetcode.cn/problems/print-in-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1114.按序打印

[力扣](https://leetcode-cn.com/problems/print-in-order/)

从这里开始的若干题目与算法关系不大，主要是涉及到多线程相关的东西。

我在这里使用的是信号量。设置两个信号量first_semo以及second_semo用来表示first和second是否执行完毕。

对于first，当执行完printFirst之后，将first_semo release掉。

对于second，初始需要请求first_semo。只有当printFirst执行完毕，first_semo release掉之后才能请求到，才能够执行后面的printSecond，以及release second_semo。

对于third，初始需要请求second_semo。只有当printSecond执行完毕，second_semo release掉之后才能请求到，才能够执行后面的printThird。

最后附上python代码：

```python
import threading

class Foo(object):
    def __init__(self):
        self.first_s = threading.Semaphore(0)
        self.second_s = threading.Semaphore(0)

    def first(self, printFirst):
        """
        :type printFirst: method
        :rtype: void
        """
        
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.first_s.release()

    def second(self, printSecond):
        """
        :type printSecond: method
        :rtype: void
        """
        
        self.first_s.acquire()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.second_s.release()
            
    def third(self, printThird):
        """
        :type printThird: method
        :rtype: void
        """
        
        self.second_s.acquire()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()
```
